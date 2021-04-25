# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ResPartnerInh(models.Model):
    _inherit = 'res.partner'

    customer_code = fields.Char('Customer Code', required=True, copy=False,
                                index=True, default=lambda self: _('New'))
    test = fields.Boolean("Test Field")
    no_cnic = fields.Char('CNIC')
    ntn = fields.Char('NTN')
    fax = fields.Char('Fax')

    beneficiary_name = fields.Char('Beneficiary Name')
    bank_name = fields.Char('Bank Name')
    address = fields.Char('Address')
    iban_no = fields.Char('IBAN NO.')
    swift_code = fields.Char('Swift Code')
    ac_no = fields.Char('Account No.')
    short_code = fields.Char('Short Code')
    purpose = fields.Char('Purpose')
    is_supplier = fields.Boolean(default=False, compute='compute_is_supplier')
    currency_id = fields.Many2one('res.currency')

    def compute_is_supplier(self):
        if self.supplier_rank > 0:
            self.is_supplier = True
        else:
            self.is_supplier = False

    @api.constrains('customer_code')
    def check_code(self):
        if self.customer_code:
            code = self.env['res.partner'].search([('customer_code', '=', self.customer_code)])
            if len(code) > 1:
                raise UserError('User Already Exist')

    def name_get(self):
        res = []
        for rec in self:
            res.append((rec.id, '%s : %s : %s' % (rec.customer_code, rec.name, str(rec.total_due))))
        return res

    @api.model
    def create(self, vals):
        if vals.get('customer_code', _('New')) == _('New'):
            vals['customer_code'] = self.env['ir.sequence'].next_by_code('res.partner.sequence') or _('New')
        result = super(ResPartnerInh, self).create(vals)
        return result


# class SaleOrderInh(models.Model):
#     _inherit = 'sale.order'
#
#     def action_confirm(self):
#         res = super(SaleOrderInh, self).action_confirm()
#         for order in self:
#             for picking in order.picking_ids:
#                 picking.do_unreserve()
#         return res


class StockPickingInh(models.Model):
    _inherit = 'stock.picking'

    user_id = fields.Many2one('res.users', related='sale_id.user_id')


