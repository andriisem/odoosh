odoo.define('cycle_count_friendly.keypad', function (require) {
    'use strict';
    
    var widgetRegistry = require('web.widget_registry');
    var Widget = require('web.Widget');
    
    var core = require('web.core');

    var QWeb = core.qweb;
    
    var FieldKeypad = Widget.extend({
        className: 'o_field_keypad',
        tag_template: 'Keyboard',

        events: {
            "click .number-char": "clickAppendNewChar",
            "click .numpad-backspace": "clickDeleteLastChar"
        },

        init: function (parent, data, options) {
            this._super.apply(this, arguments);
            this.service_name = options.attrs.service_name;            
            this.$qty = document.getElementsByName('qty');
        },

        start: function () {
            this.$widget = $(QWeb.render(this.tag_template));
            this.$widget.appendTo(this.$el);       
        },

        clickAppendNewChar: function(event) {
            var newChar;
            newChar = event.currentTarget.innerText || event.currentTarget.textContent;
            if (this.$qty[0].value === '0' && newChar !== '.') {          
                this.$qty[0].value = newChar
            } else {
                this.$qty[0].value = this.$qty[0].value + newChar
            }            
            $("input[name='qty']").trigger('input')
        },

        clickDeleteLastChar: function() {
            this.$qty[0].value = this.$qty[0].value.slice(0,-1) || "";
        },
        
    })
    widgetRegistry.add('o_field_keypad', FieldKeypad);
    return FieldKeypad;
});