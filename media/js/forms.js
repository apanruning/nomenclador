//Form helpers
(function($) { 
$.fn.lousyField = function (){
    oldvalue = ''
    return $(this)
        .focus(function(){
            oldvalue = this.value;
            return $(this).val('')
                          .toggleClass('dirty');
        })
        .blur(function(){
            placeholder = $(this).attr('placeholder');
            if (this.value == ''){
                return $(this).val(placeholder)
                              .toggleClass('dirty');
            };
        })
    }
})(jQuery);

(function($) { 
$.fn.noCrap = function (){
    /*probably an abuse of the plugins system*/
    this.each(function(){
        placeholder = $(this).attr('placeholder');
        if ($(this).val() == placeholder){
            return $(this).val('');
            
        };
    })

    }
})(jQuery);

$(document).ready( function(){
	function split(val){
		return val.split(/,\s*/);
	}
	function extractLast(term) {
		return split(term).pop();
	}
    $('.searchterm').lousyField()
    $('.search').submit(function(){
        $(this).find(':fields').noCrap()
    })
    $("#id_barrios")
		.autocomplete({
			source: function( request, response ) {
				$.getJSON( "/barrios/", {
					name: extractLast( request.term )
				}, response );
			},
			search: function() {
				var term = extractLast( this.value );
				if ( term.length < 2 ) {
					return false;
				}
			},
			focus: function() {
				return false;
			},
			select: function(event, ui) {
				var terms = split( this.value );
				terms.pop();
				terms.push( ui.item.value );
				terms.push( "" );
				this.value = terms.join( ", " );
				return false;
			}
		});

})

