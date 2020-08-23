# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ApiModel(models.Model):
    _name = 'api.model'

    name = fields.Char(String='name')

    def echarts_data(self):
        return [
            {'name': '搜索引擎', 'value': 400}, {'name': '直接访问', 'value': 335}, {'name': '邮件营销', 'value': 310},
            {'name': '联盟广告', 'value': 274}, {'name': '视频广告', 'value': 235}, {'name': '朋友影响', 'value': 285}
        ]
