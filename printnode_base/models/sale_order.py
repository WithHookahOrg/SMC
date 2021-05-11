from odoo import models


class SaleOrder(models.Model):
    _name = "sale.order"
    _inherit = ['sale.order', 'printnode.scenario.mixin']

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()

        if res is True:
            self.print_scenarios(action='print_document_on_sales_order')

            # Print picking
            if self.warehouse_id.delivery_steps == 'ship_only':
                picking_type_to_print = self.warehouse_id.out_type_id
            else:
                picking_type_to_print = self.warehouse_id.pick_type_id

            picking_ids = self.picking_ids.filtered(
                lambda p: p.picking_type_id == picking_type_to_print).ids

            self.print_scenarios(
                action='print_picking_document_after_so_confirmation',
                ids_list=picking_ids)
