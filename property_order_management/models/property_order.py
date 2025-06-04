# -*- coding: utf-8 -*-
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class PropertyOrder(models.Model):
    _name = 'property.order'
    _description = 'Property Work Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'issue_date desc, reference desc' # 按發出日期降序，然後按參考編號降序

    name = fields.Char(string='Order Description', required=True, tracking=True)
    reference = fields.Char(string='Order Reference', required=True, copy=False, readonly=True, default=lambda self: ('New'), index=True, tracking=True)
    issue_date = fields.Date(string='Issue Date', default=fields.Date.today, required=True, tracking=True)
    
    status = fields.Selection([
        ('10', 'Submit'),        # 參照 "Full function list v2.pdf" 和 "WhatsApp Business Function List.docx"
        ('55', 'In Progress'),   # 參照 "Full function list v2.pdf" 和 "WhatsApp Business Function List.docx"
        ('60', 'Completion'),    # 參照 "Full function list v2.pdf" 和 "WhatsApp Business Function List.docx"
        # 之後您可以根據 "Full function list v2.pdf" 中的完整狀態列表逐步添加其他狀態
        # 例如： ('05', 'Create'), ('30', 'SO Support'), ('35', 'AO Reject'), 等等
    ], string='Status', default='10', required=True, tracking=True, copy=False,
       group_expand='_read_group_status_ids') # group_expand 用於看板視圖

    remarks = fields.Text(string='Remarks', tracking=True)

    # Methods to handle status changes
    def action_submit(self):
        return self.write({'status': '10'})

    def action_in_progress(self):
        return self.write({'status': '55'})

    def action_complete(self):
        return self.write({'status': '60'})

    # 關聯到屋苑模型
    estate_id = fields.Many2one('property.estate', string='Estate', required=True, tracking=True, ondelete='restrict', index=True)
    # 關聯到承辦商 (res.partner 模型)
    contractor_id = fields.Many2one(
    'res.partner', string='Contractor', tracking=True,
        domain="[('is_company', '=', True), ('is_contractor', '=', True)]" # <--- 修改這裡
        # 或者如果您不強制承辦商必須是公司類型，可以簡化為：
        # domain="[('is_contractor', '=', True)]"
    )
        
    # 來自 "Full function list v2.pdf" 或 "WhatsApp Business Function List.docx" 的 OEV $
    oev_amount = fields.Float(string='OEV ($)', tracking=True)

    # 為了看板視圖的顏色標記 (可選)
    color = fields.Integer(string='Color Index') 

    # --- 您可以根據 "E-Housing PSAU version 2.xlsx - Order > Create.csv" 添加更多欄位 ---
    # 例如：
    # order_type = fields.Selection([...], string='Order Type')
    # priority = fields.Selection([...], string='Priority')
    # reported_by = fields.Char(string='Reported By')
    # contact_phone = fields.Char(string='Contact Phone')
    # target_completion_date = fields.Date(string='Target Completion Date')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', ('New')) == ('New'):
                # 確保序列號 'property.order.sequence' 已在 data XML 檔案中定義
                vals['reference'] = self.env['ir.sequence'].next_by_code('property.order.sequence') or ('New')
        return super(PropertyOrder, self).create(vals_list)

    @api.model
    def _read_group_status_ids(self, stages, domain, order): # stages, domain, order 是 Odoo 傳遞的參數
        """
        這個方法被 status 欄位的 group_expand 屬性調用。
        它用於確保看板視圖能夠顯示所有定義的狀態列，即使某些狀態下沒有記錄。
        返回的是 status 欄位 selection 選項中的 keys 列表。
        """
        # 直接返回 status 欄位定義的所有 selection keys
        # 這能確保看板視圖總是嘗試為每個定義的狀態創建一個列
        if 'status' in self._fields: # 確保 status 欄位已定義
             return [key for key, _ in self._fields['status'].selection]
        return []

    _logger.info(">>>> Odoo 17: PropertyOrder model class (with status handling) loaded by Python!")