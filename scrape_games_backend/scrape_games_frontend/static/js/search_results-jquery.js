$(document).ready(function(){
    $('.test').hide()
    $(".gametitle").click(function(){
        $(this).parent().parent().nextUntil(".container").toggle()

    });



});