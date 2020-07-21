# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Product(models.Model):
    _inherit = 'product.product'

    quantity_unit = fields.Float(string='单位数量')


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    quantity_unit = fields.Float(string='单位数量',
                                 compute='_compute_quantity_unit', inverse='_set_quantity_unit', store=True)

    @api.depends('product_variant_ids', 'product_variant_ids.quantity_unit')
    def _compute_quantity_unit(self):
        unique_variants = self.filtered(lambda template: len(template.product_variant_ids) == 1)
        for template in unique_variants:
            template.quantity_unit = template.product_variant_ids.quantity_unit
        for template in (self - unique_variants):
            template.quantity_unit = 0.0

    @api.one
    def _set_quantity_unit(self):
        if len(self.product_variant_ids) == 1:
            self.product_variant_ids.quantity_unit = self.quantity_unit
