# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class MrpWorkorder(models.Model):
    _inherit = 'mrp.workorder'

    @api.multi
    def batch_provide_lots(self):
        self.ensure_one()
        reserved_lots = []  # 对应生产单上已保留的 产品和批/序号
        for move in self.production_id.move_raw_ids:
            for move_line in move.move_line_ids:
                if move_line.lot_id:
                    reserved_lots.append([move_line.product_id, move_line.lot_id, False])
        for move_line in self.active_move_line_ids:
            if not move_line.lot_id:
                for lot in reserved_lots:
                    if (not lot[2]) and lot[0] == move_line.product_id:
                        move_line.lot_id = lot[1]
                        lot[2] = True
                        break
