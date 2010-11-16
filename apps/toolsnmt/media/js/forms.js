//Form helpers
$(document).ready( function(){
    clearValue = function (element){
        oldvalue = $(element).val();
        $(element).toggleClass('dirty');
        $(element).val('');
        $(element).blur(function(){
            if ($(element).val()==''){
                $(element).val(oldvalue);
                $(element).toggleClass('dirty')
            }
        })
    }   


    $('.searchterm').focus(function(){
        value = $(this).val();
        if(value=="Ingrese un nombre de calle"||value=="Interseccion"||value=="Altura"){
            clearValue(this)
        }
    }) 

    $('#searchbuton').click(function(){
        $('#streetsform').find(':fields').each(function(){
            value = $(this).val();
            if(value=="Ingrese un nombre de calle"||value=="Interseccion"||value=="Altura"){
                $(this).val('');
            }
        });
        $('#streetsform').submit();
    return false;
    })
})
