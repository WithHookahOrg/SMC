# -*- coding: utf-8 -*-

from odoo import models, fields, api

# -*- coding: utf-8 -*-

from odoo import models, fields, api


# class erum_module(models.Model):
#     _name = 'erum_module.erum_module'
#     _description = 'erum_module.erum_module'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
class product_templ_inherit_stock(models.Model):
    _inherit="product.template"

    stock_id= fields.Many2one('stock.quant',string="stock_id", )
    reserved_qty= fields.Float(string='reserved quants', compute="calc_reserve")
    reserved_qty1 = fields.Float(string="reserved quantss", related="stock_id.reserved_quantity")
    
    
    def calc_reserve(self):
        for rec in self:
            prd_resrv_qty=0.0
            # reserve_stk_move=self.env['stock.move'].search([('product_tmpl_id','=',rec.id),('picking_id.state','=','assigned')])
            reserve_stk_move = self.env['stock.picking'].search([('state','=','assigned'),('product_id.product_tmpl_id','=',rec.id),('picking_type_id.code', '=', 'outgoing')])
            quants = self.env['stock.quant'].search([('product_tmpl_id', '=', rec.id)])
            # quants=self.env['stock.quant']._gather(ol.product_id.product_tmpl_id, ol.location_id)
            for rsrvqt in quants:
                prd_resrv_qty = prd_resrv_qty + rsrvqt.reserved_quantity

            #prd_rsrv=reserve_stk_move.move_ids_without_package.filtered(lambda r: r.product_id.product_tmpl_id == rec)
            # for rec1 in reserve_stk_move:
            #     for ol in rec1.move_ids_without_package:
            #         if ol.product_id.product_tmpl_id == rec:
            #             quants= self.env['stock.quant'].search([('product_tmpl_id', '=', rec.id)])
            #             # quants=self.env['stock.quant']._gather(ol.product_id.product_tmpl_id, ol.location_id)
            #             for rsrvqt in quants:
            #                 prd_resrv_qty= prd_resrv_qty + rsrvqt.reserved_quantity
            #
            #     # self.env['stock.quant']._gather(ol.product_id.product_tmpl_id, locat)
            #     # for ol in rec1.move_ids
            #             #prd_resrv_qty= prd_resrv_qty+ol.forecast_availability

            rec.reserved_qty=prd_resrv_qty

    def action_open_quants_do(self):
        print(self)
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        action['domain'] = [('product_id.product_tmpl_id', '=', self.id),('picking_type_id.code', '=', 'outgoing'),('state','=','assigned')]
        return action

    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #     res = super(product_templ_inherit_stock, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
    #                                                submenu=submenu)
    #     if self.env.user.has_group("erum_module.group_create_products") ==False:
    #         for access_id in self.env['ir.model'].search([('name', '=', 'Product Template')]).access_ids:
    #             #if access_id.group_id.name != "Create Product Test":
    #             access_id.sudo().write({'perm_create': False})
    #     elif(self.env.user.has_group("erum_module.group_create_products") ==True):
    #         for access_id in self.env['ir.model'].search([('name', '=', 'Product Template')]).access_ids:
    #             #if access_id.group_id.name != "Create Product Test":
    #             access_id.sudo().write({'perm_create': True})
    #
    #         s=''
    #     return res
class product_product_inherit_stock(models.Model):
    _inherit="product.product"

    reserved_qty= fields.Float(string='reserved quants', compute="calc_reserve")

    def calc_reserve(self):
        for rec in self:
            prd_resrv_qty=0.0
            # reserve_stk_move=self.env['stock.move'].search([('product_tmpl_id','=',rec.id),('picking_id.state','=','assigned')])
            reserve_stk_move = self.env['stock.picking'].search([('state','=','assigned'),('product_id','=',rec.id),('picking_type_id.code', '=', 'outgoing')])
            #prd_rsrv=reserve_stk_move.move_ids_without_package.filtered(lambda r: r.product_id.product_tmpl_id == rec)
            # for rec1 in reserve_stk_move:
            #     for ol in rec1.move_ids_without_package:
            #         if ol.product_id == rec:
            #
            #
            #             prd_resrv_qty= prd_resrv_qty+ol.forecast_availability
            quants = self.env['stock.quant'].search([('product_id', '=', rec.id)])
            # quants=self.env['stock.quant']._gather(ol.product_id.product_tmpl_id, ol.location_id)
            for rsrvqt in quants:
                prd_resrv_qty = prd_resrv_qty + rsrvqt.reserved_quantity
            rec.reserved_qty=prd_resrv_qty

    def action_open_quants_do(self):
        print(self)
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("stock.action_picking_tree_all")
        action['domain'] = [('product_id', '=', self.id),('picking_type_id.code', '=', 'outgoing'),('state','=','assigned')]
        return action






# class reserved_quantity(models.Model):
#     _name = 'reserved_quantity.reserved_quantity'
#     _description = 'reserved_quantity.reserved_quantity'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
