# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Material(models.Model):
    _name = 'material'
    _description = '物料'

    name = fields.Char(string='名称', required=True)
    type_id = fields.Many2one(comodel_name='material.type', string='分类', domain=[('parent_type_id', '=', None)],
                              required=True)
    unit_id = fields.Many2one(comodel_name='unit', string='单位', domain=[('parent_unit_id', '=', None)], required=True)
    price = fields.Float(string='价格')
    value_x = fields.Float(string='value_x')
    value_y = fields.Float(string='value_y')
    value_z = fields.Float(string='value_z', compute='compute_z')

    @api.depends('value_x', 'value_y')
    def compute_z(self):
        for item in self:
            item.value_z = item.value_x * item.value_y


class MaterialType(models.Model):
    _name = 'material.type'
    _description = '物料分类'

    name = fields.Char(string='名称', required=True)
    parent_type_id = fields.Many2one(comodel_name='material.type', string='上级分类')
    child_type_ids = fields.One2many(comodel_name='material.type', inverse_name='parent_type_id', string='下级分类')


class Unit(models.Model):
    _name = 'unit'
    _description = '单位'

    name = fields.Char(string='名称', required=True)
    type = fields.Selection(selection=[
        ('unit', '单位'),
        ('weight', '重量'),
        ('time', '时间'),
        ('length', '长度'),
        ('volume', '体积'),
        ('area', '面积'),
    ], string='计量类型')
