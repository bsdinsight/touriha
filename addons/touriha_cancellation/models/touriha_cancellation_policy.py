from odoo import fields, models


class TourihaCancellationPolicy(models.Model):
    _name = "touriha.cancellation.policy"
    _description = "Chính sách hủy tour"
    _order = "priority desc, id"

    name = fields.Char("Tên chính sách", required=True)
    tour_type = fields.Selection(
        [
            ("domestic", "Nội địa"),
            ("outbound", "Outbound"),
            ("inbound", "Inbound"),
            ("vip", "VIP / MICE"),
            ("all", "Tất cả"),
        ],
        string="Áp dụng cho loại tour",
        default="all",
        required=True,
    )
    active = fields.Boolean("Hoạt động", default=True)
    priority = fields.Integer("Độ ưu tiên", default=10)
    rule_ids = fields.One2many(
        "touriha.cancellation.penalty.rule", "policy_id", string="Mức phạt", copy=True
    )


class TourihaCancellationPenaltyRule(models.Model):
    _name = "touriha.cancellation.penalty.rule"
    _description = "Mức phạt hủy theo ngày"
    _order = "days_before desc"

    policy_id = fields.Many2one(
        "touriha.cancellation.policy", required=True, ondelete="cascade"
    )
    days_before = fields.Integer(
        "Hủy trước (ngày) ≥",
        required=True,
        help="Áp dụng khi số ngày trước khởi hành ≥ giá trị này "
        "(lấy ngưỡng cao nhất phù hợp).",
    )
    penalty_rate = fields.Float("Tỷ lệ phạt (%)", required=True)
