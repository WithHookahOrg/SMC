# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import base64

import werkzeug

from odoo import _, exceptions, http, tools
from odoo.http import request
from odoo.tools import consteq


class MessageController(http.Controller):

    @http.route('/message/track/<int:message_id>/blank.gif', type='http',methods=['GET'], auth='public')
    def track_mail_open(self, message_id, **post):
        """ Email tracking. """
        request.env['mail.message'].sudo().set_opened(message_id)
        print("In controller")
        return 'hello'