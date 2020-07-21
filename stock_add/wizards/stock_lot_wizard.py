# -*- coding: utf-8 -*-
import math

from odoo import models, fields, api
from odoo.exceptions import UserError


class lot_wizard(models.TransientModel):
    _name = 'stock.lot.wizard'

    picking_id = fields.Many2one('stock.picking', string='调拨单')
    partner_id = fields.Many2one('res.partner', string='业务伙伴', related='picking_id.partner_id')
    picking_type_id = fields.Many2one('stock.picking.type', string='作业类型', related='picking_id.picking_type_id')
    scheduled_date = fields.Datetime(string='预定交货日期', related='picking_id.scheduled_date')
    lot_line_wizard_ids = fields.One2many('stock.lot.line.wizard', 'lot_wizard_id', string='自选批次/序列号明细')

    @api.multi
    def set_move_lines(self):
        self.ensure_one()
        for lot_line in self.lot_line_wizard_ids:
            move = lot_line.move_id
            move_lines = move.move_line_ids

            # 计算出有多少个单位，并保存每个单位的值到list
            unit_qty, rest_qty, quantity_unit = \
                [], lot_line.qty_done, lot_line.product_id.quantity_unit if lot_line.product_id.quantity_unit else 1
            while True:
                if rest_qty <= 0:
                    break
                unit_qty += [quantity_unit if rest_qty > quantity_unit else rest_qty]
                rest_qty -= quantity_unit
            # 根据需要创建的批次号数量，计算出每一个批次号的数量
            every_qty = [0 for i in range(0, lot_line.lot_qty)]
            for i in range(0, len(unit_qty)):
                every_qty[i % lot_line.lot_qty] += unit_qty[i]

            if lot_line.lot_qty != len(move_lines) and lot_line.lot_qty != 0:
                if lot_line.tracking == 'lot':
                    move_line_one = move_lines[0]
                    # 赋值
                    move_line_one.product_uom_qty = every_qty[0]
                    for i in range(1, len(move_lines)):
                        move_lines[i].picking_id = False
                        move_lines[i].move_id = False
                        move_lines[i].unlink()
                    for i in range(1, len(every_qty)):
                        self.env['stock.move.line'].create({
                            "picking_id": move_line_one.picking_id.id,
                            "move_id": move_line_one.move_id.id,
                            "product_id": move_line_one.product_id.id,
                            "package_level_id": move_line_one.package_level_id.id,
                            "location_id": move_line_one.location_id.id,
                            "location_dest_id": move_line_one.location_dest_id.id,
                            "package_id": move_line_one.package_id.id,
                            "result_package_id": move_line_one.result_package_id.id,
                            "owner_id": move_line_one.owner_id.id,
                            "product_uom_qty": every_qty[i],
                            "product_uom_id": move_line_one.product_uom_id.id,
                        })
                elif lot_line.tracking == 'serial':
                    move_line_one = move_lines[0]
                    if lot_line.lot_qty < len(move_lines):
                        for i in range(lot_line.lot_qty, len(move_lines)):
                            move_lines[i].picking_id = False
                            move_lines[i].move_id = False
                            move_lines[i].unlink()
                    if lot_line.lot_qty > len(move_lines):
                        for i in range(len(move_lines), lot_line.lot_qty):
                            self.env['stock.move.line'].create({
                                "picking_id": move_line_one.picking_id.id,
                                "move_id": move_line_one.move_id.id,
                                "product_id": move_line_one.product_id.id,
                                "package_level_id": move_line_one.package_level_id.id,
                                "location_id": move_line_one.location_id.id,
                                "location_dest_id": move_line_one.location_dest_id.id,
                                "package_id": move_line_one.package_id.id,
                                "result_package_id": move_line_one.result_package_id.id,
                                "owner_id": move_line_one.owner_id.id,
                                "product_uom_qty": move_line_one.product_uom_qty,
                                "product_uom_id": move_line_one.product_uom_id.id,
                            })
                self.picking_id.batch_finish()  # 批量完成
            else:
                if lot_line.tracking == 'lot':
                    for i in range(0, len(move_lines)):
                        move_lines[i].qty_done = every_qty[i]
                elif lot_line.tracking == 'serial':
                    for i in range(0, len(move_lines)):
                        move_lines[i].qty_done = 1

        lots = self.picking_id.create_lots()
