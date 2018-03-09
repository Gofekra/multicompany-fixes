from odoo import api, models, _
from odoo.exceptions import ValidationError


class PosOrder(models.Model):
    _inherit = "pos.order"

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id and self.account_move.company_id and \
                self.account_move.company_id != self.company_id:
            self.account_move = False
        if self.company_id and self.partner_id.company_id and \
                self.partner_id.company_id != self.company_id:
            self.partner_id = False
            # self.partner_id = self.company_id.partner_id
        if self.company_id and self.fiscal_position_id.company_id and \
                self.fiscal_position_id.company_id != self.company_id:
            self.fiscal_position_id = self.invoice_id.fiscal_position_id
        if self.company_id and self.picking_id.company_id and \
                self.picking_id.company_id != self.company_id:
            self.picking_id = False
        if self.company_id and self.invoice_id.company_id and \
                self.invoice_id.company_id != self.company_id:
            self.invoice_id = False
        if self.company_id and self.pricelist_id.company_id and \
                self.pricelist_id.company_id != self.company_id:
            self.pricelist_id = self.config_id.pricelist_id

    @api.multi
    @api.constrains('company_id', 'account_move')
    def _check_company_id_account_move(self):
        for rec in self.sudo():
            if rec.company_id and rec.account_move.company_id and\
                    rec.company_id != rec.account_move.company_id:
                raise ValidationError(
                    _('The Company in the Pos Order and in '
                      'Account Move must be the same.'))

    @api.multi
    @api.constrains('company_id', 'partner_id')
    def _check_company_id_partner_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.partner_id.company_id and\
                    rec.company_id != rec.partner_id.company_id:
                raise ValidationError(
                    _('The Company in the Pos Order and in '
                      'Res Partner must be the same.'))

    @api.multi
    @api.constrains('company_id', 'fiscal_position_id')
    def _check_company_id_fiscal_position_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.fiscal_position_id.company_id and\
                    rec.company_id != rec.fiscal_position_id.company_id:
                raise ValidationError(
                    _('The Company in the Pos Order and in '
                      'Account Fiscal Position must be the same.'))

    @api.multi
    @api.constrains('company_id', 'picking_id')
    def _check_company_id_picking_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.picking_id.company_id and\
                    rec.company_id != rec.picking_id.company_id:
                raise ValidationError(
                    _('The Company in the Pos Order and in '
                      'Stock Picking must be the same.'))

    @api.multi
    @api.constrains('company_id', 'invoice_id')
    def _check_company_id_invoice_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.invoice_id.company_id and\
                    rec.company_id != rec.invoice_id.company_id:
                raise ValidationError(
                    _('The Company in the Pos Order and in '
                      'Account Invoice must be the same.'))

    @api.multi
    @api.constrains('company_id', 'pricelist_id')
    def _check_company_id_pricelist_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.pricelist_id.company_id and\
                    rec.company_id != rec.pricelist_id.company_id:
                raise ValidationError(
                    _('The Company in the Pos Order and in '
                      'Product Pricelist must be the same.'))

    @api.constrains('company_id')
    def _check_company_id_out_model(self):
        if not self.env.context.get('bypass_company_validation', False):
            for rec in self:
                if not rec.company_id:
                    continue
                field = self.env['pos.order.line'].search(
                    [('order_id', '=', rec.id),
                     ('company_id', '!=', False),
                     ('company_id', '!=', rec.company_id.id)], limit=1)
                if field:
                    raise ValidationError(
                        _('You cannot change the company, as this '
                          'Pos Order is assigned to Pos Order Line '
                          '(%s).' % field.name_get()[0][1]))
                field = self.env['account.bank.statement.line'].search(
                    [('pos_statement_id', '=', rec.id),
                     ('company_id', '!=', False),
                     ('company_id', '!=', rec.company_id.id)], limit=1)
                if field:
                    raise ValidationError(
                        _('You cannot change the company, as this '
                          'Pos Order is assigned to '
                          'Account Bank Statement Line (%s)'
                          '.' % field.name_get()[0][1]))


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.company_id and self.product_id.company_id and \
                self.product_id.company_id != self.company_id:
            self.product_id = False
        # if self.company_id and self.tax_ids:
        #     self.tax_ids = self.env['account.tax'].search(
        #             [('____id', '=', self.id),
        #              ('company_id', '=', False),
        #              ('company_id', '=', self.company_id.id)])
        if self.company_id and self.order_id.company_id and \
                self.order_id.company_id != self.company_id:
            self.order_id = False
        # if self.company_id and self.tax_ids_after_fiscal_position:
        #     self.tax_ids_after_fiscal_position = self.env['account.tax'].\
        #         search(
        #             [('____id', '=', self.id),
        #              ('company_id', '=', False),
        #              ('company_id', '=', self.company_id.id)])

    # @api.multi
    # @api.constrains('company_id', 'product_id')
    # def _check_company_id_product_id(self):
    #     for rec in self.sudo():
    #         if rec.company_id and rec.product_id.company_id and\
    #                 rec.company_id != rec.product_id.company_id:
    #             raise ValidationError(
    #                 _('The Company in the Pos Order Line and in '
    #                   'Product Product must be the same.'))

    @api.multi
    @api.constrains('company_id', 'tax_ids')
    def _check_company_id_tax_ids(self):
        for rec in self.sudo():
            for line in rec.tax_ids:
                if rec.company_id and line.company_id and\
                        rec.company_id != line.company_id:
                    raise ValidationError(
                        _('The Company in the Pos Order Line and in '
                          'Account Tax (%s) must be the same.'
                          ) % line.name_get()[0][1])

    @api.multi
    @api.constrains('company_id', 'order_id')
    def _check_company_id_order_id(self):
        for rec in self.sudo():
            if rec.company_id and rec.order_id.company_id and\
                    rec.company_id != rec.order_id.company_id:
                raise ValidationError(
                    _('The Company in the Pos Order Line and in '
                      'Pos Order must be the same.'))

    @api.multi
    @api.constrains('company_id', 'tax_ids_after_fiscal_position')
    def _check_company_id_tax_ids_after_fiscal_position(self):
        for rec in self.sudo():
            for line in rec.tax_ids_after_fiscal_position:
                if rec.company_id and line.company_id and\
                        rec.company_id != line.company_id:
                    raise ValidationError(
                        _('The Company in the Pos Order Line and in '
                          'Account Tax (%s) must be the same.'
                          ) % line.name_get()[0][1])
