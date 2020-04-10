
function fillSubProjects(){
    var selected_proj_id = $('#select-item-project').val();
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    console.log(selected_proj_id);
    $form=$('#select-form-form');
    $.ajax({
        // url : "clock/", // the endpoint
        url: $form.attr('data-sub-projects-url'),
        type : "GET", // http 
        headers:{
            "X-CSRFToken": csrftoken
        },
        data : { 'project_id' : selected_proj_id }, // data sent with the post request

        // handle a successful response
        success : function(data) {
            console.log("success"); // another sanity check
            console.log(data); // log the returned json to the console
            $('#select-item-sub-project').html(data)
            // $('#post-text').val(''); // remove the value from the input
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}
