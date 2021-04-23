# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

MAP_INVOICE_TYPE_PARTNER_TYPE = {
    'out_invoice': 'customer',
    'out_refund': 'customer',
    'in_invoice': 'supplier',
    'in_refund': 'supplier',
}

class AccountPayment(models.Model):
    _inherit = 'account.payment'



    branch_id = fields.Many2one('res.branch')

    @api.onchange('branch_id')
    def onchange_get_branches(self):
        branches = self.env.user.branch_ids

        print(branches)

        return {'domain': {'branch_id': [('id', 'in', branches.ids)]}}

    @api.model_create_multi
    def create(self, vals_list):
        res= super(AccountPayment,self).create(vals_list)
        if res.branch_id:
            if res.move_id:
                for line in res.move_id.line_ids:
                    line.branch_id = res.branch_id
        return  res