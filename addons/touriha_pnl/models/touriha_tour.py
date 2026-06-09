from odoo import api, fields, models


class TourihaTour(models.Model):
    _inherit = "touriha.tour"

    revenue = fields.Monetary("Doanh thu", compute="_compute_pnl", store=True)
    gross_profit = fields.Monetary(
        "Lợi nhuận (kế hoạch)", compute="_compute_pnl", store=True
    )
    margin = fields.Float("Biên LN (%)", compute="_compute_pnl", store=True)
    actual_profit = fields.Monetary(
        "Lợi nhuận (thực tế)", compute="_compute_pnl", store=True
    )
    actual_margin = fields.Float(
        "Biên LN thực tế (%)", compute="_compute_pnl", store=True
    )

    @api.depends(
        "sale_order_id.amount_total",
        "cost_finalized_total",
        "cost_actual_total",
    )
    def _compute_pnl(self):
        for tour in self:
            rev = tour.sale_order_id.amount_total if tour.sale_order_id else 0.0
            tour.revenue = rev
            tour.gross_profit = rev - tour.cost_finalized_total
            tour.actual_profit = rev - tour.cost_actual_total
            tour.margin = (tour.gross_profit / rev * 100.0) if rev else 0.0
            tour.actual_margin = (tour.actual_profit / rev * 100.0) if rev else 0.0
