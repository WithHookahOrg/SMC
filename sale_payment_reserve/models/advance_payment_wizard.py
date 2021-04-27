from datetime import datetime

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AdvancePaymentWizard(models.TransientModel):
    _name = 'advance.payment.wizard'
    _description = 'Advance Payment'

    amount = fields.Float('Advance Amount')
    order_amount = fields.Float('Order Amount')
    user_id = fields.Many2one('res.users')
    branch_id = fields.Many2one('res.branch')

    def default_payment_method_id(self):
        method = self.env['account.payment.method'].search([('name', '=', 'Manual')], limit=1)
        return method.id

    def default_journal_id(self):
        journal = self.env['account.journal'].search([('name', '=', 'Cash')])
        return journal.id

    journal_id = fields.Many2one('account.journal', default=default_journal_id)
    payment_method_id = fields.Many2one('account.payment.method', default=default_payment_method_id)
    ref = fields.Char('Reference')

    def default_currency_id(self):
        currency = self.env['res.currency'].search([('name', '=', 'PKR')])
        return currency.id

    currency_id = fields.Many2one('res.currency', default=default_currency_id)

    def create_data(self):
        model = self.env.context.get('active_model')
        rec = self.env[model].browse(self.env.context.get('active_id'))
        vals = {
            'journal_id': self.journal_id.id,
            'partner_id': rec.partner_id.id,
            'date': datetime.today().date(),
            'amount': self.amount,
            'currency_id': self.currency_id.id,
            'ref': self.ref,
            'user_id': self.user_id.id,
            'branch_id': self.branch_id.id,
            'state': 'draft',
        }
        payment = self.env['account.payment'].sudo().create(vals)
        payment.action_post()

