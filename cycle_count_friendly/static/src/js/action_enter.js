odoo.define('cycle_count_friendly.enter', function (require) {
    'use strict';
    
    var basic_fields = require('web.basic_fields');
    var field_registry = require('web.field_registry');
    var FieldChar = basic_fields.FieldChar;

    var FindLocation = FieldChar.extend({

        events: _.extend({}, FieldChar.prototype.events, {
            'change': '_onChange',
        }),
    
        init: function () {
            this._super.apply(this, arguments);
        },

        _onChange: function() {
            var action = $('button[name="action_find_location"]');
            action.click()
        },
    });

    var FindProduct = FieldChar.extend({

        events: _.extend({}, FieldChar.prototype.events, {
            'change': '_onChange',
        }),
    
        init: function () {
            this._super.apply(this, arguments);
        },

        _onChange: function() {
            var action = $('button[name="action_product_next_stage"]');
            action.click()
        },
    });
    
    field_registry.add('find_location', FindLocation);
    field_registry.add('find_product', FindProduct);
    
    });
    