$(document).ready(function(){
    function startProgressBarUpdate() {
          g_progress_intv = setInterval(function() {
                $.getJSON("/get_upload_progress/", function(data) {
                  if (data == null) {
                    $("#uploadprogressbar").text("100");
                    clearInterval(g_progress_intv);
                    g_progress_intv = 0;
                    return;
                  }
                  var percentage = parseFloat(data.progress_bar);
                  $("#uploadprogressbar").text(percentage);
                });
              }, 500);
          if(g_progress_intv != 0)
              clearInterval(g_progress_intv);
        }
    function progress_bar_update(){
        g_progress_intv = setInterval(function() {
            $.getJSON("/get_upload_progress/", function(result){
                var percentage = parseFloat(result.progress_bar);
                $("#uploadprogressbar").text(percentage);
                $(".progress-bar").css('width', percentage+'%');
                $(".progress-bar").text(Math.floor(percentage)+'% Complete');
            });
        }, 500);
    };

    $('#home_page').addClass("active");
    $('#search_button').click(function(){
        var $input = $('#tftextinput')
        /* Check if there is valid input */
        if ($.trim($input.val()).length) {
            $('#loadingpage').show();
            $('.progress').show();
            progress_bar_update();
        };

    });

    $('#tftextinput').click(function(){
        $('.messages').hide();

    });



});