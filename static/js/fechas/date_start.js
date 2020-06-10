function today(){
    //para poner fechas por default/falta checar bien
    var date = new Date();
    var day = date.getDate();
    var month = date.getMonth()+1;
    var year = date.getFullYear();

    if (month < 10) month = "0" + month;
    if (day < 10) day = "0" + day;

    return year + "-" + month + "-" + day;
}

function tomorrow(){
    //para poner fechas por default/falta checar bien
    var date = new Date();
    date.setDate(date.getDate() + 1);

    var day = date.getDate();
    var month = date.getMonth()+1;
    var year = date.getFullYear();

    if (month < 10) month = "0" + month;
    if (day < 10) day = "0" + day;

    return year + "-" + month + "-" + day;
}

$(function(){
    document.getElementById("date1").value = today();
    document.getElementById("date2").value = tomorrow();
});