from odoo import _, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    rejection_reason = fields.Text("Lý do từ chối (NCC)", copy=False)

    def action_portal_accept(self):
        for po in self:
            if po.state in ("draft", "sent"):
                po.button_confirm()
                po.message_post(body=_("Nhà cung cấp đã CHẤP NHẬN PO qua portal."))
                po._touriha_notify_operation(
                    _("Nhà cung cấp %s đã chấp nhận PO %s.")
                    % (po.partner_id.name, po.name)
                )
        return True

    def action_portal_reject(self, reason=None):
        for po in self:
            if po.state in ("draft", "sent", "purchase"):
                po.rejection_reason = reason or ""
                # Giải phóng dòng chi phí để điều hành tìm NCC khác + tạo PO mới
                self.env["touriha.costing.line"].sudo().search(
                    [("purchase_order_id", "=", po.id)]
                ).write({"purchase_order_id": False, "purchase_line_id": False})
                po.button_cancel()
                po.message_post(
                    body=_("Nhà cung cấp TỪ CHỐI PO qua portal. Lý do: %s")
                    % (reason or "—")
                )
                po._touriha_notify_operation(
                    _("Nhà cung cấp %s TỪ CHỐI PO %s. Lý do: %s")
                    % (po.partner_id.name, po.name, reason or "—")
                )
        return True

    def _touriha_notify_operation(self, body):
        self.ensure_one()
        operator = self.create_uid
        partner_ids = operator.partner_id.ids if operator and operator.partner_id else []
        self.message_post(body=body, partner_ids=partner_ids)
