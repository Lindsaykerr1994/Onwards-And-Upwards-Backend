// Open/Close The 'Select' Option List
$(".onwards-select-display").click(function(event){
    event.stopPropagation();
    var display, itemsList;
    display = $(this);
    itemsList = display.siblings(".onwards-select-items");
    display.toggleClass("active-arrow");
    itemsList.toggleClass("select-open");
    itemsList.fadeToggle("fast");
});
// Selecting An Option
$(".onwards-select-items div").click(function(event){
    event.stopPropagation();
    // Get activity id
    var pKey = $(this).attr("data-pkey");
    var optText = $(this).text();
    // Assign to input
    var input = $(this).parent().siblings("input");
    input.val(pKey);
    console.log(input);
    input.trigger('change');
    // Update select display
    var display = $(this).parent().siblings().children("p");
    display.text(optText)
    // Remove all instances of class "same-as-selected";
    $(this).parent().children(".same-as-selected").removeClass("same-as-selected");
    // Add class of "same-as-selected"
    $(this).addClass("same-as-selected");
    $(this).parent().fadeToggle("fast");
    $(this).parent().toggleClass("select-open");
    $(this).parent().siblings(".onwards-select-display").toggleClass("active-arrow");
});
$(window).click(function(){
    $(".onwards-select-display").removeClass("active-arrow");
    $(".select-open").fadeToggle("fast");
    $(".select-open").removeClass("select-open");
})