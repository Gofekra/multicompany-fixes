from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.constrains('company_id')
    def _check_company_id_out_model(self):
        super(AccountInvoice, self)._check_company_id_out_model()
        if not self.env.context.get('bypass_company_validation', False):
            for rec in self:
                if not rec.company_id:
                    continue
                field = self.env['pos.order'].search(
                    [('invoice_id', '=', rec.id),
                     ('company_id', '!=', False),
                     ('company_id', '!=', rec.company_id.id)], limit=1)
                if field:
                    raise ValidationError(
                        _('You cannot change the company, as this '
                          'Account Invoice is assigned to Pos Order '
                          '(%s).' % field.name_get()[0][1]))
