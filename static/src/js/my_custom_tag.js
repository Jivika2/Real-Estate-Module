/* odoo.define('real_estate_ads.CustomAction', function(require){
    'use strict';

    var AbstractionAction = require('web.AbstractionAction');
    var core = require('web.core');

    var CustomAction = AbstractionAction.extend({
        template: "CustomAction",
        start: function(){
            console.log("action")
        }
    })

    core.action_registry.add("custom_client_action", CustomAction)
}); */

odoo.define('real_estate_ads.CustomAction', function(require){
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var core = require('web.core');

    var CustomAction = AbstractAction.extend({
        template: "CustomActions",  // This must match the template ID in your XML file
        start: function(){
            console.log("Custom client action started")
        }
    })

    core.action_registry.add("custom_client_action", CustomAction);
});
