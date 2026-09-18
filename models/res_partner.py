# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError
import requests
import logging

_logger = logging.getLogger(__name__)

# Base URL of the Laravel wholesale portal API (e.g. https://tirebasics.ca/api),
# read from Settings > Technical > System Parameters under this key.
#
# When the parameter is unset the portal integration is simply OFF: no HTTP call
# is ever made and the portal fields read as empty. This used to be a hardcoded
# placeholder ("https://your-laravel-site.com/api") that did not resolve, so
# every read of last_login / failed_logins blocked on a DNS failure -- one call
# per partner, serialized -- which stalled contact forms and timed out exports.
LARAVEL_BASE_URL_PARAM = "bramalea.laravel_base_url"

# last_login / failed_logins are non-stored computes backed by an HTTP call.
# That is acceptable for a single form view and ruinous for a list view or an
# export, where the call is paid per record. Above this many records we skip the
# API entirely and leave the fields empty rather than make the user wait.
LARAVEL_MAX_SYNC_RECORDS_PARAM = "bramalea.laravel_max_sync_records"
DEFAULT_MAX_SYNC_RECORDS = 20

REQUEST_TIMEOUT = 5


class ResPartner(models.Model):
    _inherit = 'res.partner'

    portal_status = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive')],
        default='inactive',
        string="Portal Status",
        help="Set to Active to grant wholesale site access."
    )
    last_login = fields.Datetime(
        string="Last Login",
        compute="_compute_portal_info_from_api",
        store=False
    )
    failed_logins = fields.Integer(
        string="Failed Logins",
        compute="_compute_portal_info_from_api",
        store=False
    )
    wholesale_role = fields.Selection(
        [('admin', 'Admin'),
         ('purchaser', 'Purchaser'),
         ('accountant', 'Accountant')],
        string="Wholesale Role"
    )

    company_name = fields.Char('Company name', related='parent_id.name')

    # ===========================
    # PORTAL API CONFIGURATION
    # ===========================
    def _laravel_base_url(self):
        """Configured base URL of the portal API, or False when the integration
        is not configured -- in which case every call below is a no-op."""
        param = self.env["ir.config_parameter"].sudo().get_param(LARAVEL_BASE_URL_PARAM)
        return (param or "").strip().rstrip("/") or False

    def _laravel_max_sync_records(self):
        raw = self.env["ir.config_parameter"].sudo().get_param(LARAVEL_MAX_SYNC_RECORDS_PARAM)
        try:
            return int(raw)
        except (TypeError, ValueError):
            return DEFAULT_MAX_SYNC_RECORDS

    # ===========================
    # FETCH LARAVEL PORTAL INFO
    # ===========================
    @api.depends('portal_status')
    def _compute_portal_info_from_api(self):
        # Assign every record up front, so the compute is complete even when the
        # integration is off, skipped for size, or the API is unreachable.
        for partner in self:
            partner.last_login = False
            partner.failed_logins = 0

        base_url = self._laravel_base_url()
        if not base_url:
            return

        targets = self.filtered(lambda p: p.portal_status == 'active')
        if not targets:
            return

        limit = self._laravel_max_sync_records()
        if len(targets) > limit:
            _logger.info(
                "bramalea: skipping portal-info fetch for %s partners (limit %s); "
                "list views and exports do not wait on the portal API.",
                len(targets), limit)
            return

        for partner in targets:
            try:
                response = requests.get(
                    "%s/portal-info/%s" % (base_url, partner.id),
                    timeout=REQUEST_TIMEOUT)
            except Exception as e:  # noqa: BLE001
                # An unreachable host stays unreachable for the rest of this
                # batch: log once and stop, instead of paying the timeout again
                # for every remaining partner.
                _logger.warning(
                    "bramalea: portal API unreachable (%s); skipping the "
                    "remaining portal-info fetches in this batch.", e)
                return
            if response.status_code != 200:
                _logger.warning(
                    "bramalea: portal API returned %s for partner %s",
                    response.status_code, partner.id)
                continue
            try:
                data = response.json()
            except ValueError:
                _logger.warning(
                    "bramalea: portal API returned non-JSON for partner %s", partner.id)
                continue
            partner.last_login = data.get('last_login')
            partner.failed_logins = data.get('failed_logins', 0)

    # ===========================
    # HANDLE PORTAL STATUS CHANGE
    # ===========================
    def _call_laravel_portal_api(self, status):
        base_url = self._laravel_base_url()
        if not base_url:
            return
        for partner in self:
            try:
                response = requests.post(
                    "%s/update-portal-status" % base_url,
                    json={"contact_id": partner.id, "status": status},
                    timeout=REQUEST_TIMEOUT)
                if response.status_code != 200:
                    _logger.error(
                        "Failed to update portal status for %s: %s",
                        partner.name, response.text)
            except Exception as e:  # noqa: BLE001
                _logger.error("Error calling Laravel API for %s: %s", partner.name, e)

    def write(self, vals):
        if 'portal_status' in vals:
            # Call the API once for the partners that actually change. This used
            # to loop over self and call self._call_laravel_portal_api(), firing
            # one request per partner per partner (N^2) on a multi-record write.
            changed = self.filtered(lambda p: p.portal_status != vals['portal_status'])
            if changed:
                changed._call_laravel_portal_api(vals['portal_status'])
        return super().write(vals)

    # ===========================
    # PASSWORD RESET BUTTON
    # ===========================
    def action_reset_password(self):
        base_url = self._laravel_base_url()
        if not base_url:
            # This is a user-initiated button: say so, rather than logging an
            # error the user never sees and letting them think it was sent.
            raise UserError(_(
                "The wholesale portal API is not configured, so no password "
                "reset was sent. Set the system parameter '%s' first.",
                LARAVEL_BASE_URL_PARAM))
        for partner in self:
            try:
                response = requests.post(
                    "%s/reset-password" % base_url,
                    json={"contact_id": partner.id},
                    timeout=REQUEST_TIMEOUT)
                if response.status_code != 200:
                    _logger.error(
                        "Failed to reset password for %s: %s", partner.name, response.text)
            except Exception as e:  # noqa: BLE001
                _logger.error("Error calling reset password for %s: %s", partner.name, e)
