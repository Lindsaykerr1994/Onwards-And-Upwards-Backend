;$("#id_client").change(handleClientChange);
$("#id_activity_select").change(handleActivityChange);
$("#id_solo").change(handleSoloChange);
$("#id_course").change(handleCourseChange);
$("#id_number_participants").change(handleNumberChange);
$("input[name='discount']").change(calculatePrice);

function handleClientChange() {
    var clientNo = $("#id_client").val();
    console.log(clientNo)
    var clientOpt = $(`#client-select .onwards-select-items div[data-pkey='${clientNo}']`);
    var firstName = clientOpt.attr("data-first-name");
    $("#id_client_first_name").val(firstName);
    var lastName = clientOpt.attr("data-last-name");
    $("#id_client_last_name").val(lastName);
    var emailAdd = clientOpt.attr("data-email");
    $("#id_client_email").val(emailAdd);
    var phoneNum = clientOpt. attr("data-phone");
    $("#id_client_phone").val(phoneNum)
    $(".form-input input[type='text']").trigger('change');
    $(".form-input input[type='email']").trigger('change');
    $("#client-fieldset input[type='text']").attr("readonly", true);
    $("#client-fieldset input[type='email']").attr("readonly", true);
};
function handleActivityChange() {
    console.log("changed activity");
    var activity = $("#id_activity_select").val();
    $("#course-select .onwards-select-items div").addClass("d-none");
    if($("#id_solo").is(":checked")){
        options = $(`#course-select .onwards-select-items div[data-activity="${activity}"][data-solo="True"]`);
    } else {
        options = $(`#course-select .onwards-select-items div[data-activity="${activity}"][data-solo="False"]`);
    };
    options.removeClass("d-none");
    if($("#id_course").val()!==null){
        $("#id_course").val("0");
    };  
}
function handleCourseChange() {
    console.log("changed course");
    var code = $("#id_course").val();
    console.log(code);
    var NOP = parseInt($("#id_number_participants").val());
    if(Number.isNaN(NOP)){
        if($("#id_solo").is(":checked")){
            $("#id_number_participants").val(1);
            $("#id_number_participants").change();
        } else {
            $("#id_number_participants").val(2);
            $("#id_number_participants").change();
        }
    }
    calculatePrice(code);
}
function handleSoloChange() {
    var num = $("#id_number_participants").val();
    if(Number.isNaN(num)){
    } else {
        var isSolo = $("#id_solo").is(":checked");
        if(isSolo){
            if(num>=2){
                num = 1;
                $("#id_number_participants").val(num);
            }
            $("#groupText").removeClass("text-orange");
            $("#soloText").addClass("text-orange");
        } else {
            $("#soloText").removeClass("text-orange");
            $("#groupText").addClass("text-orange");
        }
    }
    if($("#id_course").val()!==null){
        // Get current course
        var pkey = $("#id_course").val();
        var option = $(`#course-select .onwards-select-items div[data-pkey=${pkey}]`);
        // Get course name
        var optText = option.text().trim();
        // Solo Course or Group?
        var solo = $(option).attr("data-solo");
        if(solo==="True"){
            solo = "False";
        } else {
            solo = "True";
        }
        // Get course activity pk
        var activity = $(option).attr("data-activity");
        // Get the equivalent courses, same activity, different solo setting
        var altOptions = $(`#course-select .onwards-select-items div[data-activity="${activity}"][data-solo="${solo}"]`);
        // Search through them for the equivalent option
        for(i=0;i<altOptions.length;i++){
            var text = altOptions[i].textContent.trim();
            if(text == optText){
                altOption = altOptions[i];
            }
        }
        // Get the new course value
        var altOptionVal = altOption.getAttribute("data-pkey");
        // Update the hidden input
        $("#id_course").val(altOptionVal);
        // Hide the old courses
        $("#course-select .onwards-select-items div").addClass("d-none");
        // Show the new courses
        $(`#course-select .onwards-select-items div[data-activity=${activity}][data-solo=${solo}]`).removeClass("d-none");
        // Add "same-as-selected" to new option, while removing from old;
        $(`#course-select .onwards-select-items div`).removeClass("same-as-selected");
        $(`#course-select .onwards-select-items div[data-pkey=${altOptionVal}]`).addClass("same-as-selected");
        calculatePrice();
    } else {
        activity = $("#id_activity_select").val();
        $(`#course-select .onwards-select-items div`).addClass("d-none");
        if($("#id_solo").is(":checked")){
            $(`#course-select .onwards-select-items div[data-activity="${activity}"][data-solo="True"]`).removeClass("d-none");
        } else {
            $(`#course-select .onwards-select-items div[data-activity="${activity}"][data-solo="False"]`).removeClass("d-none");
        } 
    }
}
function handleNumberChange() {
    var num = $("#id_number_participants").val();
    var solo = $("#id_solo").is(":checked");
    if (num > 1){
        if(solo===true){
            $("#id_solo").attr("checked",false);
        }
    } else {
        if(solo===false){
            $("#id_solo").attr("checked",true);
        }
    }
    var code = $("#id_course").val();
    calculatePrice(code);
}
function calculatePrice() {
    var NOP = parseInt($("#id_number_participants").val());
    if(Number.isNaN(NOP)){
        if($("#id_solo").is(":checked")){
            NOP = 1;
        } else {
            NOP = 2;
        }
    }
    var code = $("#id_course").val();
    var option = $(`#course-select .onwards-select-items div[data-pkey="${code}"]`);
    var price = parseInt($(option).attr("data-price"));
    console.log(price);
    if($("#id_override_price").is(":checked")){
        var discount = parseInt($("input[name='discount']:checked").val());
        discount = (100-discount)/100;
        cost = (price*NOP)*discount;
    } else {
        cost = price*NOP;
    }
    if(Number.isNaN(cost)){
        return;
    }
    $("#id_price").val(cost.toFixed(2));
    $("#currency-sym").text("£");
    $("#id_price").trigger('change');
}
$("#id_override_price").change(function(){
    if($("#id_override_price").is(":checked")){
        $("#id_price").attr("readonly", false);
        $("#radio-input").fadeTo(400,1);
    } else {
        $("#id_price").attr("readonly", true);
        calculatePrice();
        $("#radio-input").fadeTo(400,0);
    }
})