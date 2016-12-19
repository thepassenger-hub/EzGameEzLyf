$(document).ready(function(){
    $('.alldeals').hide();
    var $faketitle = null;
    $('.gametitle').click(function(){
        window.scrollTo(0, 0);
        $faketitle = $(this).attr('ref');
        $('#alldeals'+$faketitle).show();
        $('#alldeals'+$faketitle).toggleClass('open');
        $('.row.content').toggleClass('open');
        $('.row.content').toggle();
        $('.footer').toggle();
        $('hr').toggle();


//        $('.container-fluid').attr('height', '100%');
    });
    $('.btn.btn-danger').click(function(){
        $('#alldeals'+$faketitle).toggleClass('open');
        $('.row.content').toggle();
        $('.row.content').toggleClass('open');
        $('.alldeals').hide();
        $('.footer').toggle();
        $('hr').toggle();
    });
    /*$('.new').hide()
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
    });*/

    /*$("button").click(function(){
        var $faketitle = $(this).attr('id')
        var $mymodal = $('#'+$faketitle)
        $mymodal.modal('show')

    });*/
});