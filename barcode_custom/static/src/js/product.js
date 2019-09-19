odoo.define('barcode_custom.image_tab', function (require) {
'use strict';

var AbstractView = require('web.AbstractView');

AbstractView.include({
    /**
     * @override
     */
    init: function () {
        var q = window.location.href.split('q=');
        if (q[1] == 'image') {
            var old_page = '<page name="studio_page_ozBv6" string="Image">';
            var new_page = '<page name="studio_page_ozBv6" string="Image" autofocus="autofocus">';
            arguments[0].arch = arguments[0].arch.replace(old_page, new_page)
        }
        this._super.apply(this, arguments);
    },
});

});