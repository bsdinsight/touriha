import math

from odoo import api, fields, models


class TourihaTour(models.Model):
    _inherit = "touriha.tour"

    # ── Cấu hình định mức ──
    room_capacity = fields.Integer("Số khách/phòng", default=2)
    foc_per_pax = fields.Integer(
        "FOC: cứ N khách +1 miễn phí",
        default=0,
        help="0 = không áp dụng. Vd 15 = mỗi 15 khách trả phí được 1 suất miễn phí "
        "(trưởng đoàn/HDV).",
    )

    # ── Cơ cấu khách (tự tính) ──
    pax_adult = fields.Integer("Người lớn", compute="_compute_auto_quantity", store=True)
    pax_child_bed = fields.Integer(
        "Trẻ em (có giường)", compute="_compute_auto_quantity", store=True
    )
    pax_child_no_bed = fields.Integer(
        "Trẻ em (không giường)", compute="_compute_auto_quantity", store=True
    )
    pax_infant = fields.Integer("Em bé", compute="_compute_auto_quantity", store=True)

    # ── Định mức tự động ──
    room_count = fields.Integer("Số phòng", compute="_compute_auto_quantity", store=True)
    meal_count = fields.Float("Số suất ăn", compute="_compute_auto_quantity", store=True)
    seat_count = fields.Integer("Số ghế xe", compute="_compute_auto_quantity", store=True)
    foc_count = fields.Integer("Số suất FOC", compute="_compute_auto_quantity", store=True)

    @api.depends(
        "passenger_ids.pax_type",
        "passenger_ids.rooming_group",
        "room_capacity",
        "foc_per_pax",
    )
    def _compute_auto_quantity(self):
        for tour in self:
            paxs = tour.passenger_ids
            adult = paxs.filtered(lambda p: p.pax_type == "adult")
            child_bed = paxs.filtered(lambda p: p.pax_type == "child_bed")
            child_no_bed = paxs.filtered(lambda p: p.pax_type == "child_no_bed")
            infant = paxs.filtered(lambda p: p.pax_type == "infant")

            tour.pax_adult = len(adult)
            tour.pax_child_bed = len(child_bed)
            tour.pax_child_no_bed = len(child_no_bed)
            tour.pax_infant = len(infant)

            # Suất ăn: NL=1, trẻ có giường=1, trẻ không giường=0.5, em bé=0
            tour.meal_count = len(adult) + len(child_bed) + 0.5 * len(child_no_bed)
            # Ghế xe: mọi khách trừ em bé
            tour.seat_count = len(adult) + len(child_bed) + len(child_no_bed)

            # Phòng: khách cần giường = NL + trẻ có giường.
            # Mỗi "Nhóm phòng" khai báo = 1 phòng; phần còn lại ghép theo số khách/phòng.
            bed_pax = adult + child_bed
            cap = tour.room_capacity if tour.room_capacity and tour.room_capacity > 0 else 2
            grouped = bed_pax.filtered(lambda p: p.rooming_group)
            ungrouped = bed_pax - grouped
            n_groups = len(set(grouped.mapped("rooming_group")))
            tour.room_count = n_groups + math.ceil(len(ungrouped) / cap)

            # FOC: theo số khách trả phí (không tính em bé)
            paying = len(adult) + len(child_bed) + len(child_no_bed)
            tour.foc_count = (paying // tour.foc_per_pax) if tour.foc_per_pax else 0
