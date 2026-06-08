from odoo import fields, models


class TourihaPassenger(models.Model):
    _inherit = "touriha.passenger"

    sale_order_id = fields.Many2one(
        "sale.order", string="Báo giá", ondelete="cascade", index=True
    )
