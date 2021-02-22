$("#client_select").change(function(){
    var clientNo = $(this).val();
    var clientOpt = $(`#client_select option[value='${clientNo}']`);
    var firstName = clientOpt.attr("data-first-name");
    $("#id_client_first_name").val(firstName);
    var lastName = clientOpt.attr("data-last-name");
    $("#id_client_last_name").val(lastName);
    var emailAdd = clientOpt.attr("data-email");
    $("#id_client_email").val(emailAdd);
    var phoneNum = clientOpt. attr("data-phone");
    $("#id_client_phone").val(phoneNum)
});
$("#id_activity_select").change(function(){
    var activity = $("#id_activity_select").val();
    $("#id_course option").addClass("d-none");
    if($("#id_solo").attr("checked",true)){
        options = $(`#id_course option[data-activity="${activity}"][data-solo="True"]`);
        
    } else {
        options = $(`#id_course option[data-activity="${activity}"][data-solo="False"]`);
    };
    options.removeClass("d-none");
    if($("#id_course").val()!==null){
        $("#id_course").val("0");
    };  
});
$("#id_solo").change(function(){
    if($("#id_course").val()!==null){
        var i, altOption;
        var option = $(`#id_course option:selected`);
        var optionText = $(option).text().trim();
        console.log(optionText)
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

    }
});
$("#id_course").change(function(){
    var code = $("#id_course").val();
    calculatePrice(code);
})
function calculatePrice(code) {
    var option = $(`#id_course option[value="${code}"]`);
    var price = parseInt($(option).attr("data-price"));
    var NOP = parseInt($("#id_number_participants").val());
    var cost = price*NOP;
    console.log(cost);
}