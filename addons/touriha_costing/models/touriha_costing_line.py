from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
from odoo.tools import float_compare


class TourihaCostingLine(models.Model):
    _name = "touriha.costing.line"
    _description = "Dòng chi phí tour (costing)"
    _order = "tour_id, supplier_id, id"

    tour_id = fields.Many2one(
        "touriha.tour", string="Tour", required=True, ondelete="cascade", index=True
    )
    currency_id = fields.Many2one(related="tour_id.currency_id")
    product_id = fields.Many2one("product.product", string="Dịch vụ", required=True)
    supplier_id = fields.Many2one(
        "res.partner", string="Nhà cung cấp", domain="[('supplier_rank', '>', 0)]"
    )
    quantity = fields.Float("Số lượng", default=1.0)

    estimate_price = fields.Monetary("Giá dự kiến")
    finalized_price = fields.Monetary("Giá chốt")
    actual_price = fields.Monetary("Giá thực tế")
    override_reason = fields.Char("Lý do chỉnh giá chốt")

    estimate_subtotal = fields.Monetary(
        "Tạm tính (dự kiến)", compute="_compute_subtotals", store=True
    )
    finalized_subtotal = fields.Monetary(
        "Tạm tính (chốt)", compute="_compute_subtotals", store=True
    )
    actual_subtotal = fields.Monetary(
        "Tạm tính (thực tế)", compute="_compute_subtotals", store=True
    )

    variance_percent = fields.Float(
        "Biến động %", compute="_compute_variance", store=True
    )
    variance_alert = fields.Boolean(
        "Cảnh báo biến động", compute="_compute_variance", store=True
    )

    purchase_order_id = fields.Many2one(
        "purchase.order", string="Đơn mua (PO)", readonly=True, copy=False
    )
    purchase_line_id = fields.Many2one(
        "purchase.order.line", readonly=True, copy=False
    )

    state = fields.Selection(
        [
            ("estimate", "Dự kiến"),
            ("finalized", "Đã chốt"),
            ("po_created", "Đã tạo PO"),
            ("actual", "Thực tế"),
        ],
        compute="_compute_state",
        store=True,
        default="estimate",
    )

    @api.depends("quantity", "estimate_price", "finalized_price", "actual_price")
    def _compute_subtotals(self):
        for line in self:
            line.estimate_subtotal = line.quantity * line.estimate_price
            line.finalized_subtotal = line.quantity * line.finalized_price
            line.actual_subtotal = line.quantity * line.actual_price

    @api.depends("finalized_price", "actual_price")
    def _compute_variance(self):
        for line in self:
            if line.finalized_price and line.actual_price:
                line.variance_percent = (
                    (line.actual_price - line.finalized_price)
                    / line.finalized_price
                    * 100
                )
            else:
                line.variance_percent = 0.0
            line.variance_alert = abs(line.variance_percent) > 5.0

    @api.depends("finalized_price", "actual_price", "purchase_order_id")
    def _compute_state(self):
        for line in self:
            if line.actual_price:
                line.state = "actual"
            elif line.purchase_order_id:
                line.state = "po_created"
            elif line.finalized_price:
                line.state = "finalized"
            else:
                line.state = "estimate"

    @api.constrains("finalized_price", "estimate_price", "override_reason")
    def _check_override_reason(self):
        for line in self:
            if (
                line.finalized_price
                and line.estimate_price
                and float_compare(
                    line.finalized_price, line.estimate_price, precision_digits=2
                )
                != 0
                and not line.override_reason
            ):
                raise ValidationError(
                    _("Dòng '%s': cần nhập lý do khi giá chốt khác giá dự kiến.")
                    % (line.product_id.display_name or "")
                )

    @api.onchange("product_id")
    def _onchange_product_id(self):
        if self.product_id:
            if not self.estimate_price:
                self.estimate_price = self.product_id.standard_price
            if not self.supplier_id and self.product_id.seller_ids:
                self.supplier_id = self.product_id.seller_ids[0].partner_id
