# Copyright 2015 Antiun Ingenieria S.L. - Javier Iniesta
# Copyright 2018 ForgeFlow, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import _, api, exceptions, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    industry_id = fields.Many2one(
        comodel_name="res.partner.industry", string="Industry"
    )

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        """Propagate industries in the creation of partner."""
        values = super()._prepare_customer_values(
            partner_name, is_company=is_company, parent_id=parent_id
        )
        values.update(
            {
                "industry_id": self.industry_id.id,
            }
        )
        return values

    @api.onchange("partner_id")
    def _onchange_partner_id(self):
        if self.partner_id:
            if self.partner_id.industry_id:
                self.industry_id = self.partner_id.industry_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("partner_id"):
                customer = self.env["res.partner"].browse(vals["partner_id"])
                if customer.industry_id and not vals.get("industry_id"):
                    vals.update({"industry_id": customer.industry_id.id})
        return super().create(vals_list)
