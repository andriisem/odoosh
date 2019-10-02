odoo.define('import_csv_so.partner_kanban_view_handler', function(require) {
    "use strict";
    
    var KanbanRecord = require('web.KanbanRecord');
    
    KanbanRecord.include({
        
        _openRecord: function () {
            if (this.modelName === 'res.partner' && this.$el.parents('.o_res_partner_import_kanban').length) {
                var action = {
                    type: 'ir.actions.client',
                    name: 'Load File',
                    tag: 'import_custom_csv',
                    partner: this.record.id.raw_value,
                    partner_name: this.record.name.raw_value,
                };
                this.do_action(action);
            } else {
                this._super.apply(this, arguments);
            }
        }
    });
    
    });