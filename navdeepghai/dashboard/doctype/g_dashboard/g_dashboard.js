// Copyright (c) 2020, GERMBUSTERS and contributors
// For license information, please see license.txt

frappe.provide("germbusters");
germbusters.GDashboard = Class.extend({
    init: function(args){
        $.extend(this, args);

    },
    setup: function(){
        let values = [];
        $.each(this.frm.doc.columns, (idx, col)=>{
            values.push(col.column_name);
        });
    },
    refresh: function(){
        this.update_columns_details();
    },
    update_columns_details: function(){
        let values = [];
        $.each(this.frm.doc.columns, (idx, col)=>{
            values.push(col.column_name);
        });
        this.frm.set_df_property("column_name",
                        "options", values, this.frm.doc.name, "columns_details");
        this.frm.fields_dict.columns_details.grid.refresh();
    }
});

cur_frm.script_manager.make(germbusters.GDashboard);
