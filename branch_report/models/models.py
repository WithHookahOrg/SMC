# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError
class BrachReport(models.Model):
    _inherit = 'account.payment'

    # def branch_report_action(self):
    #     pass
    five_th = fields.Integer(string="5000 x")
    one_th = fields.Integer(string="1000 x")
    five_hundred = fields.Integer(string='500 x')
    currency_note = fields.Boolean(string="Note", default= False)


    @api.onchange('partner_id')
    def curr_note_check(self):
        if self.partner_id:
            if self.partner_id.ceo_currency_check == True:
                self.currency_note = True
            elif self.partner_id.ceo_currency_check == False:
               self.currency_note = False



    def action_post(self):

        amnt_in_note = (5000 * self.five_th) + (1000 * self.one_th) + (500 * self.five_hundred)

        if self.partner_id.ceo_currency_check == True:
            if self.amount == amnt_in_note:
                res = super(BrachReport, self).action_post()
                return res
            else:
                raise UserError(_('Amount is not equal to Currency note.'))
        else:
            res = super(BrachReport, self).action_post()
            return res


class resPartner_CurrencyNote(models.Model):
    _inherit="res.partner"

    ceo_currency_check= fields.Boolean(string="Currency Note", default=False)

