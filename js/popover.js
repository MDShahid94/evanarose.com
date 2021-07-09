$(document).ready(function(){

    /*Bootstrap popovers are initialized with the following script. In the options, I'm setting the placement to be on the right, the trigger to be hover rather than click, and to allow HTML from the JSON data source. */
    
        $('[data-toggle="popover"]').popover({
            placement : 'bottom',
            trigger: 'click',
            html: true
        });
    
    /* Set the location where mydoc_tooltips_source.json is. */
    var url = "tooltips.json";
    
        $.get( url, function( data ) {
    
     /* Bootstrap popover text is defined inside a data-content attribute inside an element. That's
     why I'm using attr here. If you just want to insert content on the page, use append and remove the data-content argument from the parentheses.*/
    
     $.each(data.entries, function(i, page) {
        var title = page.doc_id.replaceAll("_", " ");
        var newTitle = '<span class="text-info"><strong>'+title+'</strong></span><button type="button" id="close" class="close" onclick="$(&quot;.'+page.doc_id+'&quot;).popover(&quot;hide&quot;);">&times;</button>';
        $( '.' + page.doc_id ).attr('data-original-title', newTitle);
        $( '.' + page.doc_id ).attr("data-content", page.body );
        $('body').on('hidden.bs.popover', function (e) {
            $(e.target).data("bs.popover").inState.click = false;
        });
    });
});
});