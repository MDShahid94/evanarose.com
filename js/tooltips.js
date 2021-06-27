$(document).ready(function(){

/*Bootstrap popovers are initialized with the following script. In the options, I'm setting the placement to be on the right, the trigger to be hover rather than click, and to allow HTML from the JSON data source. */

    $('[data-toggle="popover"]').popover({
        placement : 'right',
        trigger: 'hover',
        html: true
    });

/* Set the location where mydoc_tooltips_source.json is. */
var url = "tooltips.json";

$.get( url, function( data ) {

 /* Bootstrap popover text is defined inside a data-content attribute inside an element. That's
 why I'm using attr here. If you just want to insert content on the page, use append and remove the data-content argument from the parentheses.*/

    $.each(data.entries, function(i, page) {
        if (page.doc_id == "basketball") {
            $( "#basketball" ).attr( "data-content", page.body );
        }

        if (page.doc_id == "baseball") {
            $( "#baseball" ).attr( "data-content", page.body );
        }
        if (page.doc_id == "football") {
            $( "#football" ).attr( "data-content", page.body );
        }

        if (page.doc_id == "soccer") {
            $( "#soccer" ).attr( "data-content", page.body );
        }


        });
    });


});