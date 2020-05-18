/*
*/

frappe.provide("germbusters");
frappe.ready(function(){
    //$('.carouselmain').carousel()
    $(".carousel-button").on("click", function(event){
        event.preventDefault();
        window.location.href = $(this).attr("data-target") || '/';
    });
});
