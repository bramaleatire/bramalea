# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.onchange('price_unit')
    def _onchange_price_unit_restrict(self):
        """Bloquea cambios manuales en vista, pero NO los automáticos por cambio de producto."""
        if not self.env.user.has_group('bramalea.group_no_edit_price'):
            return

        if self._origin:
            # si el precio cambia y NO se cambió el producto → bloqueo
            if (
                self.price_unit != self._origin.price_unit
                and self.product_id == self._origin.product_id
            ):
                raise UserError("You are not allowed to manually modify Unit Price.")

    def write(self, vals):
        """Bloquea cambios en servidor, pero permite cambios por cambio de producto."""
        if 'price_unit' in vals:
            if self.env.user.has_group('bramalea.group_no_edit_price'):

                # permitir si el cambio viene junto a product_id
                if 'product_id' in vals:
                    return super().write(vals)

                # obtener valor anterior
                for line in self:
                    if vals['price_unit'] != line.price_unit:
                        raise UserError("You are not allowed to modify Unit Price.")

        return super().write(vals)
