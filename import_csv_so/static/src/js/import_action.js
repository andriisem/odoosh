odoo.define('import_csv_so.import', function (require) {
    "use strict";
    
    var AbstractAction = require('web.AbstractAction');
    var ControlPanelMixin = require('web.ControlPanelMixin');
    var core = require('web.core');
    var session = require('web.session');
    var QWeb = core.qweb;
    var StateMachine = window.StateMachine;

    function jsonp(form, attributes, callback) {
        attributes = attributes || {};
        var options = {jsonp: _.uniqueId('import_callback_')};
        window[options.jsonp] = function () {
            delete window[options.jsonp];
            callback.apply(null, arguments);
        };
        if ('data' in attributes) {
            _.extend(attributes.data, options);
        } else {
            _.extend(attributes, {data: options});
        }
        _.extend(attributes, {
            dataType: 'script',
        });
        $(form).ajaxSubmit(attributes);
    }

    var ImportCustomCSV = AbstractAction.extend(ControlPanelMixin, { 
        template: 'ImportCustomView',
        events: {
            'change .oe_import_customer': 'select_customer',
            'change .oe_import_file': 'file_load',
        },
        
        init: function (parent, action) {
            this._super.apply(this, arguments);
            this.partner = action.partner
            this.partner_name = action.partner_name
        },

        start: function () {
            var self = this;
            
            return $.when(
                this._super(),
                self.create_model().done(function (id) {
                    self.id = id;
                    self.$('input[name=import_id]').val(id);
    
                    self.renderButtons();
                    if (self.partner) {
                        self.$('input[name="customer"]').trigger('change')
                    }
                    var status = {
                        cp_content: {$buttons: self.$buttons},
                    };

                    self.update_control_panel(status);
                })
            );
        },

        create_model: function() {
            return this._rpc({
                model: 'custom_csv.import',
                method: 'create',
                args: [{res_model: this.res_model}],
                kwargs: {context: session.user_context},
            });
        },

        renderButtons: function() {
            var self = this;
            this.$buttons = $(QWeb.render("ImportCsvView.buttons", this));
            this.$buttons.filter('.oe_select_customer').on('click', function (e) {
                self.do_action('import_csv_so.select_customer_action_kanban');
            });
            this.$buttons.filter('.oe_import_file').on('click', function () {
                self.$('.oe_import_file').click();
            });
            this.$buttons.filter('.o_import_import').on('click', this.import.bind(this));
            this.$buttons.filter('.o_import_cancel').on('click', function(e) {
                e.preventDefault();
                self.exit();
            });
        },

        onselected_customer: function () {
            this.$buttons.filter('.oe_select_customer').addClass('d-none');
            this.$buttons.filter('.oe_import_file').removeClass('d-none');
        },

        onfile_loaded: function () {            
            jsonp(this.$el, {
                url: '/custom_csv_import/set_file'
            }, this.proxy('settings_changed'));
        },

        onpreviewing: function () {
            this.$buttons.filter('.oe_import_file').addClass('d-none');
            this.$buttons.filter('.o_import_import').removeClass('d-none');
            
            var self = this;
            this._rpc({
                model: 'custom_csv.import',
                method: 'parse_preview',
                args: [this.id, this.partner],
                kwargs: {context: session.user_context},
            }).done(function (result) {
                self.result = result
                self.$('.oe_import_preview').html(
                    QWeb.render('ImportCsvView.preview.error', result));
                    if (result.error) {
                        self.$buttons.filter('.o_import_import').attr('disabled', 'disabled');
                    }
            });
        },

        onimported: function () {
            var self = this;
            this._rpc({
                model: 'custom_csv.import',
                method: 'csv_import_so',
                args: [this.id, this.result, this.partner],
                kwargs: {context: session.user_context},
            }).then(function (result) {
                self.do_action({
                    name: 'Imported Orders',
                    res_model: 'sale.order',
                    domain: [['id', 'in', result]],
                    views: [[false, 'list'], [false, 'form']],
                    type: 'ir.actions.act_window',
                    view_type: "list",
                    view_mode: "list"
                });
            })
        },

        exit: function () {
            this.trigger_up('history_back');
        },
    });
    core.action_registry.add('import_custom_csv', ImportCustomCSV);

    StateMachine.create({
        target: ImportCustomCSV.prototype,
        events: [
            { name: 'select_customer', from: ['none', 'file_load', 'settings_changed'], to: 'selected_customer' },
            { name: 'file_load', from: ['selected_customer', 'settings_changed'], to: 'file_loaded' },
            { name: 'settings_changed', from: 'file_loaded', to: 'previewing' },
            { name: 'import', from: 'previewing', to: 'imported' },

        ],
    });

    return ImportCustomCSV;
});