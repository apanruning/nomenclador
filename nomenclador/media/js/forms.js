//Form helpers
$(document).ready( function(){
clearValue = function (element){
    oldvalue = $(element).val()
    console.log($(element).val())
    $(element).attr('class','searchterm-dirty')
    $(element).val('')
    $(element).blur(function(){
        if ($(element).val()==''){
            $(element).val(oldvalue)
            $(element).attr('class','searchterm')
        }
    })
    $('#streetsform').submit(function(){
        $(this).find(':fields').each(function(){
            value = $(this).val()
            if(value=="Ingrese un nombre de calle"||value=="Interseccion"||value=="Altura"){
                $(this).val('')
            }
        })
    })

    $('.searchterm').focus(function(){
        value = $(this).val()
        if(value=="Ingrese un nombre de calle"||value=="Interseccion"||value=="Altura"){
            clearValue(this)
        }
    }) 
})
