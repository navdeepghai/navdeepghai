/*

*/

frappe.provide("germbusters.dashboard");
/*
    Filters
*/
germbusters.dashboard.Dashboard = Class.extend({
    init: function(args){
        $.extend(this, args);
        this.make();
    },
    make: function(){
        this.dashboard_data = dashboard;
        this.$wrapper = $(".page-wrapper");
        this.make_table()
        this.make_filters();
        this.make_sidebar();
        this.refresh();
    },
    make_filters: function(){
        this.filters = new germbusters.dashboard.Filters({
            "dashboard": this,
        });
    },
    make_sidebar: function(){
        this.sidebar = new germbusters.dashboard.Sidebar({
            "dashboard": this
        });
    },
    refresh: function(){
        var values = this.filters.get_values();
        this.get_data(values);
    },
    get_data: function(filters){
        frappe.call({
            "method": "germbusters.www.dashboard.index.get_data",
            "args":{
                "filters": filters,
                "dashboard": dashboard
            },
            "callback": (res)=>{
                this.handle_response(res)
            }
        });
    },
    handle_response: function(res){
        this.$table.find("tbody").empty();
        if(!(res && res.message)){
            $(`<tr><td colspan="${this.dashboard_data.columns.length}" class='text-center'><h2>
                        ${__("No Data")}</h2>
            </td></tr>`).appendTo(this.$table.find("tbody"));
        }else{
            $.each(res.message, (idx, val)=>{
                this.add_row(idx, val);
            });
        }
    },
    make_table: function(){
        this.$table = $(`<table class="table table-responsive-sm table-hover table-dark table-bordered booking-details">
            <thead><tr></tr></thead>
            <tbody></tbody>
        </table>`);
        this.make_headers();
        this.$table.appendTo(this.$wrapper);
    },
    make_headers: function(columns){
        $.each(this.dashboard_data.columns, (idx, col)=>{
            $(`<th style="width:${col.column_width}% !important;vertical-align:middle;" class="text-uppercase bold text-${frappe.scrub(col.text_align)}">
                <strong>${col.column_name}</strong>
            </th>`).appendTo(this.$table.find("thead").find("tr"));
        });
    },
    add_row: function(idx, val){
        let $tr = this.get_row(idx, this.dashboard_data.columns, val);
        $tr.appendTo(this.$table.find("tbody"));
    }
});


germbusters.dashboard.Filters = Class.extend({
    init: function(args){
        $.extend(this, args);
        this.make();
    },
    make: function(){
        this.$wrapper = $(".filters");
        this.fields_dict = {};
        this.values = {};
        this.make_filters();
    },
    make_filters: function(){
        var me = this;
        $.each(this.dashboard.dashboard_data.filters, (idx, df)=>{
            let field = {
                "df":{
                    "fieldname": df.fieldname,
                    "fieldtype": df.fieldtype,
                    "label": df.label,
                    "options": df.options,
                    "onchange": ()=>{
                        this.set_values();
                        if(this.dashboard.refresh){
                            this.dashboard.refresh()
                        }
                    }
                },
                "parent": this.get_filter_wrapper(),
                "render_input": true,
            }
            this.fields_dict[field.df.fieldname]=frappe.ui.form.make_control(field);
            let $input = this.fields_dict[field.df.fieldname].$input;
            if(field.df.default){
                $input.val(field.df.default);
                this.values[field.df.fieldname] = field.df.default;
            }
            this.handle_input(this.fields_dict[field.df.fieldname], df);
        });
    },
    handle_input: function(field, df){
        if(df.is_default && df.fieldtype == "Date"){
            field.set_value(frappe.datetime.nowdate());
        }else if(df.default && df.fieldtytpe == "Select"){
            field.set_value(df.default);
        }
    },
    set_values: function(){
        this.values = {};
        $.each(this.fields_dict, (fieldname, field)=>{
            this.values[fieldname] = field.$input.val();
        });
    },
    get_values: function(){
        return this.values;
    },
    get_filter_wrapper: function(){
        let $wrapper = $(`<div class='col-md-3'></div>`);
        $wrapper.appendTo(this.$wrapper);
        return $wrapper;
    }
});
/*
    End Filters
*/

/*
    Start Support
*/
germbusters.dashboard.Support = Class.extend({
    init: function(args){
        $.extend(this, args);
        this.make();
    },
    make: function(){
        this.make_dialog();
    },
    make_dialog: function(){
        this.dialog  = new frappe.ui.GDialog({
            "title": __("Call & Open Ticket"),
            "fields":[{
                    "fieldname": "support", "fieldtype": "HTML",
            }],
        });
        this.add_buttons();
        this.dialog.show();
    },
    add_buttons: function(){
        this.dialog.set_value("support", this.get_support_button());
        this.dialog.fields_dict.support.$wrapper.find(".call").on("click", (event)=>{
            this.handle_call();
        });
        this.dialog.fields_dict.support.$wrapper.find(".open-ticket").on("click", (event)=>{
            this.handle_email();
        });
    },
    handle_existing_support: function(values){
        this.val = values;
        this.dialog.show();
    },
    handle_email: function(){
        let email = germbusters.boot_context.it_email;
        let subject = frappe.utils.format("{0}: {1}-{2},", [frappe.user_id, this.val.name, this.val.task])
        let ele = document.createElement("a");
        ele.setAttribute("href", frappe.utils.format("mailto:{0}?subject={1}", [email, subject]));
        ele.click();
    },
    handle_call: function(){
        let mobile = germbusters.boot_context.mobile_no;
        let ele = document.createElement("a");
        ele.setAttribute("href", frappe.utils.format("tel:{0}", [mobile]));
        ele.click();

    },
    get_support_button: function(){
        return $(`<div class='row'>
            <div class="col-md-6">
                <button class="btn btn-primary open-ticket">${__("Open Ticket")}</button>
            </div>
            <div class="col-md-6">
                <button class="btn btn-primary call">${__("Call Now")}</button>
            </div>
        </div>`);
    }
});
/*
    End Supoort
*/

/*
    Sidebar
*/
germbusters.dashboard.Sidebar = Class.extend({
    init: function(args){
        $.extend(this, args);
        this.make();
    },
    make: function(){
        this.$wrapper  = $(".c-sidebar-nav-item");
        this.make_sidebar();
    },
    make_sidebar: function(){
        this.side_options = {};
        $.each(this.dashboard.dashboard_data.sidebar_items, (idx, option)=>{
            if(frappe.user.has_role(option.user_role)){
                this.side_options[option.label] = this.get_options_wrapper(option);
                this.side_options[option.label].appendTo(this.$wrapper);
                this.handle_sidebar(this.side_options[option.label], option);
            }
        });
    },
    get_options_wrapper: function(option){
        let $option = $(`<a class="c-sidebar-nav-link" href="#">
            <li class="c-sidebar-nav-icon ${option.icon}"></li>
            ${__(option.label)}
        </a>`);
        return $option;
    },
    handle_sidebar: function($option, option){
        $option.on("click", (event)=>{
            window.location.href= frappe.utils.format("/dashboard?dashboard={0}", [encodeURI(option.sidebar_doctype)]);
        });
    }
});
/*
    End Sidebar
*/
