# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PropertyEstate(models.Model):
    _name = 'property.estate'
    _description = 'Property Estate Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name asc'

    name = fields.Char(string='Estate Name', required=True, index=True, tracking=True)
    rom_code = fields.Char(string='ROM Code', tracking=True) # 來自 "E-Housing PSAU version 2.xlsx - Estate Management.csv"
    dmo_code = fields.Char(string='DMO Code', tracking=True) # 來自 "E-Housing PSAU version 2.xlsx - Estate Management.csv"
    address = fields.Text(string='Address', tracking=True)

    # 關聯到座數/樓宇模型
    block_ids = fields.One2many('property.block', 'estate_id', string='Blocks/Buildings')
    block_count = fields.Integer(string='Block Count', compute='_compute_block_count', store=True)

    order_ids = fields.One2many('property.order', 'estate_id', string='Work Orders')
    order_count = fields.Integer(string='Order Count', compute='_compute_order_count', store=True)

    active = fields.Boolean(string='Active', default=True, help="Set active to false to hide the estate without removing it.")

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The Estate name must be unique!')
    ]

    @api.depends('order_ids')
    def _compute_order_count(self):
        for estate in self:
            estate.order_count = len(estate.order_ids)

    @api.depends('block_ids')
    def _compute_block_count(self):
        for estate in self:
            estate.block_count = len(estate.block_ids)

    def name_get(self):
        result = []
        for record in self:
            display_name = record.name
            if record.dmo_code:
                display_name = f"{record.name} ({record.dmo_code})"
            result.append((record.id, display_name))
        return result

    # 動作按鈕，用於打開關聯的樓宇列表
    def action_view_blocks(self):
        self.ensure_one()
        return {
            'name': ('Blocks/Buildings of %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'property.block',
            'view_mode': 'tree,form',
            'domain': [('estate_id', '=', self.id)],
            'context': {'default_estate_id': self.id}
        }

    _logger.info(">>>> Odoo 17: PropertyEstate model (with block relation) loaded!")