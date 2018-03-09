from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    @api.multi
    @api.constrains('company_id', 'pos_statement_id')
    def _check_company_id_pos_statement_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.pos_statement_id.company_id and\
                    rec.company_id != rec.pos_statement_id.company_id:
                raise ValidationError(
                    _('The Company in the Account Bank Statement Line and in '
                      'Pos Order must be the same.'))
