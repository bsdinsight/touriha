{
    "name": "Touriha – Costing & Mua dịch vụ",
    "version": "19.0.1.0.0",
    "summary": "Costing 3 giai đoạn (dự kiến/chốt/thực tế) + tạo PO theo nhà cung cấp",
    "category": "Services/Touriha",
    "author": "BSD Insight",
    "license": "LGPL-3",
    "website": "https://touriha.com",
    "support": "daibt@bsdinsight.com",
    "maintainer": "BSD Insight",
    "depends": ["touriha_operations", "purchase"],
    "data": [
        "security/ir.model.access.csv",
        "views/touriha_costing_views.xml",
        "views/purchase_order_views.xml",
    ],
    "application": False,
    "installable": True,
}
