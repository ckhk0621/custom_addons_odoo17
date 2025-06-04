# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_contractor = fields.Boolean(string='Is a Contractor', default=False,
                                  help="Check this box if this contact is a contractor.")
    # 您可以根據 "E-Housing PSAU version 2.xlsx - Contractor Management.csv"
    # 在這裡添加更多承辦商特定的欄位，例如：
    # contractor_type = fields.Selection([...], string='Contractor Type')
    # service_scope = fields.Text(string='Service Scope')