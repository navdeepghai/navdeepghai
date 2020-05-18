/*
    App Related Init Structure
*/

frappe.provide("booking");
frappe.provide("navdeepghai");

$(document).ready(function(){
    if(frappe.boot.dashboard_roles.hasOwnProperty(frappe.user.name)){
        window.location.href = frappe.utils.format("/dashboard?dashboard={0}",
                    [encodeURI(frappe.boot.dashboard_roles[frappe.user.name][0])]);
    }
});
$.extend(navdeepghai, {
    set_12_hours_timer: function(data_field_name){
        $(`input[data-fieldname='${data_field_name}']`).timepicker({
            minuteStep: 30,
            secondStep: 5,
            showInputs: false,
            modalBackdrop: true,
            defaultTime: false
        });
    },
    date_time_format: "YYYY-MM-DD h:mm A",
    time_format: "h:mm A",
    open_in_google_map: function(source_adddress, destination_address){
		var me = this;
        let src = "";
        let des = "";
        if(source_address){
            src  = format("origin={0},{1}", [source_address])
        }
        if(destination_address){
            des = format("&destination={0}&travelmode=driving", [destination]);
        }
		url = encodeURI(frappe.utils.format("https://www.google.com/maps/dir/?api=1&{0}{1}", [src, des]));
		window.open(url, "_blank");
	},
	success: function(source_address, destination_address){
		var me = this;
        let source = "", destination = "", base_url = "";

        /*
        if(!source_address && navdeepghai.get_user_agent() == "apple"){
            source_address = "Current Location";
        */
        if(!source_address){
            source_address = "current+location";
        }
        /*
		if(navdeepghai.get_user_agent()	 == "apple"){
			base_url = "https://maps.apple.com/"
            if(source_address){
                source =  frappe.utils.format("saddr={0}", [source_address]);
            }
			destination = frappe.utils.format("&daddr={0}", [destination_address])

		}
        */
		base_url = "https://www.google.com/maps/dir/?api=1";
        source = frappe.utils.format("&origin={0}", [source_address]);
		destination = frappe.utils.format("&destination={0}", [destination_address])
        let href = encodeURI(frappe.utils.format("{0}{1}{2}", [base_url, source, destination]));
		window.open(href, "_blank");
	},
    get_user_agent:function(){
        var flag  = null;
        var agent = navigator.platform;
        if(agent == 'iPhone' ||  agent == 'iPod'  || agent == 'iPad'){
            flag = "apple";
        }
        else if (agent == 'Android'){
            flag = "android";
        }else{
            flag = "android";
        }
        return flag;
    }
});
