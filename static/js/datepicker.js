$("#id_date").click(function(){
});
$(document).ready(function(){
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
    setDays(todaysDate, todaysDate)
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
function setDays(todaysDate, viewMonth, dateSelected){
    var i = 1, j, k, cell, cellObj, remainingCells, allCells;
    var d = new Date(viewMonth['year'],viewMonth['month']-1,1);
    var firstDay = d.getDay();
    var totalDays = viewMonth['totalDays']
    $(".calendar-row .cell-occupied").removeClass("cell-occupied cell-disabled");
    $(".calendar-row .todays-date").removeClass("todays-date");
    $(".calendar-row .date-selected").removeClass("date-selected");
    $(".calendar-row .is-empty").removeClass("is-empty");
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
                    if(viewMonth['month']===todaysDate['month']&&viewMonth['year']===todaysDate['year']){
                        allCells = $('.calendar-row .cell-occupied');
                        for(k=0;k<allCells.length;k++){
                            if(allCells[k].textContent<todaysDate['day']){
                                allCells[k].className += " cell-disabled";
                            } else if(allCells[k].textContent===todaysDate['day']){
                                
                            };
                        }
                    }
                    if(dateSelected!=null){
                        if(dateSelected.length>0){
                            $(`.calendar-row td button[data-year='${dateSelected[0]}'][data-month='${dateSelected[1]}'][data-date='${dateSelected[2]}']`).addClass("date-selected");
                            
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
    };
}