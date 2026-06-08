from odoo import _, api, fields, models
from odoo.exceptions import UserError


class TourihaTour(models.Model):
    _inherit = "touriha.tour"

    costing_line_ids = fields.One2many(
        "touriha.costing.line", "tour_id", string="Dòng chi phí"
    )
    cost_estimate_total = fields.Monetary(
        "Tổng dự kiến", compute="_compute_cost_totals", store=True
    )
    cost_finalized_total = fields.Monetary(
        "Tổng chốt", compute="_compute_cost_totals", store=True
    )
    cost_actual_total = fields.Monetary(
        "Tổng thực tế", compute="_compute_cost_totals", store=True
    )

    purchase_order_ids = fields.One2many(
        "purchase.order", "tour_id", string="Đơn mua"
    )
    purchase_order_count = fields.Integer(compute="_compute_purchase_order_count")

    @api.depends(
        "costing_line_ids.estimate_subtotal",
        "costing_line_ids.finalized_subtotal",
        "costing_line_ids.actual_subtotal",
    )
    def _compute_cost_totals(self):
        for tour in self:
            tour.cost_estimate_total = sum(
                tour.costing_line_ids.mapped("estimate_subtotal")
            )
            tour.cost_finalized_total = sum(
                tour.costing_line_ids.mapped("finalized_subtotal")
            )
            tour.cost_actual_total = sum(
                tour.costing_line_ids.mapped("actual_subtotal")
            )

    @api.depends("purchase_order_ids")
    def _compute_purchase_order_count(self):
        for tour in self:
            tour.purchase_order_count = len(tour.purchase_order_ids)

    def action_create_purchase_orders(self):
        self.ensure_one()
        lines = self.costing_line_ids.filtered(
            lambda l: l.finalized_price and l.supplier_id and not l.purchase_order_id
        )
        if not lines:
            raise UserError(
                _(
                    "Không có dòng chi phí nào sẵn sàng tạo PO "
                    "(cần có giá chốt + nhà cung cấp, và chưa tạo PO)."
                )
            )
        po_by_supplier = {}
        for line in lines:
            po = po_by_supplier.get(line.supplier_id.id)
            if not po:
                po = self.env["purchase.order"].create(
                    {
                        "partner_id": line.supplier_id.id,
                        "origin": self.code,
                        "tour_id": self.id,
                        "company_id": self.company_id.id,
                    }
                )
                po_by_supplier[line.supplier_id.id] = po
            pol = self.env["purchase.order.line"].create(
                {
                    "order_id": po.id,
                    "product_id": line.product_id.id,
                    "product_qty": line.quantity,
                }
            )
            pol.price_unit = line.finalized_price
            line.write({"purchase_order_id": po.id, "purchase_line_id": pol.id})
        self.message_post(
            body=_("Đã tạo %s đơn mua (PO) từ bảng chi phí.") % len(po_by_supplier)
        )
        return self.action_view_purchase_orders()

    def action_view_purchase_orders(self):
        self.ensure_one()
        return {
            "type": "ir.actions.act_window",
            "name": _("Đơn mua – %s") % self.name,
            "res_model": "purchase.order",
            "domain": [("tour_id", "=", self.id)],
            "view_mode": "list,form",
            "context": {"default_tour_id": self.id},
        }
