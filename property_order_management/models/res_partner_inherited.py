# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartnerInherited(models.Model):
    _inherit = 'res.partner'  # 繼承現有的 res.partner 模型

    is_contractor = fields.Boolean(string='Is a Contractor', default=False,
                                    help="Check this box if this contact is a contractor/service provider.")
    # 您可以根據需要為承辦商添加更多特定欄位，例如：
    # contractor_type = fields.Selection([...], string='Contractor Type')
    # contractor_specialization = fields.Char(string='Specialization')