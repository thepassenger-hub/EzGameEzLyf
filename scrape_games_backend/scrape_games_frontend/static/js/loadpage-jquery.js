$(document).ready(function(){
    $('#loadingpage').hide();
    $('.tfbutton').click(function(){
        var $input = $('.tftextinput')
        /* Check if there is valid input */
        if ($.trim($input.val()).length) {
            $('.messages').hide();
            $('#loadingpage').show();
        };
    });
});