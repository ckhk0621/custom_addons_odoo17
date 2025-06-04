# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PropertyEstate(models.Model):
    _name = 'property.estate'
    _description = 'Property Estate'
    _order = 'name'

    name = fields.Char(string='Estate Name', required=True, index=True)
    rom_code = fields.Char(string='ROM Code')
    dmo_code = fields.Char(string='DMO Code')
    active = fields.Boolean(string='Active', default=True)

    # 為了在下拉選單中更好看，可以定義一個 name_get 方法
    # (Odoo 16+ 預設的 name_get 行為通常已經很好，除非有特殊需求)
    # def name_get(self):
    #     result = []
    #     for record in self:
    #         name = record.name
    #         if record.rom_code:
    #             name = f"[{record.rom_code}] {name}" # Python 3.6+ f-string
    #         result.append((record.id, name))
    #     return result

    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'The Estate name must be unique!')
    ]