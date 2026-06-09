from odoo import _, api, fields, models
from odoo.exceptions import UserError


class TourihaCancellationRequest(models.Model):
    _name = "touriha.cancellation.request"
    _description = "Yêu cầu hủy tour & hoàn tiền"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "create_date desc"
    _rec_name = "tour_id"

    tour_id = fields.Many2one(
        "touriha.tour", string="Tour", required=True, tracking=True
    )
    currency_id = fields.Many2one(related="tour_id.currency_id")
    cancellation_date = fields.Date(
        "Ngày yêu cầu hủy", default=fields.Date.context_today, required=True, tracking=True
    )
    cancellation_by = fields.Selection(
        [
            ("customer", "Khách hàng"),
            ("touriha", "Touriha chủ động"),
            ("force_majeure", "Bất khả kháng"),
        ],
        string="Bên hủy",
        default="customer",
        required=True,
        tracking=True,
    )
    reason = fields.Char("Lý do")

    total_amount = fields.Monetary("Tổng đã thanh toán")
    days_before_departure = fields.Integer(
        "Số ngày trước khởi hành", compute="_compute_days", store=True
    )
    policy_id = fields.Many2one(
        "touriha.cancellation.policy",
        string="Chính sách áp dụng",
        compute="_compute_policy",
        store=True,
    )
    penalty_rate = fields.Float("Tỷ lệ phạt (%)", compute="_compute_penalty", store=True)
    penalty_amount = fields.Monetary("Tiền phạt", compute="_compute_penalty", store=True)
    refund_amount = fields.Monetary(
        "Tiền hoàn lại", compute="_compute_penalty", store=True
    )

    refund_method = fields.Selection(
        [
            ("bank_transfer", "Chuyển khoản"),
            ("credit_note", "Credit note"),
            ("cash", "Tiền mặt"),
            ("momo", "Momo"),
            ("vnpay", "VNPay"),
        ],
        string="Phương thức hoàn tiền",
    )

    state = fields.Selection(
        [
            ("draft", "Nháp"),
            ("approved", "Đã duyệt"),
            ("done", "Đã hoàn tiền"),
            ("rejected", "Từ chối"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )

    @api.depends("tour_id.start_date", "cancellation_date")
    def _compute_days(self):
        for req in self:
            if req.tour_id.start_date and req.cancellation_date:
                req.days_before_departure = (
                    req.tour_id.start_date - req.cancellation_date
                ).days
            else:
                req.days_before_departure = 0

    @api.depends("tour_id.tour_type")
    def _compute_policy(self):
        Policy = self.env["touriha.cancellation.policy"]
        for req in self:
            policy = Policy.search(
                [
                    ("active", "=", True),
                    "|",
                    ("tour_type", "=", req.tour_id.tour_type),
                    ("tour_type", "=", "all"),
                ],
                order="priority desc, id",
                limit=1,
            )
            req.policy_id = policy.id if policy else False

    @api.depends(
        "days_before_departure", "policy_id", "cancellation_by", "total_amount"
    )
    def _compute_penalty(self):
        for req in self:
            if req.cancellation_by in ("touriha", "force_majeure"):
                rate = 0.0  # Touriha hủy / bất khả kháng → hoàn 100%
            elif req.policy_id and req.policy_id.rule_ids:
                applicable = req.policy_id.rule_ids.filtered(
                    lambda r: r.days_before <= req.days_before_departure
                )
                if applicable:
                    rate = max(applicable, key=lambda r: r.days_before).penalty_rate
                else:
                    # ngày trước khởi hành < mọi ngưỡng → mức phạt cao nhất
                    rate = req.policy_id.rule_ids.sorted("days_before")[0].penalty_rate
            else:
                rate = 0.0
            req.penalty_rate = rate
            req.penalty_amount = req.total_amount * rate / 100.0
            req.refund_amount = req.total_amount - req.penalty_amount

    def action_approve(self):
        for req in self:
            if req.state != "draft":
                raise UserError(_("Chỉ duyệt được yêu cầu ở trạng thái Nháp."))
            req.state = "approved"
            req.tour_id.write({"state": "cancelled"})
            req.tour_id.message_post(
                body=_("Tour bị hủy (phí hủy %s%%, hoàn lại %s).")
                % (req.penalty_rate, req.refund_amount)
            )
        return True

    def action_done(self):
        for req in self:
            if req.state != "approved":
                raise UserError(_("Chỉ hoàn tiền sau khi đã duyệt."))
            if req.refund_amount > 0 and not req.refund_method:
                raise UserError(_("Vui lòng chọn phương thức hoàn tiền."))
            req.state = "done"
            req.message_post(
                body=_("Đã hoàn tiền %s qua %s.")
                % (req.refund_amount, req.refund_method or "—")
            )
        return True

    def action_reject(self):
        self.write({"state": "rejected"})
        return True

    def action_draft(self):
        self.write({"state": "draft"})
        return True
