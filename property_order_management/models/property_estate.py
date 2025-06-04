# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PropertyEstate(models.Model):
    _name = 'property.estate'
    _description = 'Property Estate Information'
    _order = 'name asc'

    name = fields.Char(string='Estate Name', required=True, index=True)
    rom_code = fields.Char(string='ROM Code')
    dmo_code = fields.Char(string='DMO Code')
    address = fields.Text(string='Address')
    order_ids = fields.One2many('property.order', 'estate_id', string='Work Orders')
    order_count = fields.Integer(string='Order Count', compute='_compute_order_count', store=True) # store=True 可以提高效能
    active = fields.Boolean(string='Active', default=True, help="Set active to false to hide the estate without removing it.")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The Estate name must be unique!')
    ]

    @api.depends('order_ids')
    def _compute_order_count(self):
        for estate in self:
            estate.order_count = len(estate.order_ids)

    def name_get(self):
        result = []
        for record in self:
            display_name = record.name
            if record.dmo_code:
                display_name = f"{record.name} ({record.dmo_code})"
            result.append((record.id, display_name))
        return result

    _logger.info(">>>> Odoo 17: PropertyEstate model class loaded!")