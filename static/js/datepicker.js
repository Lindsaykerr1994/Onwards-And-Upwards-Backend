$("#id_date").click(function(){
    const fullDate = new Date();
    var year = fullDate.getFullYear();
    var month = fullDate.getMonth() + 1;
    var date = fullDate.getDate();
    var todaysDate = {
        'year': year,
        'month': month,
        'day': date,
        'totalDays': findTotalDays(month, year),
        'monthName': getMonthName(month)
    }
    setDays(todaysDate, todaysDate);
    toggleDatepicker();
});
$("#cancel-date").click(function(){
    $("#id_date").val("");
    toggleDatepicker()
});
$("#confirm-date").click(function(){
    toggleDatepicker();
})
$(".datepicker-button").click(function(){
    if(!$(this).hasClass("cell-disabled")&&!$(this).hasClass("is-empty")){
        if(!$(this).hasClass("date-selected")){
            var date = parseInt($(this).attr('data-date'));
            if(date<10){
                date = `0${date}`;
            }
            var month = parseInt($(this).attr('data-month'));
            if(month<10){
                month = `0${month}`;
            }
            var year = $(this).attr('data-year');
            var dateSelected = `${year}-${month}-${date}`;
            if($("#id_multiple_dates").is(":checked")){
                var dates = $("#id_date").val();
                if(dates.length>0){
                    dateSelected = dates+","+dateSelected;
                } else {
                    dateSelected = dateSelected;
                }
            } else {
                $(".datepicker-button").removeClass("date-selected");
            }
            $(this).addClass("date-selected");
            $("#id_date").val(dateSelected);
            $("#id_date").trigger('change');
        } else {
            var dates = $("#id_date").val();
            dates = dates.split(",");
            var date = parseInt($(this).attr('data-date'));
            if(date<10){
                date = `0${date}`;
            }
            var month = parseInt($(this).attr('data-month'));
            if(month<10){
                month = `0${month}`;
            }
            var year = $(this).attr('data-year');
            var dateSelected = `${year}-${month}-${date}`;
            var indexDate = dates.indexOf(dateSelected);
            dates.splice(indexDate,1);
            $("#id_date").val(dates);
            $("#id_date").trigger('change');
            $(this).removeClass("date-selected");
        }
    }
})
$("#next-month-button").click(function(){
    var currentMonth = parseInt($("#monthSelection").attr("data-month"));
    var year = parseInt($("#yearSelection").attr("data-year"));
    var nextMonth = currentMonth + 1;
    if(nextMonth===13){
        year = year + 1;
        nextMonth = nextMonth - 12;
    }
    viewMonth = {
        'year': year,
        'month': nextMonth,
        'totalDays': findTotalDays(nextMonth, year),
        'monthName': getMonthName(nextMonth)
    }
    const fullDate = new Date();
    var year = fullDate.getFullYear();
    var month = fullDate.getMonth() + 1;
    var date = fullDate.getDate();
    var todaysDate = {
        'year': year,
        'month': month,
        'day': date,
        'totalDays': findTotalDays(month, year),
        'monthName': getMonthName(month)
    }
    setDays(todaysDate, viewMonth);
})
$("#prev-month-button").click(function(){
    var currentMonth = parseInt($("#monthSelection").attr("data-month"));
    var year = parseInt($("#yearSelection").attr("data-year"));
    var prevMonth = currentMonth - 1;
    if($("#prev-month-button").hasClass("disabled-button")){
        return;
    } else {
        if(prevMonth===0){
            year = year - 1;
            prevMonth = prevMonth + 12;
        }
        viewMonth = {
        'year': year,
        'month': prevMonth,
        'totalDays': findTotalDays(prevMonth, year),
        'monthName': getMonthName(prevMonth)
        }
        const fullDate = new Date();
        var year = fullDate.getFullYear();
        var month = fullDate.getMonth() + 1;
        var date = fullDate.getDate();
        var todaysDate = {
            'year': year,
            'month': month,
            'day': date,
            'totalDays': findTotalDays(month, year),
            'monthName': getMonthName(month)
        }
        setDays(todaysDate, viewMonth);
    };
})
$("#id_multiple_dates").change(function(){
    if(!$(this).is(':checked')){
        var dates = $("#id_date").val();
        dates = dates.split(",");
        console.log(dates);
        if(dates.length>1){
            var singleDate = dates[0];
            $("#id_date").val(singleDate);
            singleDate = singleDate.split("-");
            cell = {
                'year': singleDate[0],
                'month': parseInt(singleDate[1]),
                'date': parseInt(singleDate[2])
            }
            $(".datepicker-button").removeClass("date-selected");
            $(`.datepicker-button[data-year=${cell['year']}][data-month=${cell['month']}][data-date=${cell['date']}]`).addClass("date-selected");
        }
    }
})
$("#monthText").click(function(){
    var textDiv = document.getElementById("monthText").children;
    $("#monthSelection").removeClass("d-none");
    $("#monthSelection").parent().addClass("openDropdown");
    $("#monthSelection div").click(function(){
        var newMonth = parseInt($(this).attr("data-month"));
        $("#monthSelection").attr("data-month", newMonth);
        var thisYear = parseInt($("#yearSelection").attr("data-year"));
        const fullDate = new Date();
        var year = fullDate.getFullYear();
        var month = fullDate.getMonth() + 1;
        var date = fullDate.getDate();
        var todaysDate = {
            'year': year,
            'month': month,
            'day': date,
            'totalDays': findTotalDays(month, year),
            'monthName': getMonthName(month)
        }
        var viewMonth = {
            'year': thisYear,
            'month': newMonth,
            'totalDays': findTotalDays(newMonth, thisYear),
            'monthName': getMonthName(newMonth)
        }
        setDays(todaysDate, viewMonth);
    });
    $(document).click(function(e){
        if(e.target != textDiv[0]){
            $("#monthSelection").addClass("d-none");
            $("#monthSelection").parent().removeClass("openDropdown");
        } 
    })
})
$("#yearText").click(function(){
    var textDiv = document.getElementById("yearText").children;
    $("#yearSelection").removeClass("d-none");
    $("#yearSelection").parent().addClass("openDropdown");
    $("#yearSelection div").click(function(){
        var newYear = parseInt($(this).attr("data-year"));
        $("#yearSelection").attr("data-year", newYear);
        var thisMonth = parseInt($("#monthSelection").attr("data-month"));
        const fullDate = new Date();
        var year = fullDate.getFullYear();
        var month = fullDate.getMonth() + 1;
        var date = fullDate.getDate();
        var todaysDate = {
            'year': year,
            'month': month,
            'day': date,
            'totalDays': findTotalDays(month, year),
            'monthName': getMonthName(month)
        }
        var viewMonth = {
            'year': newYear,
            'month': thisMonth,
            'totalDays': findTotalDays(thisMonth, newYear),
            'monthName': getMonthName(thisMonth)
        }
        setDays(todaysDate, viewMonth);
    });
    $(document).click(function(e){
        if(e.target != textDiv[0]){
            $("#yearSelection").addClass("d-none");
            $("#yearSelection").parent().removeClass("openDropdown");
        }
    })
})
$("#today-date").click(function(){
    const fullDate = new Date();
    var year = fullDate.getFullYear();
    var month = fullDate.getMonth() + 1;
    var date = fullDate.getDate();
    var todaysDate = {
        'year': year,
        'month': month,
        'day': date,
        'totalDays': findTotalDays(month, year),
        'monthName': getMonthName(month)
    }
    setDays(todaysDate, todaysDate);
})
function findTotalDays(month, year){
    var totalDays;
        if (month===2){
            if(year%4 === 0 && year%100 !== 0){
                totalDays = 29;
            } else {
                if(year%400 === 0){
                    totalDays = 29;
                } else { 
                    totalDays = 28;
                }
            }
        } else if(month===4||month===6||month===9||month===11){
            totalDays = 30;
        } else {
            totalDays = 31;
        }
        return totalDays;
};
function getMonthName(month){
    var names = ["January", "February", "March", "April", "May",
                "June", "July", "August", "September", "October",
                "November", "December"]
    var monthName = names[month-1];
    return monthName;
};
function setDays(todaysDate, viewMonth){
    var dateSelected = $("#id_date").val();
    if(dateSelected.length != 0){
        dateSelected = dateSelected.split(",");
    }
    var i = 1, ii, j, k, cell, cellObj, remainingCells, allCells;
    var d = new Date(viewMonth['year'],viewMonth['month']-1,1);
    var firstDay = d.getDay();
    var totalDays = viewMonth['totalDays']
    setTitle(viewMonth);
    $(".calendar-row .cell-occupied").removeClass("cell-occupied cell-disabled");
    $(".calendar-row .todays-date").removeClass("todays-date");
    $(".calendar-row .date-selected").removeClass("date-selected");
    $(".calendar-row .is-empty").removeClass("is-empty");
    // if($("#prev-month-button").attr("data-past-dates") != "true") {
    //     if(viewMonth['year']===todaysDate['year']&&viewMonth['month']===todaysDate['month']){
    //         $("#prev-month-button").addClass(" disabled-button");
    //     } else {
    //         $("#prev-month-button").removeClass("disabled-button");
    //     }
    // }
    while(i<=totalDays){
        for(j=0;j<6;j++){
            if(j===0){
                cell = firstDay;
            } else {
                cell=0;
            };
            for(cell;cell<7;cell++){
                cellObj=$(`.calendar-row:eq(${j}) td:eq(${cell}) button:eq(0)`);
                cellObj.text(i);
                cellObj.addClass("cell-occupied");
                cellObj.attr("data-date",i);
                cellObj.attr("data-month",viewMonth['month']);
                cellObj.attr("data-year",viewMonth['year']);
                i++;
                if(i>totalDays){
                    remainingCells=$(`.calendar-row td button:not(.cell-occupied)`);
                    remainingCells.addClass("is-empty");
                    $(".calendar-row .is-empty").text("");
                    $(".calendar-row .is-empty").attr("data-date","");
                    $(".calendar-row .is-empty").attr("data-month","");
                    $(".calendar-row .is-empty").attr("data-year","");
                    // if(viewMonth['month']===todaysDate['month']&&viewMonth['year']===todaysDate['year']){
                    //     allCells = $('.calendar-row .cell-occupied');
                    //     for(k=0;k<allCells.length;k++){
                    //         if(allCells[k].textContent<todaysDate['day']){
                    //             allCells[k].className += " cell-disabled";
                    //         } else if(allCells[k].textContent===todaysDate['day']){
                                
                    //         };
                    //     }
                    // }
                    if(dateSelected!=null){
                        for(ii=0;ii<dateSelected.length;ii++){
                            var sD = dateSelected[ii].split("-");
                            var selectDate = {
                                'year': sD[0],
                                'month': parseInt(sD[1]),
                                'date': parseInt(sD[2])
                            }
                            $(`.datepicker-button[data-year='${selectDate['year']}'][data-month='${selectDate['month']}'][data-date='${selectDate['date']}']`).addClass("date-selected");
                        }
                    }
                    var todaysCell = $(`.calendar-row td button[data-year='${todaysDate['year']}'][data-month='${todaysDate['month']}'][data-date='${todaysDate['day']}']`);
                    if(todaysCell.length>0){
                        todaysCell.addClass("todays-date");
                    };
                    return;
                }
            }
        }
    }
};
function setTitle(viewMonth){
    var month = viewMonth['month'];
    var year = viewMonth['year'];
    $("#monthSelection").attr("data-month",viewMonth['month']);
    $("#yearSelection").attr("data-year",viewMonth['year']);
    $("#monthText span").text(viewMonth['monthName']);
    $("#monthSelection div").removeClass("selectedMonth");
    $(`#monthSelection div[data-month=${month}]`).addClass("selectedMonth");
    $("#yearText span").text(viewMonth['year']);
    $("#yearSelection div").removeClass("selectedYear");
    $(`#yearSelection div[data-year=${year}]`).addClass("selectedYear");

}
function toggleDatepicker(){
    if($("#datepickerModal").hasClass("datepickerOpen")){
        $("#datepickerModal").removeClass("datepickerOpen");
    } else {
        $("#datepickerModal").addClass("datepickerOpen");
    }
}
$(document).ready(function(){
    var thisYear = new Date().getFullYear();
    for(let i=0;i<100;i++){
        var newYear = (thisYear-97)+i;
        $("#yearSelection").append(`<div data-year='${newYear}'>${newYear}</div>`)
    }
})