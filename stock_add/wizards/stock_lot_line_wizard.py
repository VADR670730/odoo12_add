# -*- coding: utf-8 -*-
import math
from odoo import models, fields, api


class lot_line_wizard(models.TransientModel):
    _name = 'stock.lot.line.wizard'

    move_id = fields.Many2one('stock.move', string='库存移动')
    product_id = fields.Many2one('product.product', string='产品', related='move_id.product_id')
    product_uom = fields.Many2one('uom.uom', string='单位', related='move_id.product_uom')
    tracking = fields.Selection([
        ('serial', 'By Unique Serial Number'),
        ('lot', 'By Lots'),
        ('none', 'No Tracking')], string="跟踪", related='product_id.product_tmpl_id.tracking')
    qty_uom = fields.Float(string='需求数量', related='move_id.product_uom_qty')
    qty_done = fields.Float(string='完成数量')
    lot_qty = fields.Integer(string='生成批次/序列号数量')
    lot_wizard_id = fields.Many2one('stock.lot.wizard', string='自选批次/序列号')

    @api.onchange('qty_done')
    def qty_done_change(self):
        for line in self:
            tracking = line.product_id.product_tmpl_id.tracking
            if tracking == 'serial':
                lot_qty = line.qty_done
            else:
                lot_qty = 1 if not line.product_id.quantity_unit \
                    else math.ceil(line.qty_done / line.product_id.quantity_unit)
            line.lot_qty = lot_qty

    @api.onchange('lot_qty')
    def lot_qty_change(self):
        for line in self:
            tracking = line.product_id.product_tmpl_id.tracking
            if tracking == 'serial':
                line.lot_qty = line.qty_done
