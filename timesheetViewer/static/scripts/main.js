
function fillSubProjects(){
    var selected_proj_id = $('#select-item-project').val();
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $form=$('#select-form-form');

    $.ajax({
        url: $form.attr('data-sub-projects-url'),
        type : "GET", // http 
        headers:{
            "X-CSRFToken": csrftoken
        },
        data : { 'project_id' : selected_proj_id }, // data sent with the post request

        // handle a successful response
        success : function(data) {
            console.log("success"); // another sanity check
            // console.log(data); // log the returned json to the console
            $('#select-item-sub-project').html(data);

            // Populate the Project ID Input on the timesheet form
            displayFullId();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function displayFullId(){
    // MIGHT NEED TO CHANGE TO AJAX OR ATLEAST ADD A TIMEOUT HERE TO BE SAFE
    var proj_id = $('#select-item-project').val().toString();
    var sub_proj_id = $('#select-item-sub-project').val().toString();
    var full_id = proj_id + '-' + sub_proj_id;

    // Populate the Project ID Input on the timesheet form
    $('#id_full_project_id').val(full_id);
}