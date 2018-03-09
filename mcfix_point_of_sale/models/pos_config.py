from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class PosConfig(models.Model):
    _inherit = 'pos.config'

    journal_id = fields.Many2one(
        domain="[('type', '=', 'sale'), ('company_id', '=', company_id)]",
    )
    journal_ids = fields.Many2many(
        domain="[('journal_user', '=', True ), "
               "('type', 'in', ['bank', 'cash']), "
               "('company_id', '=', company_id)]",
    )
    invoice_journal_id = fields.Many2one(
        domain="[('type', '=', 'sale'), ('company_id', '=', company_id)]",
    )
    stock_location_id = fields.Many2one(
        domain="[('usage', '=', 'internal'),"
               "'|',('company_id','=',False),('company_id','=',company_id)]",
    )

    @api.multi
    @api.depends('company_id')
    def name_get(self):
        names = super(PosConfig, self).name_get()
        res = self.add_company_suffix(names)
        return res

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id and self.journal_ids:
            self.journal_ids = self.env['account.journal'].search(
                [('journal_user', '=', True),
                 ('type', 'in', ['bank', 'cash']),
                 ('company_id', '=', self.company_id.id)])
        if self.company_id and self.journal_id.company_id and \
                self.journal_id.company_id != self.company_id:
            self.journal_id = self.env['account.journal'].search([
                ('company_id', '=', self.company_id.id),
                ('type', '=', 'sale')
            ], limit=1)
            self.invoice_journal_id = self.journal_id
        if self.company_id and self.tip_product_id.company_id and \
                self.tip_product_id.company_id != self.company_id:
            self.tip_product_id = False
        if self.company_id and self.pricelist_id.company_id and \
                self.pricelist_id.company_id != self.company_id:
            self.pricelist_id = self.tip_product_id.pricelist_id
        if self.company_id and self.stock_location_id.company_id and \
                self.stock_location_id.company_id != self.company_id:
            self.stock_location_id = self.env['stock.warehouse'].search(
                [('company_id', '=', self.company_id.id)], limit=1
            ).lot_stock_id
        if self.company_id and self.default_fiscal_position_id.company_id and \
                self.default_fiscal_position_id.company_id != self.company_id:
            self.default_fiscal_position_id = False
        # if self.company_id and self.sequence_id.company_id and \
        #         self.sequence_id.company_id != self.company_id:
        #     self.sequence_id = False
        # if self.company_id and self.sequence_line_id.company_id and \
        #         self.sequence_line_id.company_id != self.company_id:
        #     self.sequence_line_id = False
        # if self.company_id and self.available_pricelist_ids:
        #     self.available_pricelist_ids = self.env['product.pricelist'].\
        #         search(
        #             [('____id', '=', self.id),
        #              ('company_id', '=', False),
        #              ('company_id', '=', self.company_id.id)])
        # if self.company_id and self.journal_ids:
        #     self.journal_ids = self.env['account.journal'].search(
        #             [('____id', '=', self.id),
        #              ('company_id', '=', False),
        #              ('company_id', '=', self.company_id.id)])
        # if self.company_id and self.fiscal_position_ids:
        #     self.fiscal_position_ids = self.env['account.fiscal.position'].\
        #         search(
        #             [('____id', '=', self.id),
        #              ('company_id', '=', False),
        #              ('company_id', '=', self.company_id.id)])

    @api.multi
    @api.constrains('company_id', 'invoice_journal_id')
    def _check_company_id_invoice_journal_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.invoice_journal_id.company_id and\
                    rec.company_id != rec.invoice_journal_id.company_id:
                raise ValidationError(
                    _('The Company in the Pos Config and in '
                      'Account Journal must be the same.'))

    @api.multi
    @api.constrains('company_id', 'journal_id')
    def _check_company_id_journal_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.journal_id.company_id and\
                    rec.company_id != rec.journal_id.company_id:
                raise ValidationError(
                    _('The Company in the Pos Config and in '
                      'Account Journal must be the same.'))

    @api.multi
    @api.constrains('company_id', 'pricelist_id')
    def _check_company_id_pricelist_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.pricelist_id.company_id and\
                    rec.company_id != rec.pricelist_id.company_id:
                raise ValidationError(
                    _('The Company in the Pos Config and in '
                      'Product Pricelist must be the same.'))

    @api.multi
    @api.constrains('company_id', 'sequence_line_id')
    def _check_company_id_sequence_line_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.sequence_line_id.company_id and\
                    rec.company_id != rec.sequence_line_id.company_id:
                raise ValidationError(
                    _('The Company in the Pos Config and in '
                      'Ir Sequence must be the same.'))

    @api.multi
    @api.constrains('company_id', 'stock_location_id')
    def _check_company_id_stock_location_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.stock_location_id.company_id and\
                    rec.company_id != rec.stock_location_id.company_id:
                raise ValidationError(
                    _('The Company in the Pos Config and in '
                      'Stock Location must be the same.'))

    @api.multi
    @api.constrains('company_id', 'default_fiscal_position_id')
    def _check_company_id_default_fiscal_position_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.default_fiscal_position_id.company_id \
                    and rec.company_id != rec.default_fiscal_position_id.\
                    company_id:
                raise ValidationError(
                    _('The Company in the Pos Config and in '
                      'Account Fiscal Position must be the same.'))

    @api.multi
    @api.constrains('company_id', 'tip_product_id')
    def _check_company_id_tip_product_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.tip_product_id.company_id and\
                    rec.company_id != rec.tip_product_id.company_id:
                raise ValidationError(
                    _('The Company in the Pos Config and in '
                      'Product Product must be the same.'))

    @api.multi
    @api.constrains('company_id', 'available_pricelist_ids')
    def _check_company_id_available_pricelist_ids(self):
        for rec in self.sudo():
            for line in rec.available_pricelist_ids:
                if rec.company_id and line.company_id and\
                        rec.company_id != line.company_id:
                    raise ValidationError(
                        _('The Company in the Pos Config and in '
                          'Product Pricelist (%s) must be the same.'
                          ) % line.name_get()[0][1])

    @api.multi
    @api.constrains('company_id', 'journal_ids')
    def _check_company_id_journal_ids(self):
        for rec in self.sudo():
            for line in rec.journal_ids:
                if rec.company_id and line.company_id and\
                        rec.company_id != line.company_id:
                    raise ValidationError(
                        _('The Company in the Pos Config and in '
                          'Account Journal (%s) must be the same.'
                          ) % line.name_get()[0][1])

    @api.multi
    @api.constrains('company_id', 'fiscal_position_ids')
    def _check_company_id_fiscal_position_ids(self):
        for rec in self.sudo():
            for line in rec.fiscal_position_ids:
                if rec.company_id and line.company_id and\
                        rec.company_id != line.company_id:
                    raise ValidationError(
                        _('The Company in the Pos Config and in '
                          'Account Fiscal Position (%s) must be the same.'
                          ) % line.name_get()[0][1])

    @api.multi
    @api.constrains('company_id', 'sequence_id')
    def _check_company_id_sequence_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.sequence_id.company_id and\
                    rec.company_id != rec.sequence_id.company_id:
                raise ValidationError(
                    _('The Company in the Pos Config and in '
                      'Ir Sequence must be the same.'))
