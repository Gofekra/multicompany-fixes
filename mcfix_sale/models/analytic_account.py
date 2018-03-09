from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'

    @api.constrains('company_id')
    def _check_company_id_out_model(self):
        super(AccountAnalyticAccount, self)._check_company_id_out_model()
        if not self.env.context.get('bypass_company_validation', False):
            for rec in self:
                if not rec.company_id:
                    continue
                field = self.env['sale.order'].search(
                    [('analytic_account_id', '=', rec.id),
                     ('company_id', '!=', False),
                     ('company_id', '!=', rec.company_id.id)], limit=1)
                if field:
                    raise ValidationError(
                        _('You cannot change the company, as this '
                          'Account Analytic Account is assigned to Sale Order '
                          '(%s).' % field.name_get()[0][1]))


class AccountAnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    @api.multi
    @api.constrains('company_id', 'so_line')
    def _check_company_id_so_line(self):
        for rec in self.sudo():
            if rec.company_id and rec.so_line.company_id and\
                    rec.company_id != rec.so_line.company_id:
                raise ValidationError(
                    _('The Company in the Account Analytic Line and in '
                      'Sale Order Line must be the same.'))