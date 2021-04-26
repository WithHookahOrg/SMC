# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

# from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase
# from addons.purchase.models.purchase import PurchaseOrder as Purchase


class PurchaseImportOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def _default_picking_type(self):
        return self._get_picking_type(self.env.context.get('company_id') or self.env.company.id)

    import_order = fields.Boolean(string="Import Order", default=False)
    state = fields.Selection([
        ('draft_new', 'Draft'),
        ('director', 'Approve'),
        ('ceo', 'Approve'),
        ('approved', 'Approved'),
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('to approve', 'To Approve'),
        ('purchase', 'Purchase Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled')
    ], string='Status', readonly=True, index=True, copy=False, default='draft_new', tracking=True)
    picking_type_id = fields.Many2one('stock.picking.type', 'Deliver To',
                                      required=True, default=_default_picking_type)

    @api.model
    def create(self, vals):
        company_id = vals.get('company_id', self.default_get(['company_id'])['company_id'])
        if 'import_order' in vals:
            if vals['import_order']:
                sequence = self.env.ref('purchase_import_order.seq_import_order_purchase')
                vals['name'] = sequence.next_by_id()
        rec = super(PurchaseImportOrder, self).create(vals)
        rec.state = 'draft_new'
        return rec

    def action_confirm(self):
        self.state = 'director'

    def action_approve_director(self):
        self.state = 'ceo'

    def action_approve_ceo(self):
        self.state = 'approved'

    def action_create_rfq(self):
        self.state = 'draft'