$(document).ready(function(){
//    $('#home_page').addClass("active");


    $('.filters').hide();
    var filters = [];
    $('label').click(function(){
        var $filter_input = $(this).find('input');
        if ($filter_input.is(':checked')){
            filters.push($filter_input.val());
        }
        else {
            var index = filters.indexOf($filter_input.val());
            filters.splice(index, 1);
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
        };
    });

    $('#tftextinput').click(function(){
        $('.messages').hide();
        $('#loadingpage').hide();
    });

    $('#filters').click(function(){
        $('.navbar-collapse').removeClass('in');
        $('.filters').show();
        $('.filters').toggleClass('open');
        $('.row.content').toggleClass('open');
        $('.messages').hide();
    });
    $('.btn.btn-danger').click(function(){
        $('.filters').toggleClass('open');
        $('.row.content').toggleClass('open');
    });
    $('.navbar-toggle').click(function(){
        $('.filters').removeClass('open');
        $('.row.content').removeClass('open');
    })
});