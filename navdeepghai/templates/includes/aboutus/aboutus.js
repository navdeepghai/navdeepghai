/*
    Tracker
*/

frappe.provide("tracker");

frappe.ready(function(){

    germbusters.AboutUs = Class.extend({
        init: function(args){
            $.extend(this, args);
            this.make();
        },
        make: function(){
            this.$map = document.getElementById("aboutus-map");
            this.setup_defaults();
            this.init_map();
            this.setup_location();
        },
        setup_defaults: function(){
            L.Icon.Default.imagePath = '/assets/frappe/images/leaflet/';
        },
        init_map: function(){
            this.map = L.map(this.$map).setView([40.564193, -74.298928], 15);
            L.tileLayer('https://{s}.tile.osm.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(this.map);
        },
        setup_location: function(){
            frappe.call({
                "method": "germbusters.www.aboutus.index.get_company_location",
                "args":{

                },
                "callback": (res)=>{
                    this.make_marker(res);
                    this.make_popup(res);
                    this.make_address(res);
                }
            });
        },
        make_marker: function(res){
            let latlng = L.latLng(40.564193, -74.298928);
            if(this.marker){
                this.marker.setLatLng(latlng);
                return
            }
            this.marker = L.marker(latlng, {
                "icon": this.get_logo()
            }).addTo(this.map);
        },
        make_popup: function(res){
            this.marker.bindPopup(res.message.location);
            this.marker.togglePopup();
        },
        make_address: function(res){
            $(".aboutus-long-address").empty();
            $(res.message.location).appendTo(".aboutus-long-address");
        },
        get_logo: function(){
            if(this.logo){
                return this.logo;
            }
            this.logo = L.icon({
                iconUrl: '/assets/germbusters/images/tracker/map-logo.png',
                iconSize:     [150, 100], // size of the icon
                shadowSize:   [50, 64], // size of the shadow
                iconAnchor:   [22, 94], // point of the icon which will correspond to marker's location
                shadowAnchor: [4, 62],  // the same for the shadow
                popupAnchor:  [-3, -76] // point from which the popup should open relative to the iconAnchor
            });
            return this.logo;
        },
    });
    new germbusters.AboutUs({});

});
