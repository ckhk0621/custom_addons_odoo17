# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PropertyOrder(models.Model):
    _name = 'property.order'
    _description = 'Property Work Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Order Description', required=True, tracking=True)
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self: ('New'), tracking=True)
    issue_date = fields.Date(string='Issue Date', default=fields.Date.today, tracking=True)

    status = fields.Selection([
        ('10', 'Submit'),
        ('55', 'In Progress'),
        ('60', 'Completion'),
    ], string='Status', default='10', required=True, tracking=True, 
       group_expand='_read_group_status_ids')

    remarks = fields.Text(string='Remarks', tracking=True)

    # 關聯到屋苑模型
    estate_id = fields.Many2one('property.estate', string='Estate', tracking=True)
    # 關聯到承辦商 (res.partner 模型)
    # 我們可以稍後再為 res.partner 添加 is_contractor 欄位，並在這裡加上 domain
    contractor_id = fields.Many2one('res.partner', string='Contractor', tracking=True, domain="[('is_company', '=', True)]")


    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', ('New')) == ('New'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('property.order.sequence') or ('New')
        return super(PropertyOrder, self).create(vals_list)

    @api.model
    def _read_group_status_ids(self, stages, domain, order):
        # 返回 status 欄位的所有 selection keys 的一種方式
        # field_status_selection = self.env[self._name].fields_get(['status'])['status']['selection']
        # if field_status_selection:
        #    return [key for key, _ in field_status_selection]
        # 或者，如果您想按特定順序，並且確定這些 key 存在於 selection 中：
        return ['10', '55', '60']

    _logger.info(">>>> Odoo 17: PropertyOrder model class loaded by Python!")