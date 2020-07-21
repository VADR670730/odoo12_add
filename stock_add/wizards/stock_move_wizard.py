# -*- coding: utf-8 -*-

from odoo import models, fields, api


class move_wizard(models.TransientModel):
    _name = 'stock.move.wizard'

    product_id = fields.Many2one("product.product", string="产品", related="stock_move_id.product_id", required=True)
    product_uom = fields.Many2one('uom.uom', string='单位', related="stock_move_id.product_uom", required=True)
    product_uom_qty = fields.Float(string="初始需求", related="stock_move_id.product_uom_qty", required=True, default='0')
    quantity_done = fields.Float(string="完成数量", related="stock_move_id.quantity_done", default='0')
    location_id = fields.Many2one('stock.location', string='源位置', related="stock_move_id.location_id", required=True)

    move_line_ids = fields.One2many('stock.move.line.wizard', 'move_id', string='库存移动向导明细')
    stock_move_id = fields.Many2one('stock.move', string='库存移动')

    @api.multi
    def check_lines(self):
        self.ensure_one()
        # for move in self:
        # if move.stock_move_id.picking_id.state in ['draft','cancel','done'] \
        #         or move.stock_move_id.picking_id.picking_type_code == 'incoming':
        #     break
        quants = []
        for move_line in self.move_line_ids:
            if move_line.is_selected and (move_line.quantity_reserved_free > 0):
                quants += self.env['stock.quant']._update_reserved_quantity(
                    self.product_id, self.location_id, move_line.quantity_reserved_free,
                    lot_id=move_line.lot_id)

        if len(quants) > 0:
            for reserved_quant, quantity in quants:
                to_update = self.stock_move_id.move_line_ids.filtered(
                    lambda m: m.product_id.tracking != 'serial' and
                              m.location_id.id == reserved_quant.location_id.id and m.lot_id.id == reserved_quant.lot_id.id and m.package_id.id == reserved_quant.package_id.id and m.owner_id.id == reserved_quant.owner_id.id)
                if to_update:
                    to_update[0].with_context(
                        bypass_reservation_update=True).product_uom_qty += self.product_id.uom_id._compute_quantity(
                        quantity, to_update[0].product_uom_id, rounding_method='HALF-UP')
                else:
                    if self.product_id.tracking == 'serial':
                        for i in range(0, int(quantity)):
                            new_move_line = self.env['stock.move.line'].create(
                                self.stock_move_id._prepare_move_line_vals(quantity=1,
                                                                           reserved_quant=reserved_quant))
                    else:
                        new_move_line = self.env['stock.move.line'].create(
                            self.stock_move_id._prepare_move_line_vals(quantity=quantity,
                                                                       reserved_quant=reserved_quant))
            self.stock_move_id.is_manual_reserved = True
            self.stock_move_id.state = 'assigned'
        else:
            self.stock_move_id.move_line_ids.unlink()
            self.stock_move_id.is_manual_reserved = False
            self.stock_move_id.state = 'confirmed'
