from werkzeug.exceptions import Forbidden, NotFound

from odoo import http
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal


class TourihaPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if "touriha_po_count" in counters:
            partner = request.env.user.partner_id.commercial_partner_id
            values["touriha_po_count"] = (
                request.env["purchase.order"]
                .sudo()
                .search_count(self._touriha_po_domain(partner))
            )
        return values

    def _touriha_po_domain(self, partner):
        return [("partner_id", "child_of", partner.id), ("tour_id", "!=", False)]

    def _touriha_get_po(self, po_id):
        po = request.env["purchase.order"].sudo().browse(po_id)
        if not po.exists():
            raise NotFound()
        user_partner = request.env.user.partner_id.commercial_partner_id
        if po.partner_id.commercial_partner_id.id != user_partner.id:
            raise Forbidden()
        return po

    @http.route("/my/touriha/purchases", type="http", auth="user", website=True)
    def portal_my_touriha_purchases(self, **kw):
        partner = request.env.user.partner_id.commercial_partner_id
        pos = (
            request.env["purchase.order"]
            .sudo()
            .search(self._touriha_po_domain(partner), order="create_date desc")
        )
        return request.render(
            "touriha_portal.portal_my_touriha_purchases",
            {"purchases": pos, "page_name": "touriha_purchase"},
        )

    @http.route(
        "/my/touriha/purchase/<int:po_id>", type="http", auth="user", website=True
    )
    def portal_touriha_purchase(self, po_id, **kw):
        po = self._touriha_get_po(po_id)
        return request.render(
            "touriha_portal.portal_touriha_purchase_detail",
            {"po": po, "page_name": "touriha_purchase"},
        )

    @http.route(
        "/my/touriha/purchase/<int:po_id>/accept",
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
    )
    def portal_touriha_purchase_accept(self, po_id, **kw):
        self._touriha_get_po(po_id).action_portal_accept()
        return request.redirect("/my/touriha/purchase/%s" % po_id)

    @http.route(
        "/my/touriha/purchase/<int:po_id>/reject",
        type="http",
        auth="user",
        methods=["POST"],
        website=True,
    )
    def portal_touriha_purchase_reject(self, po_id, **kw):
        self._touriha_get_po(po_id).action_portal_reject(reason=kw.get("reason"))
        return request.redirect("/my/touriha/purchase/%s" % po_id)
