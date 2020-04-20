
function fillSubProjects(){
    var selected_proj_id = $('#select-item-project').val();
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajax({
        url: $('#select-item-sub-project').attr('data-url'),
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
            //console.log(data); // log the returned json to the console
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

function showToast(html){
    var $toast = $("#toast")
    $toast.html(html);
    $toast.toast('show');
}

function insert_time_entry(){
    console.log("Inserting time entry");
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();

    var $form=$('#timesheet-form');
    var serialized = $form.serialize();

    var proj = $("#select-item-project").children("option:selected").val()
    var sub_proj = $("#select-item-sub-project").children("option:selected").val()
    
    $.ajax({
        //contentType: 'application/x-www-form-urlencoded;charset=utf-8',
        url: $form.attr('data-url'),
        type : "POST", // http 
        headers:{
            "X-CSRFToken": csrftoken
        },
        data : serialized + "&proj="+proj+"&sub_proj="+sub_proj,

        // handle a successful response
        success : function(data) {
            console.log("success - Insert Entry"); // another sanity check

            showToast(data);
            loadTimsheet();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log("error - GenerateTimesheet");
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            //$toast.html('');'
            //showToast('error', "Error inserting entry");
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
            // showToast("success","Generated Timesheet");
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            //showToast("error","Error generating Timesheet");
        }
    });
}

function deleteEntries(url, rows_to_delete){
    var csrftoken = $("[name=csrfmiddlewaretoken]").val();        
    
    $.ajax({
        url: url,
        type : "POST", // Have to use post
        headers:{
            "X-CSRFToken": csrftoken
        },
        data : { 'arr':JSON.stringify(rows_to_delete)}, // data sent with the request

        // handle a successful response
        success : function(data) {
            console.log("success - Delete"); // another sanity check

            showToast(data);
            loadTimsheet();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
                " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            //showToast("error","Error deleting entry");
        }
    });
}

function deleteClicked(e) {
    var url = $(e).attr('data-url');
    var rows_to_delete = [];

    $('.entries :checkbox:checked').each(function() {
        // Name of checkbox is the primary key id
        rows_to_delete.push(this.name);
    });

    deleteEntries(url, rows_to_delete);
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

function animateCSS(element, animationName, callback) {
    const node = document.querySelector(element);
    node.classList.add('animated', animationName);

    function handleAnimationEnd() {
        node.classList.remove('animated', animationName);
        node.removeEventListener('animationend', handleAnimationEnd);

        if (typeof callback === 'function') callback();
    }

    node.addEventListener('animationend', handleAnimationEnd);
}

function clearSpan(){
    var $hour = $('#hour-input');
    var $minute = $('#minute-input');

    $hour.val('');
    $minute.val('');
}

function validateSpanInput(element){
    var value = element.val().toString();
    if (value == ""){value="0"};
    var parsed = /^\d+$/.test(value) ? value : NaN;

    if (isNaN(parsed)){
        console.log("error");
        element.addClass("error");
        
        return false;
    }
    else {
        element.removeClass("error");
        return parsed;
    }
}

// Parse hours/minutes and assign to spanbox
function fillTextInput(){
    var $hours = $('#hour-input');
    var $minutes = $('#minute-input');
    
    var hours = validateSpanInput($hours);
    var minutes = validateSpanInput($minutes);
    
    if (hours === false){
        $hours.focus();
        animateCSS('#span-picker', "shake");
        return;
    } else if (minutes === false) {
        $minutes.focus();
        animateCSS('#span-picker', "shake");
        return;
    }

    span = "";
    // Javascript is weird and "1" > 0 works
    if (hours > 0){
        span += hours;
        if (hours == "1") {
            span += " hour ";
        } else {
            span += " hours ";
        }
    }
    if (minutes > 0) {
        span += minutes;
        if (minutes == "1") {
            span += " minute";
        } else {
            span += " minutes";
        }
    }
    
    $('#id_span').val(span);
    clearSpan();
}

function formatTimesheetForm() {
    var time_format = {
        timepicker:true,
        datepicker:false,
        format:'H:i',
        step: 15
    };

    $('#id_day').datetimepicker({
        timepicker:false,
        datepicker:true,
        format: 'Y-m-d',
        dayOfWeekStart:1, // Start on Monday
        weeks: true,
        theme:'dark'
    });

    $('#id_start_at').datetimepicker(time_format);
    $('#id_end_at').datetimepicker(time_format);
};

function addSelectAllHandler(e){
    // e should be the select-all input checkbox
    if (e.checked){
        $('.entries :checkbox').each(function() {            
            this.checked = true;
        });
    } else {        
        $('.entries :checkbox').each(function() {
            this.checked = false;
        });
    }
}

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
    });

    // Refresh generated timesheet
    $('#refresh-generated-timesheet').click(function(e){
        e.preventDefault();
        generateTimesheet();
    });

    /* SPAN PICKER SECTION */
    // When enter pressed in span picker, focus out, fill spanbox, and clear span entries
    $('#span-picker').keydown(function(e){
        if (e.keyCode == 13) {
            var focused = $(':focus');
            focused.blur();
            fillTextInput();
        }
    });

    // Defer focus to span picker when spanbox focused
    $('#id_span').focus(function(e){
        var $spanbox = $(this);
        $hour = $('#hour-input');
        $minute = $('#minute-input');

        var value = $spanbox.val().toString();
        var value_arr = value.split(' ');

        if (value.search("hour") != -1) {
            $hour.val(value_arr[0]);
        }
        if (value.search("minute") != -1) {
            if (value.search("hour") == -1){
                $minute.val(value_arr[0]);
            } else {
                $minute.val(value_arr[2]);
            }
        }

        $hour.focus();
        $(this).attr('disabled','true');
    });

    $('#span-picker').focusout(function(e){
        if (!$('#span-picker').is(':focus-within')){
            $('#id_span').attr('disabled',false);
        }      
    });

    $('#span-picker input').each(function(){
        $(this).keyup(function() {
            validateSpanInput($(this));
        });
    });
    /* END SPAN PICKER SECTION */
}

function moveSpanPicker(){
    $('#span-picker').insertAfter($('#id_span'));
}

$(document).ready(function(){
    addListeners();
    formatTimesheetForm();
    fillSubProjects();
    loadTimsheet();
    generateTimesheet();
    moveSpanPicker();
});