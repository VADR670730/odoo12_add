# -*- coding: utf-8 -*-

from odoo import models, fields, api


class move_line_wizard(models.TransientModel):
    _name = 'stock.move.line.wizard'

    is_selected = fields.Boolean(string='选择')
    quant_id = fields.Many2one('stock.quant', string='在手库存', readonly=True, required=True, ondelete='cascade')
    lot_id = fields.Many2one('stock.production.lot', string='批次/序列号码', related="quant_id.lot_id")
    quantity_reserved_free = fields.Float(string="保留数量", default='0')
    quantity_reserved = fields.Float(string="已保留数量", related="quant_id.reserved_quantity", default='0', readonly=True)
    quantity_done = fields.Float(string="库存数量", related="quant_id.quantity", default='0', readonly=True)
    quantity_yx = fields.Float(string="有效数量", default='0', readonly=True, compute="compute_yx")
    move_id = fields.Many2one('stock.move.wizard', string='库存移动向导')

    @api.depends('quantity_done', 'quantity_reserved')
    def compute_yx(self):
        for line in self:
            line.quantity_yx = line.quantity_done - line.quantity_reserved

    @api.onchange('is_selected')
    def change_selected(self):
        for line in self:
            if not line.is_selected:
                line.quantity_reserved_free = 0
            else:
                line.quantity_reserved_free = 1

    @api.onchange('quantity_reserved_free')
    def change_reserved_free(self):
        for line in self:
            if not line.is_selected:
                line.quantity_reserved_free = 0
            if line.quantity_reserved_free > line.quantity_yx:
                line.quantity_reserved_free = line.quantity_yx
            if line.quantity_reserved_free < 0:
                line.quantity_reserved_free = 0
