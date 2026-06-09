{
    "name": "Touriha – Hủy tour & Hoàn tiền",
    "version": "19.0.1.0.0",
    "summary": "Chính sách phí hủy theo ngày + yêu cầu hủy & hoàn tiền",
    "category": "Services/Touriha",
    "author": "BSD Insight",
    "license": "LGPL-3",
    "website": "https://touriha.com",
    "support": "daibt@bsdinsight.com",
    "maintainer": "BSD Insight",
    "depends": ["touriha_operations"],
    "data": [
        "security/ir.model.access.csv",
        "data/cancellation_policy_data.xml",
        "views/touriha_cancellation_views.xml",
    ],
    "application": False,
    "installable": True,
}
