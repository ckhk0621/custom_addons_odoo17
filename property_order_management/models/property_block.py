# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PropertyBlock(models.Model):
    _name = 'property.block'
    _description = 'Property Block/Building'
    _order = 'name'

    name = fields.Char(string='Block/Building Name', required=True)
    # 關聯回屋苑
    estate_id = fields.Many2one('property.estate', string='Estate', required=True, ondelete='cascade', index=True)

    # 您可以根據 "E-Housing PSAU version 2.xlsx - Estate Management.csv" Part 2 的欄位添加更多
    # 例如：
    # building_type = fields.Char(string='Building Type')
    # completion_year = fields.Integer(string='Year of Completion')
    # number_of_lifts = fields.Integer(string='Number of Lifts') # 用於電梯故障率計算

    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_estate_uniq', 'unique (name, estate_id)', 'The Block/Building name must be unique per estate!')
    ]

    _logger.info(">>>> Odoo 17: PropertyBlock model loaded by Python!")