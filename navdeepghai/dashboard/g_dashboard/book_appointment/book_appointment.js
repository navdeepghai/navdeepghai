/* write your js controller here */

frappe.ready(function(){

    frappe.provide("service_technician");

    service_technician.ServiceTechnician = germbusters.dashboard.Dashboard.extend({
        get_row: function(idx, columns, val){
            let $row = $(`<tr addr='${val.customer_address}' booking='${val.name}'>
                    <td style="${columns[0].column_width}% !important;">
                        <span>
                            <b>${__("Customer Name: ")}</b>
                            ${val.full_name}
                        </span><br>
                        <span>
                            <b>${__("Booking ID: ")}</b>
                            ${val.name}
                        </span><br>
                        <span>
                            <b>${__("Task ID: ")}</b>
                            ${val.task}
                        </span><br>
                        <span>
                            <b>${__("Mobile: ")}</b>
                            ${val.mobile}
                        </span><br>
                        <span>
                            <b>${__("Email: ")}</b>
                            ${val.email}
                        </span><br>
                        <span>
                            <b>${__("Total Targets: ")}</b>
                                ${val.total_targets || ""}
                        </span><br>
                        <span>
                            <b>${__("Targets Type: ")}</b>
                                ${val.target_details || ""}
                        </span><br>
                        <span>
                            <b>${__("Service Type: ")}</b>
                                ${val.disinfection_system}
                        </span><br>
                        <span>
                            <b>${__("Service Address: ")}</b>
                                ${val.customer_address_without_country}
                        </span>
                    </td>
                    <td style="${columns[1].column_width}% !important;">
                        <span>
                            <b>${__("Date: ")}</b>
                            ${val.booking_date}
                        </span><br>
                        <span>
                            <b>${__("Departure: ")}</b>
                            ${val.from_time}
                        </span><br>
                        <span>
                            <b>${__("Start Time: ")}</b>
                            ${val.appointment_start_time}
                        </span><br>
                        <span>
                            <b>${__("ETC: ")}</b>
                                ${val.etc}
                        </span><br><br>
                        <span>
                            <button class='btn btn-primary'>${__("Start")}</button><br><br>
                            <button class="btn btn-info open-support-or-call">${__("Support")}</button>
                        </span>
                    </td>
                    <td style="width:${columns[2].column_width}% !important;vertical-align:middle;" class='text-${frappe.scrub(columns[2].text_align)}'>
                        <b>${val.status}</b>
                    </td>
                <tr>`);
            this.handle_direction($row);
            this.handle_support($row, val);
            this.handle_more_details($row, val);
            return $row
        },
        handle_support: function($row, val){
            var me = this;
            $($row).find(".open-support-or-call").on("click",  (event)=>{
                if(this.support){
                    this.support.handle_existing_support(val);
                    return;
                }
                let args = {
                    "val": val,
                };
                this.support = new germbusters.dashboard.Support(args);
            });
        },
        handle_more_details: function($row, val){
            $row.find(".more-details").on("click", (res)=>{
                if(val.name){
                    frappe.call({
                        "method": "germbusters.www.dashboard.service-technician.index.get_more_details",
                        "args": {
                            "booking_id": val.name,
                        },
                        "freeze": true,
                        "callback": (res)=>{
                            console.log(this);
                        }
                    });
                }
            });
        },
        handle_direction: function($row){
            var me = this;
            $row.find(".btn-primary").on("click", function(event){
                let address = $row.attr("addr");
                let href = frappe.utils.format("https://www.google.com/maps/dir/?api=1&origin={0}&destination={1}",
                                        ["current+location", address]);
                window.open(href, "_blank");
            });
            $row.find(".btn-secondary").on("click", function(event){
                let booking = $row.attr("booking");
                new service_technician.BookingDetail({"booking": booking});
            });
        }
    });

    service_technician.BookingDetail = Class.extend({
        init: function(args){
            $.extend(this, args);
            this.make();
        },
        make: function(){
            this.get_booking_detail();
        },
        get_booking_detail: function(){

            if(!this.booking){
                germbusters.unfreeze();
                return false;
            }
            frappe.unfreeze();
            frappe.unfreeze();
            frappe.call({
                "method": "germbusters.www.dashboard.service-technician.index.get_booking_detail",
                "args":{
                    "booking": this.booking,
                },
                "callback": (res)=>{
                    if(res && res.message){
                        this.init_dialog(res.message)
                    }
                }
            });
        },
        init_dialog: function(detail){

        },
    });
    new service_technician.ServiceTechnician({});

});
