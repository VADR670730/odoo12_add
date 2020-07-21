# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Echarts(models.Model):
    _name = 'test.echarts'

    name = fields.Char(string='名称')
    type = fields.Selection([('pie', '饼状图'), ('bar', '柱状图')], string='类型')
    a = fields.Char(string='AAA')
    b = fields.Char(string='BBB')
    c = fields.Char(string='CCC')
    d = fields.Char(string='DDD')
    e = fields.Char(string='EEE')
    f = fields.Char(string='FFF')
    g = fields.Char(string='GGG')
    h = fields.Char(string='HHH')
    i = fields.Char(string='III')
    j = fields.Char(string='JJJ')
    k = fields.Char(string='KKK')
    l = fields.Char(string='LLL')
    m = fields.Char(string='MMM')
    n = fields.Char(string='NNN')
    o = fields.Char(string='OOO')
    p = fields.Char(string='PPP')
    q = fields.Char(string='QQQ')
    r = fields.Char(string='RRR')
    s = fields.Char(string='SSS')
    t = fields.Char(string='TTT')
    u = fields.Char(string='UUU')
    v = fields.Char(string='VVV')
    w = fields.Char(string='WWW')
    x = fields.Char(string='XXX')
    y = fields.Char(string='YYY')
    z = fields.Char(string='ZZZ')
