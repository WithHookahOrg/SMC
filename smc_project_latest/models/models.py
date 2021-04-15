# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class smc(models.Model):
    _inherit = 'product.template'

    sale_discontinued = fields.Boolean("Sales Discontinued Products", compute="_compute_on_hand")

    def _compute_on_hand(self):
        for i in self:
            if i.type == 'product':
                if i.qty_available <= 0 and i.purchase_ok == False:
                    i.sale_discontinued = True
                    i.sale_ok = False
                else:
                    i.sale_ok = True
                    i.sale_discontinued = False
            else:
                i.sale_discontinued = False


class in_invoicing(models.Model):
    _inherit = 'account.move'

    delivery_order = fields.Many2one('stock.picking', compute='_compute_global')
    create_user = fields.Many2one('res.users', string='User', compute="compute_self_id")
    sale_origin = fields.Many2one('sale.order', compute='_compute_sale_origin')
    purchase_origin = fields.Many2one('purchase.order',  compute='_compute_purchase_origin')

    def _compute_purchase_origin(self):
        for i in self:
            record = self.env['purchase.order'].search([('name', '=', i.invoice_origin)], limit=1)
            i.purchase_origin = record.id

    def _compute_sale_origin(self):
        for i in self:
            record = self.env['sale.order'].search([('name', '=', i.invoice_origin)], limit=1)
            i.sale_origin = record.id

    def compute_self_id(self):
        for i in self:
            i.create_user = i.env.uid

    def _compute_global(self):
        for i in self:
            record = self.env['stock.picking'].search([('origin', '=', i.invoice_origin)], limit=1)
            i.delivery_order = record.id


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('manager', 'Approval from Manager'), ('ceo', 'Approval from CEO'),
        ('sale', 'Sales Order'),
        ('done', 'Locked'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')

    max_discount = fields.Float(string='Max Disccount', compute='compute_max_disccount', default=0)

    allowed_discount = fields.Float(string='Allowed Disccount', related='create_user.allowed_discount')
    create_user = fields.Many2one('res.users', string='User', compute="compute_self_id")

    def compute_self_id(self):
        for i in self:
            i.create_user = i.env.uid

    def from_manager_approval(self):
        self.state = 'manager'

    def from_ceo_approval(self):
        self.state = 'ceo'

    def action_confirm(self):
        for sale_order in self:
            if sale_order.max_discount > sale_order.allowed_discount:
                raise UserError(
                    _('Your discount limit is lesser then allowed discount.Click on "Ask for Approval" for approval_so_po'))
        return super(SaleOrder, self).action_confirm()

    @api.onchange("order_line.discount")
    def compute_max_disccount(self):
        record = self.env['sale.order'].search([])
        for i in record:
            maximum = []
            diss = 0.0
            for rec in i.order_line:
                maximum.append(rec.discount)
            if maximum:
                diss = max(maximum)
                i.max_discount = diss
            else:
                i.max_discount = 0


class users_inherit(models.Model):
    _inherit = 'res.users'
    _description = 'adding to users table'

    allowed_discount = fields.Float(string='Discount Allowed')


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    shipping_address = fields.Char(string='Shipping Address')
    create_user = fields.Many2one('res.users', string='User', compute="compute_self_id")
    sale_origin = fields.Many2one('sale.order', compute='_compute_sale_origin')
    purchase_origin = fields.Many2one('purchase.order', compute='_compute_purchase_origin')
    invoice_origin = fields.Many2one('account.move', compute='_compute_invoice_origin')

    def _compute_purchase_origin(self):
        for i in self:
            record = self.env['purchase.order'].search([('name', '=', i.origin)], limit=1)
            i.purchase_origin = record.id

    def _compute_invoice_origin(self):
        for i in self:
            record = self.env['account.move'].search([('invoice_origin', '=', i.origin)], limit=1)
            i.invoice_origin = record.id

    def _compute_sale_origin(self):
        for i in self:
            record = self.env['sale.order'].search([('name', '=', i.origin)], limit=1)
            i.sale_origin = record.id

    def compute_self_id(self):
        for i in self:
            i.create_user = i.sale_id.user_id.id
