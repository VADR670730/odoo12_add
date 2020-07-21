# -*- coding: utf-8 -*-
import math

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime


class QuantPackage(models.Model):
    _name = 'stock.quant.package'
    _inherit = ['stock.quant.package', 'barcode.mixin']
