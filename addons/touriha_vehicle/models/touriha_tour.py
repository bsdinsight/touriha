from odoo import api, fields, models


class TourihaTour(models.Model):
    _inherit = "touriha.tour"

    vehicle_suggestion = fields.Char(
        "Gợi ý xe", compute="_compute_vehicle_suggestion"
    )
    vehicle_suggestion_cost = fields.Monetary(
        "Chi phí xe (gợi ý)", compute="_compute_vehicle_suggestion"
    )

    @api.depends("seat_count")
    def _compute_vehicle_suggestion(self):
        types = self.env["touriha.vehicle.type"].search(
            [("active", "=", True), ("seat_capacity", ">", 0), ("price", ">", 0)]
        )
        for tour in self:
            seats = tour.seat_count or 0
            if seats <= 0 or not types:
                tour.vehicle_suggestion = ""
                tour.vehicle_suggestion_cost = 0.0
                continue
            # DP: dp[s] = chi phí nhỏ nhất để phủ >= s ghế
            inf = float("inf")
            dp = [0.0] + [inf] * seats
            choice = [None] * (seats + 1)
            for s in range(1, seats + 1):
                for vt in types:
                    prev = dp[max(0, s - vt.seat_capacity)]
                    if prev + vt.price < dp[s]:
                        dp[s] = prev + vt.price
                        choice[s] = vt
            if dp[seats] == inf:
                tour.vehicle_suggestion = ""
                tour.vehicle_suggestion_cost = 0.0
                continue
            # Truy vết tổ hợp xe đã chọn
            counts = {}
            id2type = {vt.id: vt for vt in types}
            s, guard = seats, 0
            while s > 0 and choice[s] is not None and guard < 1000:
                vt = choice[s]
                counts[vt.id] = counts.get(vt.id, 0) + 1
                s = max(0, s - vt.seat_capacity)
                guard += 1
            parts = [
                "%sx %s (%s chỗ)" % (n, id2type[i].name, id2type[i].seat_capacity)
                for i, n in counts.items()
            ]
            tour.vehicle_suggestion = " + ".join(parts)
            tour.vehicle_suggestion_cost = dp[seats]
