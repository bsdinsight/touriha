from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class TourihaTour(models.Model):
    _name = "touriha.tour"
    _description = "Tour du lịch"
    _inherit = ["mail.thread", "mail.activity.mixin"]
    _order = "start_date desc, id desc"

    name = fields.Char("Tên tour", required=True, tracking=True)
    code = fields.Char("Mã tour", required=True, copy=False, default="New", tracking=True)
    tour_type = fields.Selection(
        [
            ("domestic", "Nội địa"),
            ("outbound", "Outbound"),
            ("inbound", "Inbound"),
        ],
        string="Loại tour",
        default="domestic",
        required=True,
        tracking=True,
    )

    start_date = fields.Date("Ngày khởi hành", tracking=True)
    end_date = fields.Date("Ngày kết thúc", tracking=True)
    duration_days = fields.Integer("Số ngày", compute="_compute_duration", store=True)

    customer_id = fields.Many2one("res.partner", string="Khách hàng", tracking=True)
    company_id = fields.Many2one(
        "res.company", default=lambda self: self.env.company, required=True
    )
    currency_id = fields.Many2one("res.currency", related="company_id.currency_id")

    min_pax = fields.Integer("Số khách tối thiểu", default=1)
    max_pax = fields.Integer("Số khách tối đa", default=40)

    passenger_ids = fields.One2many("touriha.passenger", "tour_id", string="Hành khách")
    passenger_count = fields.Integer(
        "Số khách", compute="_compute_passenger_count", store=True
    )

    state = fields.Selection(
        [
            ("draft", "Nháp"),
            ("confirmed", "Đã xác nhận"),
            ("in_progress", "Đang chạy"),
            ("completed", "Hoàn thành"),
            ("cancelled", "Đã hủy"),
        ],
        default="draft",
        required=True,
        tracking=True,
    )

    note = fields.Html("Ghi chú")

    @api.depends("start_date", "end_date")
    def _compute_duration(self):
        for tour in self:
            if tour.start_date and tour.end_date and tour.end_date >= tour.start_date:
                tour.duration_days = (tour.end_date - tour.start_date).days + 1
            else:
                tour.duration_days = 0

    @api.depends("passenger_ids")
    def _compute_passenger_count(self):
        for tour in self:
            tour.passenger_count = len(tour.passenger_ids)

    @api.constrains("start_date", "end_date")
    def _check_dates(self):
        for tour in self:
            if tour.start_date and tour.end_date and tour.end_date < tour.start_date:
                raise ValidationError(
                    _("Ngày kết thúc phải sau hoặc bằng ngày khởi hành.")
                )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("code", "New") == "New":
                vals["code"] = self.env["ir.sequence"].next_by_code("touriha.tour") or "New"
        return super().create(vals_list)

    def action_confirm(self):
        self.write({"state": "confirmed"})

    def action_start(self):
        self.write({"state": "in_progress"})

    def action_complete(self):
        self.write({"state": "completed"})

    def action_cancel(self):
        self.write({"state": "cancelled"})

    def action_reset_to_draft(self):
        self.write({"state": "draft"})
