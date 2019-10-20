odoo.define('fullfilemt.check_availability', function (require) {
    "use strict";

    var KanbanController = require('web.KanbanController');

    var CheckAvailability = {

        _checkAvailability: function () {
            if (!this.$buttons) {
                return;
            }
            if (this.modelName === 'fullfilemt') {  
                this.$buttons.find('.o-kanban-button-new').addClass('d-none');
                this.$buttons.find('.o_button_import').addClass('d-none');
            }
            var self = this;
            this.$buttons.on('click', '.o_button_check_availability', function () {
                self.do_action({
                    name: 'Check Availability',
                    type: 'ir.actions.act_window',
                    res_model: 'fullfilemt.check.availability',
                    views: [[false, 'list']],
                    target: 'current'
                });
            });
        }
    };

    KanbanController.include({
        renderButtons: function () {
            this._super.apply(this, arguments);
            CheckAvailability._checkAvailability.call(this);
        }
    });
});