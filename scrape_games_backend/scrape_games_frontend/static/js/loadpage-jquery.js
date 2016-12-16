$(document).ready(function(){
//    $('#home_page').addClass("active");


    $('.filters').hide();
    var filters = [];
    $('label').click(function(){
        var $tony = $(this).find('input');
        if ($tony.is(':checked')){
            console.log($tony.val());
            filters.push($tony.val());
            console.log(filters);
        }
        else {
            var index = filters.indexOf($tony.val());
            filters.splice(index, 1);
            console.log(filters);
        };
    });
    $('#search_button').click(function(){
        var $input = $('#tftextinput');
        /* Check if there is valid input */
        if ($.trim($input.val()).length) {
            $('#loadingpage').show();
        };
        if (filters.length){
            $('#storefilters').prop("disabled", false);
            $('#storefilters').val(filters);
            console.log($('#storefilters').val());
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