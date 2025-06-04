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
        ('05', 'Create'),
        ('10', 'Submit'),
        ('30', 'SO Support'),
        ('35', 'AO Reject'),
        ('45', 'Work Order Issue'),
        ('50', 'Cont. Acknowledge'),
        ('55', 'In Progress'),
        ('60', 'Completion'),
        ('75', 'Certified Awaiting Claim'),
        ('78', 'Payment Claim Created'),
        ('85', 'Final Pay Completed'),
        ('86', 'Zero Final Payment'),
    ], string='Status', default='05', required=True, tracking=True, copy=False,
       group_expand='_read_group_status_ids')

    remarks = fields.Text(string='Remarks', tracking=True)
    estate_id = fields.Many2one('property.estate', string='Estate', required=True, tracking=True, ondelete='restrict', index=True)
    contractor_id = fields.Many2one(
        'res.partner', string='Contractor', tracking=True,
        domain="[('is_company', '=', True), ('is_contractor', '=', True)]"
    )
    oev_amount = fields.Float(string='OEV ($)', tracking=True) #
    color = fields.Integer(string='Color Index')

    # --- 新增欄位 ---
    # 參考 "E-Housing PSAU version 2.xlsx - Order > Create.csv"
    work_type = fields.Char(string='Work Type') # 假設為 Char，您可以根據實際情況改為 Selection
    project_no = fields.Char(string='Project No.')
    budget_year = fields.Char(string='Budget Year')
    initiator = fields.Many2one('res.users', string='Initiator', default=lambda self: self.env.user, tracking=True) # 預設為當前使用者
    contact_person = fields.Char(string='Contact Person')
    contact_tel_no = fields.Char(string='Contact Tel. No.')
    # target_completion_date = fields.Date(string='Target Completion Date') # 您可以根據需要添加
    # basic_start_date = fields.Date(string='Basic Start Date') # 用於自動化狀態
    # basic_fin_date = fields.Date(string='Basic Fin. Date') # 用於自動化狀態和逾期付款計算

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', ('New')) == ('New'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('property.order.sequence') or ('New')
            if not vals.get('status'): # 確保新訂單的初始狀態是 '05'
                vals['status'] = '05'
        return super(PropertyOrder, self).create(vals_list)

    @api.model
    def _read_group_status_ids(self, stages, domain, order):
        return [key for key, _ in self._fields['status'].selection]

    # --- 狀態流轉按鈕方法 (根據需要擴展) ---
    def action_submit(self):
        self.write({'status': '10'})

    def action_so_support(self):
        self.write({'status': '30'})

    def action_ao_reject(self):
        self.write({'status': '35'})
        
    def action_issue_work_order(self): # 假設 HA AC 批准
        self.write({'status': '45'})

    def action_contractor_acknowledge(self):
        self.write({'status': '50'})
        
    def action_set_in_progress(self):
        self.write({'status': '55'})

    def action_set_completion(self): # 先到 60
        self.write({'status': '60'})
    
    # ... 您可以為 75, 78, 85, 86 等狀態添加更多方法 ...

    _logger.info(">>>> Odoo 17: PropertyOrder model (with more fields and statuses) loaded by Python!")