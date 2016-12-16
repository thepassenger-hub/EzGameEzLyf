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
        $('#loadingpage').hide();
    });

    $('#filters').click(function(){
        $('.filters').show();
        $('.filters').toggleClass('open');
        $('.row.content').toggleClass('open');
        $('.messages').hide();
    });
    $('.btn.btn-danger').click(function(){
        $('.filters').toggleClass('open');
        $('.row.content').toggleClass('open');
    });
});