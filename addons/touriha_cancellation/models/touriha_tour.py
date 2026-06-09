from odoo import _, models


class TourihaTour(models.Model):
    _inherit = "touriha.tour"

    def action_open_cancellation(self):
        self.ensure_one()
        Req = self.env["touriha.cancellation.request"]
        existing = Req.search(
            [("tour_id", "=", self.id), ("state", "!=", "rejected")], limit=1
        )
        ctx = {"default_tour_id": self.id}
        # nếu có touriha_crm, lấy sẵn tổng tiền từ báo giá
        if "sale_order_id" in self._fields and self.sale_order_id:
            ctx["default_total_amount"] = self.sale_order_id.amount_total
        action = {
            "type": "ir.actions.act_window",
            "name": _("Yêu cầu hủy tour"),
            "res_model": "touriha.cancellation.request",
            "view_mode": "form",
            "target": "current",
            "context": ctx,
        }
        if existing:
            action["res_id"] = existing.id
        return action
