# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
import datetime
from datetime import datetime, timedelta


class ReportAccountHashIntegrity(models.AbstractModel):
    _name = 'report.branch_report.branch_report_id'
    _description = 'Get hash integrity result as PDF.'

    # @api.model
    # def _get_report_values(self, docids, data=None, DATETIME_FORMAT=None):
    #     date_from = data['form']['date_from']
    #     date_to = data['form']['date_to']
    #     selected_id = data['form']['branch']
    #
    #     # SO = self.env['account.payment']
    #     # date_from = datetime.strptime(date_from)
    #     # start_date = datetime.strptime(date_start, DATE_FORMAT)
    #     # date_to = datetime.strptime(date_to)
    #     delta = timedelta(days=1)
    #
    #     total_values = []
    #     # while date_from <= date_to:
    #     #     date = date_from
    #     # date_from += delta
    #
    #     # print(date, date_from)
    #     # orders = self.env['account.payment'].search([('branch_id.id', '=', selected_id)])
    #     orders = self.env['account.payment'].search([])
    #     # orders = SO.search([('date', '>=', date_from.strftime(DATETIME_FORMAT)), ('date', '<', date_to.strftime(DATETIME_FORMAT)),  ('branch_id.id', '=', selected_id)
    #
    #     total_orders = len(orders)
    #     amount_total = sum(order.amount for order in orders)
    #
    #     total_values.append({
    #         # 'date': date.strftime("%Y-%m-%d"),
    #         # 'date': date.strftime("%Y-%m-%d"),
    #         # 'total_orders': total_orders,
    #         'amount_total': amount_total,
    #         'company': self.env.user.company_id
    #     })
    #
    #     return {
    #         'doc_ids': data['ids'],
    #         'doc_model': 'account.payment',
    #         'date_from': date_from,
    #         'date_to': date_to,
    #         'docs': total_values,
    #     }

    def calc_total_balance(self, cus_mod):
        lst_db = []
        lst_cr = []
        total_debit = 0.0
        total_credit = 0.0

        for crdbt in cus_mod:
            if crdbt.debit:
                lst_db.append(crdbt.debit)
            else:
                lst_db.append(0.0)

            if crdbt.credit:
                lst_cr.append(crdbt.credit)

            else:
                lst_cr.append(0.0)

        for tot_deb in lst_db:
            total_debit = total_debit + tot_deb

        tot_debit = int(round(total_debit))

        for tot_cr in lst_cr:
            total_credit = total_credit + tot_cr

        tot_credit = int(round(total_credit))

        total_bal = tot_debit - tot_credit

        return total_bal

    @api.model
    def _get_report_values(self, docids, data=None):
        date_from = data['form']['date_from']
        date_to = data['form']['date_to']
        selected_id = data['form']['branch'][-3]
        print("Data", data)
        # c = selected_id[0]
        model = self.env.context.get('active_model')
        docs = self.env[model].browse(self.env.context.get('active_id'))
        all_val = self.env['account.payment'].search([])
        c = []

        # for i in all_val:
        #     c.append({
        #         "partner_type": i.partner_type,
        #     })
        # d = c['partner_type'] = 'customer'
        # e = d

        all_payment = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to), ('branch_id.id', '=', selected_id),  ('state', '=', 'posted'),('move_type', '=', 'entry')])
        branch_name = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to),  ('state', '=', 'posted'),('branch_id.id', '=', selected_id)], limit=1)
        customer_type = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to), ('branch_id.id', '=', selected_id),  ('state', '=', 'posted'),('partner_type','=', 'customer')])
        customer_type_vendor = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to), ('state', '=', 'posted'),('branch_id.id', '=', selected_id),('partner_type','=', 'supplier')])
        customer_method = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to),  ('state', '=', 'posted'),('branch_id.id', '=', selected_id),('payment_method_id', '=', 'Checks')])
        curncy_note = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to),  ('state', '=', 'posted'),('branch_id.id', '=', selected_id),('partner_id.ceo_currency_check','=',True)])
        account_move_line = self.env['account.move'].search([('date', '>=', date_from),('date', '<=', date_to),('journal_id', '=', 'Miscellaneous Operations'),('branch_id.id', '=', selected_id),('state', '=', 'posted')])
        # account_move_line = self.env['account.move'].search([('journal_id', '=', 'Miscellaneous Operations')])
        account_line = []
        account_line1 = []

        account_move_line_data = self.env['account.move.line'].search([('date', '>=', date_from),('date', '<=', date_to),('journal_id.name', '=', 'Miscellaneous Operations'),('move_id.branch_id.id', '=', selected_id),('move_id.state', '=', 'posted')])



        acc_data=[]

        for dt in account_move_line_data:
            val_updated = False
            if dt.account_id.name == 'Refreshment':
                s=''
            for acc in acc_data:
                ac_id= acc['acc_id']
                nm= acc['name']
                bal = acc['bal']
                if ac_id == dt.account_id.id:
                    acount_total_bal =  self.calc_total_balance(dt)
                    acc['bal'] = acc['bal']+acount_total_bal
                    val_updated = True


            else:
                if val_updated == False:
                    acc_total_balance= self.calc_total_balance(dt)
                    acc_data.append({
                        'acc_id':dt.account_id.id,
                        'name'  : dt.account_id.name,
                        'bal'   : acc_total_balance
                    })


        # name = account_line[]
        for i in account_move_line.line_ids:
            debit = i.debit
            c = debit
            if debit==0.0:
                account_line1.append({
                    'name': i.account_id.name,
                    'debit': i.debit,
                })
            else:
                account_line.append({
                    'name': i.account_id.name,
                    'debit': i.debit,
                })

        keys = []
        for i in account_line:
            for key in i.keys():
                keys.append(key)
        # zero = []
        # non_zero = []
        # for i in account_line[1]:
        #     if i==0:
        #         zero.append({
        #             'name': i.account_id.name,
        #             'debit': i.debit,
        #         })
        #     else:
        #         non_zero.append({
        #             'name': i.account_id.name,
        #             'debit': i.debit,
        #         })
        all_payment1 = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to), ('branch_id.id', '=', selected_id), ('move_type', '=', 'out_invoice')])
        out_refund = self.env['account.move'].search([('date', '>=', date_from),('date', '<=', date_to), ('branch_id.id', '=', selected_id), ('move_type', '=', 'out_refund')])
        all_payment_2 = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to), ('branch_id.id', '=', selected_id), ('move_type', '=', 'in_invoice')])
        purchase_receipt = self.env['account.payment'].search([('date', '>=', date_from),('date', '<=', date_to), ('branch_id.id', '=', selected_id), ('move_type', '=', 'in_receipt')])
        # stock_move = self.env['stock.picking'].search([('date_done', '>=', date_from),('date_done', '<=', date_to), ('branch_id.id', '=', selected_id.id)])
        # all_payment = self.env['account.payment'].search([('branch_id.id', '=', selected_id)])

        out_refund_list = []

        for i in out_refund:
            out_refund_list.append({
                "partner_id": i.partner_id.name,
                "amount": i.amount_total,
                # "payment_type": i.payment_type,
                # "journal_id": i.journal_id,
                # "journal_id_name": i.journal_id.name,
                # "journal_name": i.journal_id.name,
                # "partner_type": i.partner_type,
                # 'branch_id': i.branch_id.id
            })

        branch_name = branch_name.branch_id.name
        d = purchase_receipt
        customer_method_list = []
        for i in customer_method:
            customer_method_list.append({
                "partner_id": i.partner_id.name,
                "amount": i.amount,
                "payment_type": i.payment_type,
                "journal_id": i.journal_id,
                "journal_id_name": i.journal_id.name,
                "journal_name": i.journal_id.name,
                "partner_type": i.partner_type,
                'branch_id': i.branch_id.id
            })
        customer_vendor_list = []
        for customer in customer_type_vendor:
            customer_vendor_list.append({
                "partner_id": customer.partner_id.name,
                "amount": customer.amount,
                "payment_type": customer.payment_type,
                "journal_id": customer.journal_id,
                "journal_name": customer.journal_id.name,
                "partner_type": customer.partner_type,
                'branch_id': customer.branch_id.id
            })

        customer_list = []
        for customer in customer_type:
            customer_list.append({
                "partner_id": customer.partner_id.name,
                "amount": customer.amount,
                "payment_type": customer.payment_type,
                "journal_id": customer.journal_id,
                "journal_name": customer.journal_id.name,
                "partner_type": customer.partner_type,
                'branch_id': customer.branch_id.id,
                'branch_name': customer.branch_id.name,
            })

        total_values = []
        for i in all_payment:
            total_values.append({
                "partner_id": i.partner_id.name,
                "amount": i.amount,
                "payment_type":i.payment_type,
                "journal_id":i.journal_id,
                "partner_type": i.partner_type,
                'branch_id': i.branch_id.id
            })


        five_th_notes=0
        one_th_notes =0
        five_hndrd_notes =0
        for note in curncy_note:
            five_th_notes = five_th_notes + note.five_th
            one_th_notes   = one_th_notes  + note.one_th
            five_hndrd_notes  = five_hndrd_notes + note.five_hundred


        return {
            'doc_ids': docids,
            'doc_model': 'account.payment',
            'data': data,
            'docs': docs,
            'total_values': total_values,
            'customer_list': customer_list,
            'customer_vendor_list': customer_vendor_list,
            'branch_name': branch_name,
            'customer_method_list': customer_method_list,
            'account_line': account_line,
            'out_refund_list': out_refund_list,
            'acc_total_list':acc_data,
            'fivth_notes' :five_th_notes,
            'oneth_note' :one_th_notes,
            'five_hndrd' : five_hndrd_notes

        }
