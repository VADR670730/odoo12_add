# -*- coding: utf-8 -*-

from odoo import models, fields


class StockMove(models.Model):
    _inherit = 'stock.move'

    is_manual_reserved = fields.Boolean(string='是否已手动保留', default=False, copy=False)

    def action_show_details(self):
        self.ensure_one()
        result = super(StockMove, self).action_show_details()
        result['context'].update({'isIncoming': self.picking_id.picking_type_code == 'incoming',
                                  'show_reserved_quantity': not (self.picking_id.picking_type_code == 'incoming')})
        return result

    def action_show_details_wizard(self):
        if self.picking_id.picking_type_code == 'incoming':
            return False

        quant_ids = self.env['stock.quant'].search(
            [('product_id', '=', self.product_id.id), ('location_id', '=', self.location_id.id),
             ('quantity', '!=', 0)], order='lot_id asc')
        move_wizard = self.env['stock.move.wizard'].create({
            'stock_move_id': self.id
        })
        for quant in quant_ids:
            self.env['stock.move.line.wizard'].create({
                'is_selected': False,
                'quant_id': quant.id,
                'move_id': move_wizard.id
            })

        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_id': move_wizard.id,
            'res_model': 'stock.move.wizard',
            'target': 'new',
        }

    def _do_unreserve(self):
        for stock_move in self:
            stock_move.is_manual_reserved = False
        super(StockMove, self)._do_unreserve()

    def _action_assign(self):
        for stock_move in self:
            if not stock_move.is_manual_reserved:
                super(StockMove, stock_move)._action_assign()

