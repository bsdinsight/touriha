from odoo import fields, models


class TourihaPassenger(models.Model):
    _name = "touriha.passenger"
    _description = "Hành khách trong tour"
    _order = "tour_id, id"

    # Optional: hành khách có thể được nhập ở báo giá (sale.order) trước khi có tour;
    # touriha_crm gắn sale_order_id và set tour_id khi xác nhận báo giá.
    tour_id = fields.Many2one(
        "touriha.tour", string="Tour", ondelete="cascade", index=True
    )
    partner_id = fields.Many2one("res.partner", string="Liên hệ")
    name = fields.Char("Họ tên", required=True)
    birth_date = fields.Date("Ngày sinh")
    pax_type = fields.Selection(
        [
            ("adult", "Người lớn"),
            ("child_bed", "Trẻ em (có giường)"),
            ("child_no_bed", "Trẻ em (không giường)"),
            ("infant", "Em bé"),
        ],
        string="Loại khách",
        default="adult",
        required=True,
    )
    passport_number = fields.Char("Số hộ chiếu")
    passport_expiry = fields.Date("Hết hạn hộ chiếu")
    rooming_group = fields.Char("Nhóm phòng")
    note = fields.Char("Ghi chú")
