odoo.define('fullfilemt.fullfilemt_check_availability', function (require) {
    "use strict";

    var ListController = require('web.ListController');

    var RequestAll = {

        _requestAll: function () {
            if (!this.$buttons) {
                return;
            }
            if (this.modelName === 'fullfilemt.check.availability') {  
                this.$buttons.find('.o_list_button_add').addClass('d-none');
                this.$buttons.find('.o_button_import').addClass('d-none');
            }
            var self = this;

            this.$buttons.on('click', '.o_button_request_all', function () {
                self._rpc({
                    model: 'fullfilemt.check.availability',
                    method: 'action_request_all',
                    args: [[]],
                }).then(function (result) {
                    document.location.reload(true);
                })               
            });
        }
    };

    ListController.include({
        renderButtons: function () {
            this._super.apply(this, arguments);
            RequestAll._requestAll.call(this);
        }
    });
});