$(document).ready(function(){
//    $('#home_page').addClass("active");
    $('.filters').hide();
    $('#search_button').click(function(){
        var $input = $('#tftextinput');
        /* Check if there is valid input */
        if ($.trim($input.val()).length) {
            $('#loadingpage').show();
        };

    });

    $('#tftextinput').click(function(){
        $('.messages').hide();
    });

//    $('.navbar-toggle').click(function(){
//        $('.container-fluid').toggleClass('navbar-toggled');
//    });
    $('#filters').click(function(){
        $('.filters').show();
        $('.filters').toggleClass('open');
        $('.search-form').toggle();
        $('.messages').hide();
    });
});