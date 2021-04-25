# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError,ValidationError

MAP_INVOICE_TYPE_PARTNER_TYPE = {
	'out_invoice': 'customer',
	'out_refund': 'customer',
	'in_invoice': 'supplier',
	'in_refund': 'supplier',
}

class AccountPayment(models.Model):
	_inherit = 'account.payment'

	# @api.model
	# def default_get(self, fields):
	# 	rec = super(AccountPayment, self).default_get(fields)
	# 	invoice_defaults = self.reconciled_invoice_ids
	# 	if invoice_defaults and len(invoice_defaults) == 1:
	# 		invoice = invoice_defaults[0]
	# 		rec['branch_id'] = invoice.branch_id.id
	# 	return rec
	#
	# branch_id = fields.Many2one('res.branch')

	branch_id = fields.Many2one('res.branch', default=lambda r: r.env.user.branch_id.id)

	@api.onchange('branch_id')
	def onchange_get_branches(self):
		branches = self.env.user.branch_ids

		print(branches)

		return {'domain': {'branch_id': [('id', 'in', branches.ids)]}}

	@api.model_create_multi
	def create(self, vals_list):
		res = super(AccountPayment, self).create(vals_list)
		if self.env.context.get('active_id', False) == False:
			if res.journal_id.type == 'bank':
				if res.cheques_payment == False and res.online_credit_payment == False and res.corporate_sale == False and res.other_receipt == False:
					raise UserError(_("Must select one option"))
		if res.branch_id:
			if res.move_id:
				for line in res.move_id.line_ids:
					line.branch_id = res.branch_id
		return res

