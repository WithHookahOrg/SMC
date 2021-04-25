# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMoveInh(models.Model):
    _inherit = 'account.move'

    customer_balance = fields.Float('Balance', compute='compute_customer_balance')

    def compute_customer_balance(self):
        for rec in self:
            invoices = self.env['res.partner'].search([('id', '=', rec.partner_id.id)])
            rec.customer_balance = invoices.total_due


# class AccountPaymentInh(models.Model):
#     _inherit = 'account.payment'
#
#     user_id = fields.Many2one('res.users')
#     sale_ids = fields.Many2many('sale.order')
#
#     @api.onchange('sale_ids')
#     def onchange_get_customer(self):
#         if self.sale_ids:
#             for rec in self:
#                 rec.user_id = rec.sale_ids[0].user_id.id
#                 rec.partner_id = rec.sale_ids[0].partner_id.id
#
#
# class StockPickingInh(models.Model):
#     _inherit = 'stock.picking'
#
#     def action_assign(self):
#         payments = self.env['account.payment'].search([('partner_id', '=', self.partner_id.id), ('state', '=', 'posted')])
#         if payments:
#             sale_order = self.env['sale.order'].search([('name', '=', self.origin)])
#             for rec in payments:
#                 if sale_order.id in rec.sale_ids.ids:
#                     record = super(StockPickingInh, self).action_assign()