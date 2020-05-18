/*
*/

// Navdeep
function setMobileView(){
    const innerWidth = window.innerWidth;
    const innerHeight = window.innerHeight;
    if(innerWidth < 500){
        var ele = document.getElementsByClassName("headling-title");
        for(var i=0;i<ele.length; i++){
            ele[i].style.fontSize = '1em';
        }
    }else{
        var ele = document.getElementsByClassName("headling-title");
        for(var i=0;i<ele.length; i++){
            ele[i].style.fontSize = '1.33333em';
        }
    }

    var images_sets = document.getElementsByClassName("image-set");
    for(var i=0;i<images_sets.length; i++){
        let ul = images_sets[i];
        let target_image = ul.attributes['data-image-name'].value;
        let imgDiv = document.getElementById(target_image);
        let default_image_path = `url("${imgDiv.attributes['data-bg'].value}")`;
        if(!imgDiv || imgDiv == null || imgDiv == undefined){
            continue;
        }

        for(var j=0;j<ul.childNodes.length; j++){
            let minHeight = ul.childNodes[j].attributes['image-min-height'].value;
            let maxHeight = ul.childNodes[j].attributes['image-max-height'].value;
            let minWidth = ul.childNodes[j].attributes['image-min-width'].value;
            let maxWidth = ul.childNodes[j].attributes['image-max-width'].value;
            let image = ul.childNodes[j].attributes['image-data'].value;
            if(innerWidth < maxWidth &&  innerWidth > minWidth ){
                let url = `url("${image}")`
                imgDiv.style.backgroundImage = url;
                break;
            }else{
                imgDiv.style.backgroundImage = default_image_path;
            }
        }
    }
}

window.addEventListener("resize", function(win){
    setMobileView();
});

(function(){
    setMobileView();
})();

frappe.provide("germbusters");

$.extend(germbusters, {
    freeze: function(){
        let message = "<div class='text-center loader'></div><div>Loading...</div>";
        frappe.freeze(message);
    },
    unfreeze: function(){
        frappe.unfreeze();
    }
});
