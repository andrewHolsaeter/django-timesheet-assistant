
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

function insert_time_entry(){
    console.log("Inserting time entry");
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    var $form=$('#timesheet-form');
    var serialized = $form.serialize();
    console.log(serialized);
    var proj = $("#select-item-project").children("option:selected").val()
    var sub_proj = $("#select-item-sub-project").children("option:selected").val()
    
    var $toast=$('#toast');
    $.ajax({
        //contentType: 'application/x-www-form-urlencoded;charset=utf-8',
        url: $form.attr('data-url'),
        type : "POST", // http 
        headers:{
            "X-CSRFToken": csrftoken
        },
        data : serialized + "&proj="+proj+"&sub_proj="+sub_proj,
        
    //     { the_post: $form.val(),
    //     proj_id:proj,
    // sub_proj_id:sub_proj },
    // data sent with the post request

        // handle a successful response
        success : function(data) {
            console.log("success - Insert Entry"); // another sanity check
            // console.log(data); // log the returned json to the console
            //$toast.html(data);
            $toast.toast('show');
            loadTimsheet();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error - GenerateTimesheet");
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            //$toast.html('');
            $toast.toast('show');
        }
    });
}

function generateTimesheet(){
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    var $form=$('#generated-timesheet');
    var week = $("#week-input").val();
    var year = $("#year-input").val();

    $.ajax({
        
        url: $form.attr('data-url'),
        type : "GET", // http 
        headers:{
            "X-CSRFToken": csrftoken
        },
        data : { 'week' : week, 'year': year }, // data sent with the post request

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
    console.log(full_id);
    // Populate the Project ID Input on the timesheet form
   // $('#id_sub_project_id').val(sub_proj_id);
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

function addListeners(){
    // Week input
    $("#week-input").change(function(e){
        
        console.log("Week changed");
        generateTimesheet();
    });
    // Year input
    $("#year-input").change(function(e){
        console.log("Year changed");
        generateTimesheet();
    });

    // Submit entry form button
    $('#timesheet-form').submit(function(e){
        e.preventDefault();
        console.log("Submit handler hit");
        insert_time_entry();
    })
};

$(document).ready(function(){
    addListeners();
    formatTimesheetForm();
    fillSubProjects();
    loadTimsheet();
    generateTimesheet();
});