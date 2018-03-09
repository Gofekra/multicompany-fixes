from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountJournal(models.Model):
    _inherit = 'account.journal'

    # @api.model
    # def search(self, args, offset=0, limit=None, order=None, count=False):
    #     company = self._context.get('company_id')
    #     if company:
    #         args += [('company_id', '=', company)]
    #     return super(AccountJournal, self).search(
    #         args=args, offset=offset, limit=limit, order=order, count=count)

    @api.constrains('company_id')
    def _check_company_id_out_model(self):
        super(AccountJournal, self)._check_company_id_out_model()
        if not self.env.context.get('bypass_company_validation', False):
            for rec in self:
                if not rec.company_id:
                    continue
                field = self.env['pos.order'].search(
                    [('sale_journal', '=', rec.id),
                     ('company_id', '!=', False),
                     ('company_id', '!=', rec.company_id.id)], limit=1)
                if field:
                    raise ValidationError(
                        _('You cannot change the company, as this '
                          'Account Journal is assigned to Pos Order '
                          '(%s).' % field.name_get()[0][1]))
                field = self.env['pos.config'].search(
                    [('invoice_journal_id', '=', rec.id),
                     ('company_id', '!=', False),
                     ('company_id', '!=', rec.company_id.id)], limit=1)
                if field:
                    raise ValidationError(
                        _('You cannot change the company, as this '
                          'Account Journal is assigned to Pos Config '
                          '(%s).' % field.name_get()[0][1]))
                field = self.env['pos.config'].search(
                    [('journal_ids', 'in', [rec.id]),
                     ('company_id', '!=', False),
                     ('company_id', '!=', rec.company_id.id)], limit=1)
                if field:
                    raise ValidationError(
                        _('You cannot change the company, as this '
                          'Account Journal is assigned to Pos Config '
                          '(%s).' % field.name_get()[0][1]))
                field = self.env['pos.config'].search(
                    [('journal_id', '=', rec.id),
                     ('company_id', '!=', False),
                     ('company_id', '!=', rec.company_id.id)], limit=1)
                if field:
                    raise ValidationError(
                        _('You cannot change the company, as this '
                          'Account Journal is assigned to Pos Config '
                          '(%s).' % field.name_get()[0][1]))
