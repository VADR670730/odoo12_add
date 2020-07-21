# -*- coding: utf-8 -*-

import math
from odoo import models, api
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    # 创建批次/序列号按钮
    @api.multi
    def button_create_lots(self):
        self.ensure_one()
        if self.state != 'assigned' or self.picking_type_code != 'incoming':
            return

        lot_wizard = self.env['stock.lot.wizard'].create({
            'picking_id': self.id,
        })

        is_lots = False
        for stock_move in self.move_ids_without_package:
            tracking = stock_move.product_id.product_tmpl_id.tracking
            if tracking == 'none':
                continue

            is_lots = True
            if tracking == 'serial':
                lot_qty = stock_move.quantity_done
            else:
                lot_qty = 1 if not stock_move.product_id.quantity_unit \
                    else math.ceil(stock_move.quantity_done / stock_move.product_id.quantity_unit)
            self.env['stock.lot.line.wizard'].create({
                'qty_done': stock_move.quantity_done,
                'move_id': stock_move.id,
                'lot_qty': lot_qty,
                'lot_wizard_id': lot_wizard.id
            })

        if not is_lots:
            raise UserError('该调拨单没有需要创建的序列/批次号。')

        action = {
            'type': 'ir.actions.act_window',
            'name': '设置序列/批次号数量',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.lot.wizard',
            'target': 'new',
            'res_id': lot_wizard.id,
        }
        return action

    # 创建批次/序列号
    @api.multi
    def create_lots(self):
        self.ensure_one()
        if self.state != 'assigned' or self.picking_type_code != 'incoming':
            return False

        lot_ids = []
        # stock_move_line
        for stock_move_line in self.move_line_ids_without_package:
            # stock_move_line.product_id.tracking: lot、serial、none
            if stock_move_line.product_id.tracking == 'none':
                continue
            if stock_move_line.lot_id:
                lot_ids.append(stock_move_line.lot_id.id)
                continue

            lot = {
                'product_id': stock_move_line.product_id.id,
                'product_uom_id': stock_move_line.product_uom_id.id,
            }
            new_lot = self.env["stock.production.lot"].create(lot)
            # 将stock_move_line指定其序列号
            stock_move_line.write({'lot_id': new_lot.id})
            stock_move_line.write({'lot_name': new_lot.name})
            lot_ids.append(new_lot.id)
        return lot_ids

    # 批量完成
    @api.multi
    def batch_finish(self):
        for item in self:
            if item.state in ['done', 'cancel']:
                continue
            move_lines = item.move_line_ids_without_package
            for move_line in move_lines:
                move_line.qty_done = move_line.product_uom_qty

    # 取消验证
    @api.multi
    def back_validate(self):
        self.ensure_one()
        for move in self.move_lines:
            move.state = 'draft'
        if self.location_id == self.location_dest_id:
            for move_line in self.move_line_ids:
                move_line.unlink()
            return
        for move_line in self.move_line_ids:
            quants = move_line.lot_id.quant_ids if move_line.product_id.product_tmpl_id.tracking != 'none' \
                else self.env['stock.quant'].sudo().search([('product_id', '=', move_line.product_id.id)])
            for quant in quants:
                if quant.location_id == self.location_id:  # 源位置
                    quant.sudo().write({
                        'quantity': quant.quantity + move_line.qty_done
                    })
                elif quant.location_id == self.location_dest_id:  # 目的位置
                    if quant.quantity - quant.reserved_quantity < move_line.qty_done:
                        raise UserError('产品\"' + quant.product_id.product_tmpl_id.name + '\"已在别处锁库或移库!')
                    quant.sudo().write({
                        'quantity': quant.quantity - move_line.qty_done
                    })
                if quant.quantity == 0:
                    quant.sudo().unlink()
            move_line.unlink()
