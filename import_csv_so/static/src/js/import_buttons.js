odoo.define('import_csv_so.import_buttons', function (require) {
    "use strict";
    
    var config = require('web.config');
    var KanbanController = require('web.KanbanController');
    var KanbanView = require('web.KanbanView');
    var ListController = require('web.ListController');
    var ListView = require('web.ListView');
    
    
    var ImportViewMixin = {
    
        init: function (viewInfo, params) {
            var importEnabled = 'import_enabled' in params ? params.import_enabled : true;
            this.controllerParams.importEnabled = importEnabled && !config.device.isMobile;
        },
    };
    
    var ImportControllerMixin = {
    
        init: function (parent, model, renderer, params) {
            this.importEnabled = params.importEnabled;
        },
    
        _bindImport: function () {
            if (!this.$buttons) {
                return;
            }
            var self = this;
            this.$buttons.on('click', '.o_button_custom_import', function () {
                var state = self.model.get(self.handle, {raw: true});
                self.do_action({
                    type: 'ir.actions.client',
                    tag: 'import_custom_csv',
                    name: 'Select Customer',
                    params: {
                        model: self.modelName,
                        context: state.getContext(),
                    }
                });
            });
        }
    };
    
    ListView.include({
        init: function () {
            this._super.apply(this, arguments);
            ImportViewMixin.init.apply(this, arguments);
        },
    });
    
    ListController.include({
        init: function () {
            this._super.apply(this, arguments);
            ImportControllerMixin.init.apply(this, arguments);
        },
    
        renderButtons: function () {
            this._super.apply(this, arguments);
            ImportControllerMixin._bindImport.call(this);
        }
    });
    
    KanbanView.include({
        init: function () {
            this._super.apply(this, arguments);
            ImportViewMixin.init.apply(this, arguments);
        },
    });
    
    KanbanController.include({
        init: function () {
            this._super.apply(this, arguments);
            ImportControllerMixin.init.apply(this, arguments);
        },
    
        renderButtons: function () {
            this._super.apply(this, arguments);
            ImportControllerMixin._bindImport.call(this);
        }
    });
});
    