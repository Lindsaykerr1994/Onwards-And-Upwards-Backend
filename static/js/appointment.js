$("#client_select").change(handleClientChange);
$("#id_activity_select").change(handleActivityChange);
$("#id_solo").change(handleSoloChange);
$("#id_course").change(handleCourseChange);
$("#id_number_participants").change(handleNumberChange);

function handleClientChange() {
    var clientNo = $("#client_select").val();
    var clientOpt = $(`#client_select option[value='${clientNo}']`);
    var firstName = clientOpt.attr("data-first-name");
    $("#id_client_first_name").val(firstName);
    var lastName = clientOpt.attr("data-last-name");
    $("#id_client_last_name").val(lastName);
    var emailAdd = clientOpt.attr("data-email");
    $("#id_client_email").val(emailAdd);
    var phoneNum = clientOpt. attr("data-phone");
    $("#id_client_phone").val(phoneNum)
};
function handleActivityChange() {
    var activity = $("#id_activity_select").val();
    $("#id_course option").addClass("d-none");
    if($("#id_solo").is(":checked")){
        options = $(`#id_course option[data-activity="${activity}"][data-solo="True"]`);
    } else {
        options = $(`#id_course option[data-activity="${activity}"][data-solo="False"]`);
    };
    options.removeClass("d-none");
    if($("#id_course").val()!==null){
        $("#id_course").val("0");
    };  
}
function handleCourseChange() {
    var code = $("#id_course").val();
    var NOP = parseInt($("#id_number_participants").val());
    if(Number.isNaN(NOP)){
        if($("#id_solo").is(":checked")){
            $("#id_number_participants").val(1);
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
        var i, altOption;
        var option = $(`#id_course option:selected`);
        var optionText = $(option).text().trim();
        var solo = $(option).attr("data-solo");
        if(solo==="True"){
            solo = "False";
        } else {
            solo = "True";
        }
        var activity =  $(option).attr("data-activity");
        var altOptions = $(`option[data-activity="${activity}"][data-solo="${solo}"]`);
        for(i=0;i<altOptions.length;i++){
            var text = altOptions[i].textContent.trim();
            if(text == optionText){
                altOption = altOptions[i];
            }
        }
        var altOptionVal = altOption.value;
        $("#id_course").val(altOptionVal);
        $("#id_course option").addClass("d-none");
        $(`#id_course option[data-activity=${activity}][data-solo=${solo}]`).removeClass("d-none");
        calculatePrice(altOptionVal);
    } else {
        activity = $("#id_activity_select").val();
        console.log(activity);
        $(`#id_course option`).addClass("d-none");
        if($("#id_solo").is(":checked")){
            console.log("show solo courses")
            $(`#id_course option[data-activity="${activity}"][data-solo="True"]`).removeClass("d-none");
        } else {
            console.log("show group")
            $(`#id_course option[data-activity="${activity}"][data-solo="False"]`).removeClass("d-none");
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
    handleSoloChange();
    var code = $("#id_course").val();
    calculatePrice(code);
}
function calculatePrice(code) {
    var NOP = parseInt($("#id_number_participants").val());
    if(Number.isNaN(NOP)){
        if($("#id_solo").is(":checked")){
            NOP = 1;
        } else {
            NOP = 2;
        }
    }
    var option = $(`#id_course option[value="${code}"]`);
    var price = parseInt($(option).attr("data-price"));
    var cost = price*NOP;
    if(Number.isNaN(cost)){
        return;
    }
    $("#id_price").val(cost);
    $("#id_price").trigger('change');
}

$("#id_override_price").change(function(){
    if($("#id_override_price").is(":checked")){
        $("#id_price").attr("readonly", false);
    } else {
        $("#id_price").attr("readonly", true);
    }
})