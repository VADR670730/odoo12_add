# -*- coding: utf-8 -*-
from odoo import http
import json


class Test(http.Controller):
    @http.route('/echartsData/', auth='public')
    def index(self, **kw):
        echartsData = [{"name": "搜索引擎", "value": 365}, {"name": "直接访问", "value": 335},
                       {"name": "邮件营销", "value": 310}, {"name": "联盟广告", "value": 274},
                       {"name": "视频广告", "value": 235}, {"name": "朋友影响", "value": 285}]
        return json.dumps(echartsData)
