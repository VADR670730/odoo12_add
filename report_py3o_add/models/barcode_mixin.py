# -*- coding: utf-8 -*-

import base64
from odoo import api, fields, models
from odoo.exceptions import UserError


class BarcodeMixin(models.AbstractModel):
    _name = 'barcode.mixin'
    _description = '条码输出接口'

    @api.multi
    def get_barcode_content(self, attr_name, code_type, width, height):
        """
        获取字符串二维码
        :param attr_name:
        :param code_type:
        :param width:
        :param height:
        :return:
        """
        if not hasattr(self, attr_name):
            raise UserError('属性字段 %s 不存在!' % attr_name)

        content = getattr(self, attr_name, 'N/A')
        barcode = self.env['ir.actions.report'].barcode(code_type, content, width=width, height=height,
                                                        humanreadable=True)
        return base64.b64encode(barcode).decode('ascii')

    @api.multi
    def get_fixed_barcode(self, code, code_type, width, height):
        barcode = self.env['ir.actions.report'].barcode(code_type, code, width=width, height=height,
                                                        humanreadable=True)
        return base64.b64encode(barcode).decode('ascii')
