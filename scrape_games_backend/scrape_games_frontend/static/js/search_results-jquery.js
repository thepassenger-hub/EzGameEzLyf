$(document).ready(function(){
    $('.new').hide()
    $(".gamedeals").each(function(){
        if ($(this).next().attr("class") !== "test") {
            $(this).find(".btn").hide();
        }

    });
    $("button").click(function(){
        var $games = $(this).parent().parent().nextUntil(".gamedeals").find('.new');
        if ($games.css("display") == 'none'){
            $games.slideDown()
        } else if ( $games.css('display') == 'block') {
            $games.slideUp();
        }
    });
});