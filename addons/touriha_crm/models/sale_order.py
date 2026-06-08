from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_tour = fields.Boolean("Là báo giá tour")
    tour_type = fields.Selection(
        [
            ("domestic", "Nội địa"),
            ("outbound", "Outbound"),
            ("inbound", "Inbound"),
        ],
        string="Loại tour",
        default="domestic",
    )
    tour_start_date = fields.Date("Ngày khởi hành")
    tour_end_date = fields.Date("Ngày kết thúc")

    passenger_ids = fields.One2many(
        "touriha.passenger", "sale_order_id", string="Hành khách"
    )
    passenger_count = fields.Integer(
        "Số khách", compute="_compute_passenger_count", store=True
    )
    tour_id = fields.Many2one(
        "touriha.tour", string="Tour", copy=False, readonly=True
    )
    passport_warning = fields.Char(
        "Cảnh báo hộ chiếu", compute="_compute_passport_warning"
    )

    @api.depends("passenger_ids")
    def _compute_passenger_count(self):
        for order in self:
            order.passenger_count = len(order.passenger_ids)

    @api.depends("passenger_ids.passport_expiry", "tour_end_date")
    def _compute_passport_warning(self):
        for order in self:
            late = []
            if order.tour_end_date:
                for pax in order.passenger_ids:
                    if (
                        pax.passport_expiry
                        and (pax.passport_expiry - order.tour_end_date).days < 180
                    ):
                        late.append(pax.name or "?")
            order.passport_warning = (
                _("Hộ chiếu còn hạn dưới 6 tháng tính đến ngày kết thúc tour: %s")
                % ", ".join(late)
                if late
                else False
            )

    def action_confirm(self):
        res = super().action_confirm()
        for order in self:
            if order.is_tour and not order.tour_id:
                order._create_touriha_tour()
        return res

    def _create_touriha_tour(self):
        self.ensure_one()
        name = _("Tour - %s") % self.partner_id.name if self.partner_id else self.name
        tour = self.env["touriha.tour"].create(
            {
                "name": name,
                "tour_type": self.tour_type or "domestic",
                "start_date": self.tour_start_date,
                "end_date": self.tour_end_date,
                "customer_id": self.partner_id.id,
                "company_id": self.company_id.id,
                "sale_order_id": self.id,
            }
        )
        self.tour_id = tour.id
        self.passenger_ids.write({"tour_id": tour.id})
        self.message_post(body=_("Đã tạo tour %s từ báo giá này.") % tour.code)
        return tour

    def action_view_tour(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "res_model": "touriha.tour",
            "res_id": self.tour_id.id,
            "view_mode": "form",
            "target": "current",
        }
