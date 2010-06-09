//Form helpers
(function($) { 
$.fn.lousyField = function (){
    oldvalue = ''
    return $(this)
        .focus(function(){
            oldvalue = this.value;
            return $(this).val('');
        })
        .blur(function(){
            placeholder = $(this).attr('placeholder');
            if (this.value == ''){
                return $(this).val(placeholder);
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
    $('.searchterm').lousyField()
    $('.search').submit(function(){
        $(this).find(':fields').noCrap()
    })
})
