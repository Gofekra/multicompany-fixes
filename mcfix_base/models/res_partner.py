from odoo import api, models, _
from odoo.exceptions import ValidationError


class Partner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    @api.depends('company_id')
    def name_get(self):
        names = super(Partner, self).name_get()
        res = self.add_company_suffix(names)
        return res

    @api.depends('is_company', 'name', 'parent_id.name', 'type',
                 'company_name')
    def _compute_display_name(self):
        # ugly change to ensure that the display name is correctly stored.
        # See https://github.com/odoo/odoo/issues/6276
        for rec in self:
            other = rec.with_context(not_display_company=True)
            super(Partner, other)._compute_display_name()
            rec.display_name = other.display_name

    @api.model
    def create(self, vals):
        """We need this to ensure that when the partner is created,
        associated to a company, we want to override the default company and
        take instead what the forced company if provided. Otherwise the
        partner of a company was being created inconsistent with the company
        that the partner belongs to."""
        if 'company_id' in self.env.context and 'company_id' not in vals:
            vals['company_id'] = self.env.context['company_id']
        return super(Partner, self).create(vals)

    @api.multi
    def _get_top_parent(self):
        parent = self.env['res.partner']
        for partner in self:
            if partner.parent_id:
                parent |= partner.parent_id._get_top_parent()
            else:
                parent |= self
        return parent

    @api.multi
    def _get_all_children(self):
        childs = self
        for partner in self:
            if partner.child_ids:
                childs |= partner.child_ids._get_all_children()
        return childs

    @api.multi
    def write(self, vals):
        """The partner hierarchy needs to be consistent company-wise. As a
        consequence, when a user changes the company of one partner, we will
        make sure that the whole partner hierarchy is updated with the new
        company."""
        company = False
        if vals.get('company_id') and \
                not self._context.get('stop_recursion_company'):
            company = vals['company_id']
            del vals['company_id']
        result = super(Partner, self).write(vals)
        if company and not self._context.get('stop_recursion_company'):
            top_partner = self._get_top_parent()
            partners = top_partner._get_all_children()
            partners = partners.filtered(lambda p: p.company_id)
            partners |= self
            result = result and partners.with_context(
                stop_recursion_company=True).write(
                {'company_id': company})
        return result

    @api.multi
    @api.constrains('company_id', 'parent_id')
    def _check_company_id_parent_id(self):
        for rec in self.sudo():
            if not rec.parent_id.check_company(rec.company_id):
                raise ValidationError(
                    _('The Company in the Res Partner and in '
                      'the parent Res Partner must be the same.'))

    @api.constrains('company_id')
    def _check_company_id_out_model(self):
        self._check_company_id_base_model()

    def _check_company_id_fields(self):
        res = super()._check_company_id_fields()
        res += [self.child_ids, self.bank_ids, ]
        return res

    def _check_company_id_search(self):
        res = super(Partner, self)._check_company_id_search()
        res += [
            ('res.partner', [('parent_id', '=', self.id)]),
            ('res.partner', [('commercial_partner_id', '=', self.id)]),
        ]
        return res
