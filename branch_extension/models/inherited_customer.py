# Part of BrowseInfo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResPartnerIn(models.Model):
    _inherit = 'res.partner'
    
    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self._context.get('my_branch'):
            args +=  [('branch_id','!=',False),('branch_id','in',[branch.id for branch in self.env.user.branch_ids])]
        return super(ResPartnerIn, self)._search(args, offset=offset, limit=limit, order=order, count=count, access_rights_uid=access_rights_uid)
        