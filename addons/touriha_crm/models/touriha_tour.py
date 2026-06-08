from odoo import fields, models


class TourihaTour(models.Model):
    _inherit = "touriha.tour"

    sale_order_id = fields.Many2one(
        "sale.order", string="Báo giá nguồn", copy=False, readonly=True
    )

    def action_view_sale_order(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "sale.order",
            "res_id": self.sale_order_id.id,
            "view_mode": "form",
            "target": "current",
        }
