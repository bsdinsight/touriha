from odoo import models


class TourihaCancellationRequest(models.Model):
    _inherit = "touriha.cancellation.request"

    def action_done(self):
        res = super().action_done()
        template = self.env.ref(
            "touriha_notification.mail_template_refund", raise_if_not_found=False
        )
        if template:
            for req in self.filtered(lambda r: r.state == "done"):
                cust = req.tour_id.customer_id
                if cust and cust.email:
                    template.send_mail(req.id, force_send=False)
        return res
