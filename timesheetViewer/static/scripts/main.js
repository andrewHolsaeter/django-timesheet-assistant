
function fillSubProjects(){
    var selected_proj_id = $('#select-item-project').val();
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    var $form=$('#select-form-form');

    $.ajax({
        url: $form.attr('data-sub-projects-url'),
        type : "GET", // http 
        headers:{
            "X-CSRFToken": csrftoken
        },
        data : { 'project_id' : selected_proj_id }, // data sent with the post request

        // handle a successful response
        success : function(data) {
            console.log("success - FillSubProjects"); // another sanity check
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

function loadTimsheet(){
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    var $form=$('#timesheet-table');
    query = null;

    $.ajax({
        
        url: $form.attr('data-timesheet-url'),
        type : "GET", // http 
        headers:{
            "X-CSRFToken": csrftoken
        },
        data : { 'query' : query }, // data sent with the post request

        // handle a successful response
        success : function(data) {
            console.log("success - LoadTimesheet"); // another sanity check
            // console.log(data); // log the returned json to the console
            $form.html(data);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function generateTimesheet(){
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $form=$('#generated-timesheet');
    week = 15;

    $.ajax({
        
        url: $form.attr('data-url'),
        type : "GET", // http 
        headers:{
            "X-CSRFToken": csrftoken
        },
        data : { 'week' : week }, // data sent with the post request

        // handle a successful response
        success : function(data) {
            console.log("success - GenerateTimesheet"); // another sanity check
            // console.log(data); // log the returned json to the console
            $form.html(data);
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

function formatTimesheetForm() {
    var time_format = {
        timepicker:true,
        datepicker:false,
        format:'H:i',
        step: 15
    };

    $('#id_date').datetimepicker({
        timepicker:false,
        datepicker:true,
        format: 'Y-m-d',
        week: true
    });

    $('#id_start_at').datetimepicker(time_format);
    $('#id_end_at').datetimepicker(time_format);
};


$(document).ready(function(){
    formatTimesheetForm();
    fillSubProjects();
    loadTimsheet();
    generateTimesheet();
});