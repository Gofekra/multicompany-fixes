from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountFiscalPosition(models.Model):
    _inherit = 'account.fiscal.position'

    @api.constrains('company_id')
    def _check_company_id_out_model(self):
        super(AccountFiscalPosition, self)._check_company_id_out_model()
        if not self.env.context.get('bypass_company_validation', False):
            for rec in self:
                if not rec.company_id:
                    continue
                field = self.env['pos.order'].search(
                    [('fiscal_position_id', '=', rec.id),
                     ('company_id', '!=', False),
                     ('company_id', '!=', rec.company_id.id)], limit=1)
                if field:
                    raise ValidationError(
                        _('You cannot change the company, as this '
                          'Account Fiscal Position is assigned to Pos Order '
                          '(%s).' % field.name_get()[0][1]))
                field = self.env['pos.config'].search(
                    [('default_fiscal_position_id', '=', rec.id),
                     ('company_id', '!=', False),
                     ('company_id', '!=', rec.company_id.id)], limit=1)
                if field:
                    raise ValidationError(
                        _('You cannot change the company, as this '
                          'Account Fiscal Position is assigned to Pos Config '
                          '(%s).' % field.name_get()[0][1]))
                field = self.env['pos.config'].search(
                    [('fiscal_position_ids', 'in', [rec.id]),
                     ('company_id', '!=', False),
                     ('company_id', '!=', rec.company_id.id)], limit=1)
                if field:
                    raise ValidationError(
                        _('You cannot change the company, as this '
                          'Account Fiscal Position is assigned to Pos Config '
                          '(%s).' % field.name_get()[0][1]))


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('company_id')
    def _check_company_id_out_model(self):
        super(Partner, self)._check_company_id_out_model()
        if not self.env.context.get('bypass_company_validation', False):
            for rec in self:
                if not rec.company_id:
                    continue
                field = self.env['pos.order'].sudo().search(
                    [('partner_id', '=', rec.id),
                     ('company_id', '!=', False),
                     ('company_id', '!=', rec.company_id.id)], limit=1)
                if field:
                    raise ValidationError(
                        _('You cannot change the company, as this '
                          'Res Partner is assigned to Pos Order '
                          '(%s).' % field.name_get()[0][1]))
