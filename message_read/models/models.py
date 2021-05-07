# -*- coding: utf-8 -*-

import base64
import datetime
import psycopg2
import smtplib
import threading
from collections import defaultdict
from odoo.addons.base.models.ir_mail_server import MailDeliveryException
from odoo.tools.safe_eval import safe_eval
from odoo import models, fields, api, tools, _, modules
from werkzeug import urls
from odoo.tools import pycompat, ustr
import re
from binascii import Error as binascii_error
import logging
import werkzeug.urls

_logger = logging.getLogger(__name__)
_image_dataurl = re.compile(r'(data:image/[a-z]+?);base64,([a-z0-9+/\n]{3,}=*)\n*([\'"])(?: data-filename="([^"]*)")?', re.I)


class InheritMessage(models.Model):
    _inherit = 'mail.message'

    opened = fields.Datetime(help='Date when the email has been opened the first time')

    def set_opened(self, message_id=None):
        message = self.env['mail.message'].search([('id', '=', message_id)])
        message.write({'opened': fields.Datetime.now()})
        print("opened set")
        return message


    def message_format(self):
        
        vals_list = self._message_format(self._get_message_format_fields())
        com_id = self.env['ir.model.data'].xmlid_to_res_id('mail.mt_comment')
        note_id = self.env['ir.model.data'].xmlid_to_res_id('mail.mt_note')

        for vals in vals_list:
            message_sudo = self.browse(vals['id']).sudo().with_prefetch(self.ids)
            notifs = message_sudo.notification_ids.filtered(lambda n: n.res_partner_id)
            vals.update({
                'needaction_partner_ids': notifs.filtered(lambda n: not n.is_read).res_partner_id.ids,
                'history_partner_ids': notifs.filtered(lambda n: n.is_read).res_partner_id.ids,
                'is_note': message_sudo.subtype_id.id == note_id,
                'is_discussion': message_sudo.subtype_id.id == com_id,
                'subtype_description': message_sudo.subtype_id.description,
                'is_notification': vals['message_type'] == 'user_notification',
                'opened': vals['opened'] or None,
            })
            if vals['model'] and self.env[vals['model']]._original_module:
                vals['module_icon'] = modules.module.get_module_icon(self.env[vals['model']]._original_module)
        return vals_list


    def _get_message_format_fields(self):
        return [
            'id', 'body', 'date', 'author_id', 'email_from',  # base message fields
            'message_type', 'subtype_id', 'subject',  # message specific
            'model', 'res_id', 'record_name',  # document related
            'channel_ids', 'partner_ids',  # recipients
            'starred_partner_ids',  # list of partner ids for whom the message is starred
            'moderation_status',
            'opened',  # Date when the email has been opened the first time
        ]


class InhertMail(models.Model):
    _inherit = 'mail.mail'

    @api.model
    def create(self, values):
        # notification field: if not set, set if mail comes from an existing mail.message
        if values.get('mail_message_id'):
            tracking_url = self._get_tracking_url(values['mail_message_id'])
            if tracking_url:
                values['body_html'] = tools.append_content_to_html(values['body_html'], tracking_url, plaintext=False,
                                                              container_tag='div')

        if 'notification' not in values and values.get('mail_message_id'):
            values['notification'] = True
        new_mail = super(InhertMail, self).create(values)
        if values.get('attachment_ids'):
            new_mail.attachment_ids.check(mode='read')
        return new_mail

    def _get_tracking_url(self, message_id):
        base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        track_url = werkzeug.urls.url_join(
            base_url, 'message/track/%(message_id)s/blank.gif?%(params)s' % {
                'message_id': message_id,
                'params': werkzeug.urls.url_encode({'db': self.env.cr.dbname})
            }
        )
        return '<img src="%s" alt=""/>' % track_url
