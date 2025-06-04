# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PropertyOrder(models.Model):
    _name = 'property.order'
    _description = 'Property Work Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'issue_date desc, reference desc'

    name = fields.Char(string='Order Description', required=True, tracking=True)
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self: ('New'), index=True, tracking=True)
    issue_date = fields.Date(string='Issue Date', default=fields.Date.today, required=True, tracking=True)

    status = fields.Selection([
        ('10', 'Submit'),
        ('55', 'In Progress'),
        ('60', 'Completion'),
    ], string='Status', default='10', required=True, tracking=True, copy=False,
       group_expand='_read_group_status_ids')

    remarks = fields.Text(string='Remarks', tracking=True)
    estate_id = fields.Many2one('property.estate', string='Estate', required=True, tracking=True, ondelete='restrict', index=True)
    contractor_id = fields.Many2one(
        'res.partner', string='Contractor', tracking=True,
        domain="[('is_company', '=', True)]" 
        # 之後可以為 res.partner 添加 is_contractor 欄位並用 domain="[('is_contractor', '=', True)]"
    )
    oev_amount = fields.Float(string='OEV ($)', tracking=True)
    color = fields.Integer(string='Color Index') 
    # 用於看板顏色

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', ('New')) == ('New'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('property.order.sequence') or ('New')
        return super(PropertyOrder, self).create(vals_list)

    @api.model
    def _read_group_status_ids(self, stages_from_group_by, domain, order): # 修改參數名以示區分
        # stages_from_group_by: Odoo read_group 傳遞過來的，基於 groupby 欄位的現有值
        # domain: 當前 read_group 的 domain
        # order: 當前 read_group 的 order

        # 我們希望看板列總是顯示我們定義的這幾個狀態，即使某個狀態下沒有記錄
        defined_status_keys = ['10', '55', '60'] 

        # 從 self._fields['status'].selection 中獲取 (key, label) 對
        # selection_options = dict(self._fields['status'].selection)
        # return [(key, selection_options[key]) for key in defined_status_keys if key in selection_options]
        # 更簡單的方式，如果只是為了顯示這些 key:
        return self.env[self._name].browse(self.env[self._name].search(domain).ids)

    _logger.info(">>>> Odoo 17: PropertyOrder model class loaded!")