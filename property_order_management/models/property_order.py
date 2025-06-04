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
    oev_amount = fields.Float(string='OEV ($)', tracking=True)
    color = fields.Integer(string='Color Index')

    # --- Fields ---
    work_type = fields.Char(string='Work Type')
    project_no = fields.Char(string='Project No.')
    budget_amount = fields.Float(string='Budget Amount ($)', tracking=True)
    fiscal_year = fields.Char(string='Fiscal Year', size=4, tracking=True)
    initiator = fields.Many2one('res.users', string='Initiator', default=lambda self: self.env.user, tracking=True)
    contact_person = fields.Char(string='Contact Person')
    contact_tel_no = fields.Char(string='Contact Tel. No.')

    @api.onchange('fiscal_year')
    def _onchange_fiscal_year(self):
        if self.fiscal_year:
            # Remove any non-digit characters
            year = ''.join(filter(str.isdigit, self.fiscal_year))
            # Ensure it's exactly 4 digits
            if len(year) > 4:
                year = year[:4]
            elif len(year) < 4:
                year = year.zfill(4)
            self.fiscal_year = year

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('reference', ('New')) == ('New'):
                vals['reference'] = self.env['ir.sequence'].next_by_code('property.order.sequence') or ('New')
            if not vals.get('status'):
                vals['status'] = '05'
            # Format fiscal_year on creation
            if fiscal_year := vals.get('fiscal_year'):
                year = ''.join(filter(str.isdigit, fiscal_year))
                if len(year) > 4:
                    year = year[:4]
                elif len(year) < 4:
                    year = year.zfill(4)
                vals['fiscal_year'] = year
        return super(PropertyOrder, self).create(vals_list)

    @api.model
    def _read_group_status_ids(self, stages, domain, order):
        return [key for key, _ in self._fields['status'].selection]

    # --- Status transition methods ---
    def action_submit(self):
        self.write({'status': '10'})

    def action_so_support(self):
        self.write({'status': '30'})

    def action_ao_reject(self):
        self.write({'status': '35'})
        
    def action_issue_work_order(self):
        self.write({'status': '45'})

    def action_contractor_acknowledge(self):
        self.write({'status': '50'})
        
    def action_set_in_progress(self):
        self.write({'status': '55'})

    def action_set_completion(self):
        self.write({'status': '60'})

    _logger.info(">>>> Odoo 17: PropertyOrder model (with more fields and statuses) loaded by Python!")