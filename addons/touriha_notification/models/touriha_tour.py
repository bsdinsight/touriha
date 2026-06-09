from datetime import timedelta

from odoo import api, fields, models


class TourihaTour(models.Model):
    _inherit = "touriha.tour"

    def _touriha_send_template(self, xmlid):
        template = self.env.ref(xmlid, raise_if_not_found=False)
        if not template:
            return
        for tour in self:
            if tour.customer_id and tour.customer_id.email:
                template.send_mail(tour.id, force_send=False)

    def action_confirm(self):
        res = super().action_confirm()
        self._touriha_send_template(
            "touriha_notification.mail_template_tour_confirmed"
        )
        return res

    def action_create_purchase_orders(self):
        res = super().action_create_purchase_orders()
        template = self.env.ref(
            "touriha_notification.mail_template_po_supplier", raise_if_not_found=False
        )
        if template:
            pos = self.mapped("purchase_order_ids").filtered(
                lambda p: not p.touriha_po_mail_sent and p.partner_id.email
            )
            for po in pos:
                template.send_mail(po.id, force_send=False)
                po.touriha_po_mail_sent = True
        return res

    @api.model
    def _cron_departure_reminder(self):
        days = int(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("touriha.departure_reminder_days", "3")
        )
        target = fields.Date.today() + timedelta(days=days)
        tours = self.search(
            [("state", "=", "confirmed"), ("start_date", "=", target)]
        )
        tours._touriha_send_template(
            "touriha_notification.mail_template_departure_reminder"
        )
        return True
