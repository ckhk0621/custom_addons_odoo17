# -*- coding: utf-8 -*-
{
    'name': 'Property Management System (Odoo 17)',  # 模組在 Odoo 界面顯示的名稱
    'version': '17.0.1.0.0',  # 模組版本 (Odoo 17.0，第1個主要版，第0個次要版，第0個修補程式版)
    'summary': 'A comprehensive system for managing property-related operations including estates, contractors, and work orders.', # 模組摘要
    'description': """
Property Management System
==========================
This module aims to provide functionalities for:
- Estate Management (Managing property estates, ROM, DMO structures)
- Contractor Management (Managing contractors or service providers)
- Work Order Management (Creating and tracking work orders related to properties)
- Basic Reporting (Future goal)
    """,  # 更詳細的描述
    'author': 'CK Lam',  # 您的名字或公司名
    'website': 'https://ideastime.ltd',  # 您的網站
    'category': 'Services/Property Management',  # 模組分類，更精確一些
    'depends': [
        'base',  # 所有模組的基礎
        'mail',  # 用於消息追蹤、活動、chatter 功能
        # 'contacts', # 雖然 res.partner 屬於 base，但如果明確用到 contacts app 的特定功能，可以加上
    ],
    'data': [
        # 1. 安全性檔案 (設定模型的存取權限)
        'security/ir.model.access.csv',

        # 2. 資料檔案 (例如序列號定義、預設數據等)
        'data/property_order_sequence.xml', # 用於訂單編號
        # 'data/property_estate_data.xml', # (可選) 如果有屋苑的預設或演示數據

        # 3. 視圖檔案 (定義模型的界面)
        'views/property_estate_views.xml',    # 屋苑管理的視圖和動作
        # 'views/property_contractor_views.xml',# (如果決定不只用 res.partner，或者需要特定視圖)
        'views/property_order_views.xml',     # 訂單管理的視圖和動作
        
        # 4. 選單檔案 (定義使用者如何導航到這些功能)
        'views/property_menus.xml',           # 主選單和各個功能的選單項目 (建議整合)
    ],
    'demo': [
        # 'demo/property_demo_data.xml', # (可選) 如果您想添加演示數據
    ],
    'installable': True,
    'application': True,  # 設定為 True，使其在應用程式列表中作為一個主要應用顯示
    'auto_install': False,
    'license': 'LGPL-3', # 或其他您選擇的開源協議
    'icon': '/property_order_management/static/description/icon.png', # (可選) 模組圖示路徑
}