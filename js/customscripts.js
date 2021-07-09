$('#mysidebar').height($(".nav").height());

$(document).ready(function(){

    /*Bootstrap popovers are initialized with the following script. In the options, I'm setting the placement to be on the right, the trigger to be hover rather than click, and to allow HTML from the JSON data source. */
    
        $('[data-toggle="popover"]').popover({
            placement : 'bottom',
            trigger: 'click hover',
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

$( document ).ready(function() {

    //this script says, if the height of the viewport is greater than 800px, then insert affix class, which makes the nav bar float in a fixed
    // position as your scroll. if you have a lot of nav items, this height may not work for you.
    var h = $(window).height();
    //console.log (h);
    if (h > 800) {
        $( "#mysidebar" ).attr("class", "nav affix");
    }
    // activate tooltips. although this is a bootstrap js function, it must be activated this way in your theme.
    $('[data-toggle="tooltip"]').tooltip({
        placement : 'top'
    });

    /**
     * AnchorJS
     */
    anchors.add('h2,h3,h4,h5');

});

// needed for nav tabs on pages. See Formatting > Nav tabs for more details.
// script from http://stackoverflow.com/questions/10523433/how-do-i-keep-the-current-tab-active-with-twitter-bootstrap-after-a-page-reload
$(function() {
    var json, tabsState;
    $('a[data-toggle="pill"], a[data-toggle="tab"]').on('shown.bs.tab', function(e) {
        var href, json, parentId, tabsState;

        tabsState = localStorage.getItem("tabs-state");
        json = JSON.parse(tabsState || "{}");
        parentId = $(e.target).parents("ul.nav.nav-pills, ul.nav.nav-tabs").attr("id");
        href = $(e.target).attr('href');
        json[parentId] = href;

        return localStorage.setItem("tabs-state", JSON.stringify(json));
    });

    tabsState = localStorage.getItem("tabs-state");
    json = JSON.parse(tabsState || "{}");

    $.each(json, function(containerId, href) {
        return $("#" + containerId + " a[href=" + href + "]").tab('show');
    });

    $("ul.nav.nav-pills, ul.nav.nav-tabs").each(function() {
        var $this = $(this);
        if (!json[$this.attr("id")]) {
            return $this.find("a[data-toggle=tab]:first, a[data-toggle=pill]:first").tab("show");
        }
    });
});
