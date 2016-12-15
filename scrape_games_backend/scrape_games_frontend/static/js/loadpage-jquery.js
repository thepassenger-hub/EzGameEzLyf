$(document).ready(function(){
//    $('#home_page').addClass("active");
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
    $('#filters').click(function(){
        $('.filters').toggleClass('open');
        $('.search-form').toggle();
    });
});