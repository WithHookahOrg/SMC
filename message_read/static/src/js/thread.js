odoo.define('message_read.abstract_custom', function (require) {
"use strict";
var Widget = require('web.Widget');
var getMainAbstract = require('mail.model.AbstractMessage');
var time = require('web.time');
var LineRenderer = getMainAbstract.include({
   init: function (parent, data) {
        this._attachmentIDs = data.attachment_ids || [];
        this._body = data.body || "";
        // by default: current datetime
        this._date = data.date ? moment(time.str_to_datetime(data.date)) : moment();
        this._id = data.id;
        this._isDiscussion = data.is_discussion;
        this._isNotification = data.is_notification;
        this._serverAuthorID = data.author_id;
        this._type = data.message_type || undefined;
        this._opened_str =data.opened || "";

        this._processAttachmentURL();
        this._attachmentIDs.forEach(function (attachment) {
            attachment.filename = attachment.filename || attachment.name || _t("unnamed");
        });
    },

    getopen: function () {
        return this._opened_str;
    },
});



return { LineRenderer: LineRenderer, };

});