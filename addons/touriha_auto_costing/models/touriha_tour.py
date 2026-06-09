from odoo import _, models


class TourihaTour(models.Model):
    _inherit = "touriha.tour"

    def action_fill_costing_from_quantity(self):
        """Tạo/cập nhật dòng chi phí theo định mức tự tính (1 dòng/loại dịch vụ)."""
        self.ensure_one()
        Line = self.env["touriha.costing.line"]
        mapping = [
            ("hotel", self.room_count),
            ("meal", self.meal_count),
            ("transport", self.seat_count),
        ]
        for service_type, qty in mapping:
            if not qty:
                continue
            line = self.costing_line_ids.filtered(
                lambda l: l.service_type == service_type
            )[:1]
            if line:
                line.quantity = qty
            else:
                Line.create(
                    {
                        "tour_id": self.id,
                        "service_type": service_type,
                        "quantity": qty,
                    }
                )
        self.message_post(
            body=_(
                "Đã đổ định mức vào bảng chi phí: phòng=%s, suất ăn=%s, ghế=%s."
            )
            % (self.room_count, self.meal_count, self.seat_count)
        )
        return True
