from odoo import fields, models


class TourihaVehicleType(models.Model):
    _name = "touriha.vehicle.type"
    _description = "Loại xe"
    _order = "seat_capacity, id"

    name = fields.Char("Tên loại xe", required=True)
    seat_capacity = fields.Integer("Sức chứa (ghế)", required=True, default=16)
    price = fields.Monetary("Giá thuê", required=True)
    currency_id = fields.Many2one(
        "res.currency", default=lambda self: self.env.company.currency_id
    )
    supplier_id = fields.Many2one("res.partner", string="Nhà cung cấp")
    active = fields.Boolean("Hoạt động", default=True)
