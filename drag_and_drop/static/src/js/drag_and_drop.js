odoo.define('drag_and_drop.dnd', function (require) {
    "use strict";

    var Chatter = require('mail.Chatter');
    var AttachmentBox = require('mail.AttachmentBox');
    var core = require('web.core');
    var QWeb = core.qweb;
    var framework = require('web.framework');
    var BasicComposer = require('mail.composer.Basic');
    var _t = core._t;
    var FormRenderer = require('web.FormRenderer');

    Chatter.include({
        init: function (parent, record, mailFields, options) {
            this._super.apply(this, arguments);
        },
        start: function () {
            this._super.apply(this, arguments);
        },
        /*
        @Override
        Never hide the "Attachemnt"-Icon in the chatter
        */
        _updateAttachmentCounter: function () {
            var count = this.record.data.message_attachment_count || 0;
            this.$('.o_chatter_attachment_button_count').html(' ('+ count +')');
            //this.$('.o_chatter_button_attachment').toggleClass('o_hidden', !count);
         }
    });

    AttachmentBox.include({
        events: _.extend(AttachmentBox.prototype.events, {
            'drop': '_onDrop',
            'dragover': '_onHoverDrop',
            'dragleave': '_onHoverLeave',
        }),
        init: function (parent, record) {
            this._super.apply(this, arguments);
            this.draggingTid = null;
            this.parent = parent;
        },
        start: function() {
            this._super.apply(this, arguments);
            var $content = $(QWeb.render("drag_and_drop.uploadFile", {
                widget: this
            }));
            $content.appendTo(this.$('.o_chatter_dnd_attachment'));
        },
        _onDrop: function (ev) {
            ev.preventDefault();
            this.$('.o_chatter_dnd_attachment').addClass('o_chatter_dnd_attachment_hidden');
            var self = this;
            var files = ev.originalEvent.dataTransfer.files;
            var file_counter = 0;
            var file_to_upload_content = 0;

            for(var f in files){
                if(typeof files[f] === 'object') file_to_upload_content++;
            }

            if(file_to_upload_content > 0)
                framework.blockUI();
            var $uploadform = this.$('form.o_form_binary_form');

            for(var f in files){
                var file = files[f];

                if(typeof file !== 'object') return;

                var serializeArray = $uploadform.serializeArray();
                var formData = new FormData();
                for(var a in serializeArray)
                    formData.append(serializeArray[a]["name"], serializeArray[a]['value']);
                formData.append("ufile", file, file.name);
                formData.set('csrf_token', core.csrf_token);
                formData.set('id', self.currentResID);
                formData.set('model', self.currentResModel);


                $.ajax({
                    url :$uploadform.prop('action'),
                    type: 'POST',
                    headers: {
                       'X-CSRF-TOKEN': core.csrf_token
                    },
                    data: formData,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function(response) {}
                }).done(function(){
                    file_counter++;
                    if (file_counter == file_to_upload_content) {
                        self.parent._closeAttachments();
                        self.parent._openAttachments();
                        self.parent.record.data.message_attachment_count += file_to_upload_content;
                        self.parent._updateAttachmentCounter();
                        framework.unblockUI();
                    }
                });
            }
        },
        _onHoverDrop: function (ev) {
            clearTimeout(this.tid);
            ev.stopPropagation();
            ev.preventDefault();
            this.$('.o_chatter_dnd_attachment').removeClass('o_chatter_dnd_attachment_hidden');
            return false
        },
        _onHoverLeave: function (ev) {
            this.tid = setTimeout(function(){
                ev.stopPropagation();
                ev.preventDefault();
                this.$('.o_chatter_dnd_attachment').addClass('o_chatter_dnd_attachment_hidden');
            }, 50);
            return false;
        },
    });

    BasicComposer.include({
        init: function (parent, record) {
            this._super.apply(this, arguments);
            this.draggingTid = null;
        },
        start: function () {
            this._super.apply(this, arguments);
            var $content = $(QWeb.render("drag_and_drop.dnd_area_chatter", {
                widget: this
            }));
            $content.appendTo($('div.o_thread_composer'))
            $('div.o_thread_composer').on('dragover', this._onHoverDrop);
            $('div.o_thread_composer').on('dragleave', this._onHoverLeave);
            $('div.o_thread_composer').on('drop', {'parent': this}, this._onDrop);

        },
        _uploadToComposer: function (files) {
            var self = this;
            var file_counter = 0;
            var file_to_upload_content = 0;
            var attachments = self.get('attachment_ids');
            _.each(files, function (file){
                var attachment = _.findWhere(attachments, {name: file.name});
                if (attachment){
                    self._attachmentDataSet.unlink([attachment.id]);
                    attachments = _.without(attachments, attachment);
                }
            });

            var uploadAttachments = _.map(files, function (file){
                return {
                    id: 0,
                    name: file.name,
                    filename: file.name,
                    url: '',
                    upload: true,
                    mimetype: '',
                };
            });
            attachments = attachments.concat(uploadAttachments);
            self.set('attachment_ids', attachments);

            for(var f in files){
                if(typeof files[f] === 'object') file_to_upload_content++;
            }

            if(file_to_upload_content > 0)
                framework.blockUI();
            var $uploadform = self.$('form.o_form_binary_form');

            for(var f in files){
                var file = files[f];

                if(typeof file !== 'object') return;

                var serializeArray = $uploadform.serializeArray();
                var formData = new FormData();
                for(var a in serializeArray)
                    formData.append(serializeArray[a]["name"], serializeArray[a]['value']);
                formData.append("ufile", file, file.name);
                formData.set('csrf_token', core.csrf_token);


                $.ajax({
                    url :$uploadform.prop('action'),
                    type: 'POST',
                    headers: {
                       'X-CSRF-TOKEN': core.csrf_token
                    },
                    data: formData,
                    cache: false,
                    contentType: false,
                    processData: false,
                    success: function(response) {
                        $('body').append(response);
                    }
                }).done(function(){
                    file_counter++;
                    if (file_counter == file_to_upload_content) {
                        framework.unblockUI();
                    }
                });
            }
        },
        _onDrop: function (ev) {
            ev.preventDefault();
            $('#dnd_area_chatter').addClass('o_chatter_dnd_attachment_hidden');

            var self = ev.data.parent;
            var files = ev.originalEvent.dataTransfer.files;
            self._uploadToComposer(files);
            console.log(files);
        },
        _onHoverDrop: function (ev) {
            clearTimeout(this.tid);
            ev.stopPropagation();
            ev.preventDefault();
            $('#dnd_area_chatter').removeClass('o_chatter_dnd_attachment_hidden');
            return false
        },
        _onHoverLeave: function (ev) {
            var self = this;
            this.tid = setTimeout(function(){
                ev.stopPropagation();
                ev.preventDefault();
                $('#dnd_area_chatter').addClass('o_chatter_dnd_attachment_hidden');
            }, 50);
            return false;
        },
    });

    FormRenderer.include({
        _updateView: function ($newContent) {
            var base = this._super.apply(this, arguments);
            if (this.mode == "readonly") {
                this._initAddScreenshot();
            }
            return base;
        },
        _initAddScreenshot: function() {
            var self = this;
            var cancel_fn = function(){
                $('#screenshot_modal').css('display', 'none');
                $('#screenshot_modal_bg').css('display', 'none');
            };
            if ($('screenshot_modal_bg').length===0){
                $('body').append('<div id="screenshot_modal_bg" class="modal-backdrop in" style="display:none;"></div>');
                $('body').append(''+
                '<div id="screenshot_modal" style="display: none;" class="modal o_technical_modal in">'+
                    '<div class="modal-dialog modal-lg">'+
                        '<div class="modal-content">'+
                            '<div class="modal-header">'+
                                '<h4 class="modal-title">'+_t('Upload Screenshot')+'<span class="o_subtitle text-muted small"></span></h4>'+
                                '<button type="button" class="close" id="screenshot_x" data-dismiss="modal" aria-label="Close" tabindex="-1">×</button>'+
                            '</div> '+
                            '<div class="modal-body o_act_window"><div class="o_view_manager_content"><div><div class="o_form_view o_form_nosheet o_form_editable">'+
                                '<div class="o_group"><tr>'+
                                    '<td class="o_td_label"><label class="o_form_label" for="screenshot_filename">'+_t('Filename')+'</label></td>'+
                                    '<td style="width: 100%;"><input class="o_field_char o_field_widget o_input" name="screenshot_filename" type="text" placeholder="" id="screenshot_filename" required></td>'+
                                '</tr></div>'+
                            '</div></div></div></div>'+
                            '<div class="modal-footer"><div><footer>'+
                                '<button type="object" class="btn btn-sm btn-success" id="screenshot_attachment"><span>'+_t('Upload to attachment(s)')+'</span></button>'+
                                '<button type="object" class="btn btn-sm btn-primary" id="screenshot_new_message"><span>'+_t('Upload to "Send message"')+'</span></button>'+
                                '<button type="object" class="btn btn-sm btn-light" id="screenshot_log_note"><span>'+_t('Upload to "Log note"')+'</span></button>'+
                                '<button class="btn btn-sm btn-default" id="screenshot_cancel"><span>'+_t('Cancel')+'</span></button>'+
                            '</footer></div></div>'+
                        '</div> '+
                    '</div>'+
                '</div> ');
                $('#screenshot_x').click(cancel_fn);
                $('#screenshot_cancel').click(cancel_fn);
                var $content = $(QWeb.render("drag_and_drop.uploadScreenshot", {
                    widget: this
                }));
                $content.appendTo($('#screenshot_modal'));
            }
            var modal = $('#screenshot_modal');
            var model_bg = $('#screenshot_modal_bg');

            document.onpaste = function (event) {
              if (self.mode !== "readonly") return;
              if ($('.o_content').find('.o_form_view').length === 0 ) return;
              var items = (event.clipboardData  || event.originalEvent.clipboardData).items;
              var blob = null;
              for (var i = 0; i < items.length; i++) {
                if (items[i].type.indexOf("image") === 0) {
                  blob = items[i].getAsFile();
                }
              }
              if (blob !== null) {
                  var d = new Date();
                  var nowMilliseconds = $.datepicker.formatDate('yy-mm-dd-', d) + d.getHours() + '-'+ d.getMinutes() + '-' + d.getSeconds() + '-' + d.getMilliseconds();
                  $('#screenshot_filename').val('Screenshot_'+nowMilliseconds);
                  model_bg.css('display','block');
                  modal.css('display','block');
                  $('#screenshot_attachment').unbind().click({
                    blob: blob,
                    cancel_fn: cancel_fn,
                    self: self
                  }, self.upload_screenshot_attachment);
                  $('#screenshot_new_message').unbind().click({
                    blob: blob,
                    cancel_fn: cancel_fn,
                    self: self,
                    isLog: false
                  }, self.open_composer_and_upload_screenshot);
                  $('#screenshot_log_note').unbind().click({
                    blob: blob,
                    cancel_fn: cancel_fn,
                    self: self,
                    isLog: true
                  }, self.open_composer_and_upload_screenshot);
              }
            }
        },

        open_composer_and_upload_screenshot(event) {
            var self = event.data.self;
            var isLog = event.data.isLog;
            if (isLog) {
                 if (self.chatter._composer !== undefined) {
                    if (self.chatter._composer.options.isLog !== isLog) {
                        self.chatter._onOpenComposerNote();
                    }
                 } else {
                    self.chatter._onOpenComposerNote();
                 }
            } else {
                if (self.chatter._composer !== undefined) {
                    if (self.chatter._composer.options.isLog !== isLog) {
                        self.chatter._onOpenComposerMessage();
                    }
                 } else {
                    self.chatter._onOpenComposerMessage();
                 }
            }
            var refreshIntervalId = setInterval(function() {
                if ($('.o_composer_send').length !== 0) {
                    if (self.chatter._composer.options.isLog === isLog) {
                        clearInterval(refreshIntervalId);
                        self.upload_screenshot_to_composer(event);
                        event.data.cancel_fn();
                    }
                }
            }, 100);
        },

        upload_screenshot_to_composer: function(event) {
            framework.blockUI();
            var self = event.data.self;
            var name = self.get_name_of_screenshot();
            var blob = self.create_blob(event, name);
            self.chatter._composer._uploadToComposer([blob]);
        },

        upload_screenshot_attachment: function(event) {
            var self = event.data.self;
            var name = self.get_name_of_screenshot();
            var blob = self.create_blob(event, name);
            var id = self.state.res_id;
            var model = self.state.model;

            framework.blockUI();

            var $uploadform = $('#screenshot_modal').find('form.o_form_binary_form');
            var serializeArray = $uploadform.serializeArray();
            var formData = new FormData();
            for(var a in serializeArray)
                formData.append(serializeArray[a]["name"], serializeArray[a]['value']);
            formData.append("ufile", blob, name);
            formData.set('csrf_token', core.csrf_token);
            formData.set('id', id);
            formData.set('model', model);

            $.ajax({
                url :$uploadform.prop('action'),
                type: 'POST',
                headers: {
                   'X-CSRF-TOKEN': core.csrf_token
                },
                data: formData,
                cache: false,
                contentType: false,
                processData: false,
                success: function(response) {}
            }).done(function(){
                self.chatter.record.data.message_attachment_count++;
                self.chatter._updateAttachmentCounter();
                framework.unblockUI();
            });
            event.data.cancel_fn();
        },

        get_name_of_screenshot() {
            return $('#screenshot_filename').val();
        },

        create_blob(event, name) {
            var blob = event.data.blob;
            var self = event.data.self;

            var id = self.state.res_id;
            var model = self.state.model;

            if (name.length !== 0){
                blob = new File([blob], name+'.png', {type: 'image/png'});;
            }
            return blob;
        }
    });
});