$(document).ready(function(){
//    $('#home_page').addClass("active");
    if ($(window).width() < 768) {
            $('.filters').hide();
    }
    else {
        $('.filters').show();
    }
    $(window).resize(function() {
        if ($(window).width() < 768) {
            $('.filters').hide();
        }
        else {
            $('.filters').show();
        }
    });

    var filters = [];
//    $('label').class()
//    $('label').change(function(){
//        $(this).toggleClass("checked");
//    });

    $('label').change(function(){
//        $(this).toggleClass("checked");
        var $filter_input = $(this).find('input');
        if ($filter_input.is(':checked')){
            filters.push($filter_input.val());
            filters.sort();
        }
        else {
            var index = filters.indexOf($filter_input.val());
            filters.splice(index, 1);
        };
        console.log(filters);
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

    $('#filters_button').click(function(){
        $('.navbar-collapse').removeClass('in');
        $('.filters').toggle();
        $('.filters').toggleClass('open');
        $('.row.content').toggleClass('open');
        $('.messages').hide();
    });

    $('.btn.btn-danger').click(function(){
        $('.filters').toggleClass('open');
        $('.row.content').toggleClass('open');
        $('.filters').fadeToggle(300);
    });

    $('.navbar-toggle').click(function(){
        $('.filters').removeClass('open');
        $('.row.content').removeClass('open');
        $('.filters').attr("display","none");
    })
});