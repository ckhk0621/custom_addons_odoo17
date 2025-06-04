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

    # Fields based on "E-Housing PSAU version 2.xlsx - Estate Management.csv" Part 2
    building_type = fields.Char(string='Building Type')
    completion_year = fields.Char(string='Year of Completion', size=4)
    number_of_lifts = fields.Integer(string='Number of Lifts')

    active = fields.Boolean(string='Active', default=True)

    _sql_constraints = [
        ('name_estate_uniq', 'unique (name, estate_id)', 'The Block/Building name must be unique per estate!')
    ]

    @api.onchange('completion_year')
    def _onchange_completion_year(self):
        if self.completion_year:
            # Remove any non-digit characters
            year = ''.join(filter(str.isdigit, self.completion_year))
            # Ensure it's exactly 4 digits
            if len(year) > 4:
                year = year[:4]
            elif len(year) < 4:
                year = year.zfill(4)
            self.completion_year = year

    _logger.info(">>>> Odoo 17: PropertyBlock model loaded!")