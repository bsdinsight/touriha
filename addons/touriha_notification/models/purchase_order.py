from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    touriha_po_mail_sent = fields.Boolean("Đã gửi email NCC", copy=False)
