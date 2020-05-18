/*
    Fetch location services from  geolocation javascript module
*/

frappe.provide("location_services");

$.extend(location_services, {
    watch_location: function(callback, options, error_handler){
        if(navigator && navigator.geolocation){
            navigator.geolocation.watchPosition(
            (res)=>{
                location_services.handle_success(res, callback)
            },
            (res)=>{
                location_services.handle_error(res);
            }, options || location_services.get_default_options());
        }else{
            frappe.msgprint(__("Your browser doesn't support location services"));
        }
    },
    get_current_location: function(callback, options, error_handler){
        if(navigator && navigator.geolocation){
            navigator.geolocation.getCurrentPosition(
            (res)=>{
                location_services.handle_success(res, callback)
            },
            (res)=>{
                location_services.handle_error(res);
            }, options || location_services.get_default_options());
        }else{
            frappe.msgprint(__("Your browser doesn't support location services"));
        }

    },
    get_default_options: function(){
        return  {
              enableHighAccuracy: true,
              timeout: 5000,
              maximumAge: 0
          };
    },
    handle_error: function(err){
        console.warn(err);
    },
    handle_success: function(loc, callback){
        let lat = loc.coords.latitude;
        let long = loc.coords.longitude;
        var me = this;
        frappe.call({
            "method": "germbusters.tracking.utils.get_location_latlong",
            "args":{
                "lat": lat, "long": long
            },
            "callback": (res)=>{
                callback && callback(res);
            }
        });
    },
    get_permission: function(){
    }
});
