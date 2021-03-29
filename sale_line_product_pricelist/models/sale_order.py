# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    product_pricelist_items = fields.Text(string="Priceslists",compute='_compute_pricelist_items')
    
    @api.depends('product_id')
    def _compute_pricelist_items(self):
        for line in self:
            priceslist_items_str = ''
            if line.product_id:
                domain = [('product_id', '=', line.product_id.id)]
                priceslist_items = self.env['stock.quant'].search(domain)
                priceslist_items_str = '|'.join([(item.location_id.name +" : " + str(item.quantity-item.reserved_quantity)+ " "+ str(item.product_uom_id.name)) for item in priceslist_items])
            line.product_pricelist_items = priceslist_items_str 
