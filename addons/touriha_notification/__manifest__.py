{
    "name": "Touriha – Notification & Email",
    "version": "19.0.1.0.0",
    "summary": "Email tự động: xác nhận tour, gửi PO cho NCC, hoàn tiền, nhắc khởi hành",
    "category": "Services/Touriha",
    "author": "BSD Insight",
    "license": "LGPL-3",
    "website": "https://touriha.com",
    "support": "daibt@bsdinsight.com",
    "maintainer": "BSD Insight",
    "depends": ["touriha_costing", "touriha_cancellation"],
    "data": [
        "data/mail_templates.xml",
        "data/cron.xml",
    ],
    "application": False,
    "installable": True,
}
