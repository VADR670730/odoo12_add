# -*- coding: utf-8 -*-
import math

from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime


class ProductionLot(models.Model):
    _name = 'stock.production.lot'
    _inherit = ['stock.production.lot', 'barcode.mixin']
