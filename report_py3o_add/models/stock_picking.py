# -*- coding: utf-8 -*-

import math
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def print_lots(self):
        self.ensure_one()
        lots = []
        for stock_move_line in self.move_line_ids_without_package:
            if stock_move_line.lot_id:
                lots.append(stock_move_line.lot_id.id)
        if not len(lots):
            raise UserError('请先创建序列/批次号！')
        return self.env.ref('report_py3o_add.action_report_stock_production_lot'). \
            report_action(docids=lots)
