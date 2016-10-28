$(document).ready(function(){
    $('.new').hide()
    $(".gametitle").click(function(){
        var $games = $(this).parent().parent().nextUntil(".gamedeals").find('.new');
        if ($('.new').css("display") == 'none'){
            $('.new').slideDown()
        } else if ( $('.new').css('display') == 'block') {
            $('.new').slideUp();
        }
    });
});