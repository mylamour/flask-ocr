// hide buttons

window.onload = function() {
    console.log("dom is ready!");

    function clear() {
        $('#err_result').hide()
        $('#alert_result').hide()
        $('#result_text').hide()
    }

    function show_correct_result(result) {
        $('#logo').hide()
        clear()
        $('#alert_result').show()
        $('#result_text').show()
        $('#result_text').val(result['output'])
    }

    function show_err_result(result) {
        $('#logo').hide()
        clear()
        $('#err_result').show()
        $('#result_text').show()
        $('#result_text').val(result['error'])
    }

    clear()

    $("#upload_image").dropzone({
        maxFiles: 2000,
        success: function(file, response){
            show_correct_result(response)
        }
    });

    console.log('CAI');

      $('#search').on('click',function(event){
             $('#err_result').hide()
             $('#alert_result').hide()
             //$('#result_text').hide()

          value = $('#image_url').val();
          //alert(value);
          event.preventDefault();
          $.ajax({
              type: "POST",
              url: "/ocrit",
              contentType: "application/json",
              dataType: "json",
              data : JSON.stringify({ "image_url" : value }),
              success: function(result) {
                  console.log(result);
                  if (typeof(result['error']) != "undefined"  ){
                      show_err_result(result)
                  }else{
                      show_correct_result(result)
                  }
                  //alert(result);
                  //$("#post-form").hide();
                  //$("#retry").show();
                  //$("#results").show();
                  //$("#results").html("<h3>Image</h3><img src="+value+" style='max-width: 400px;'><br><h3>Results</h3><div class='well'>"+
                  //result["output"]+"</div>");
              },
              error: function(error) {
                    console.log(error);
                  }
          });
            });

    //$('#url_form').on('submit', function(event){
    //
    //
    //  });


};


    //function drawImage(){
    //    var ctx = $("canvas")[0].getContext("2d"),
    //        img = new Image();
    //
    //    img.onload = function(){
    //        ctx.drawImage(img, 0, 0, 500, 500);
    //        $("span").text("Loaded.");
    //    };
    //    img.src = "http://photojournal.jpl.nasa.gov/jpeg/PIA17555.jpg";
    //    $("span").text("Loading...");
    //}
    //
    //$("button").click(drawImage);
