// Copyright (c) 2020, GERMBUSTERS and contributors
// For license information, please see license.txt

frappe.provide("germbusters.controllers");

germbusters.controllers.CompanySettings = Class.extend({
    init: function(args){
        $.extend(this, args);
    },
    refresh: function(){
        var me = this;
        this.frm.add_custom_button(__("Update Current Location"), ()=>{
            me.fetch_and_update_location();
        });
    },
    fetch_and_update_location: function(){
        var me = this;
        location_services.get_current_location((res)=>{
            if(res && res.message){
                me.frm.doc.state = res.message.state;
                me.frm.doc.zip_code = res.message.zip_code;
                me.frm.doc.country = res.message.country;
                me.frm.doc.latitude = res.message.latitude;
                me.frm.doc.longitude = res.message.longitude;
                me.frm.doc.complete_address= res.message.address;
                me.frm.save();
            }
        }).then(()=>{
        });
    }
});

cur_frm.script_manager.make(germbusters.controllers.CompanySettings);
