/* write your js controller here */

frappe.ready(function(){
    germbusters.Vehicle = germbusters.dashboard.Dashboard.extend({
        get_row: function(idx, columns, val){
            return $(`<tr>
                    <td>${val.vehicle_details}</td>
                    <td>${val.status}</td>
                </tr>`);
        },

    });
    new germbusters.Vehicle({});

});
