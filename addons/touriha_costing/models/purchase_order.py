from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    tour_id = fields.Many2one("touriha.tour", string="Tour", index=True, copy=False)
