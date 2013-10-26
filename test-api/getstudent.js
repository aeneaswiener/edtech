function getclass(id) {
    $.ajax({
        type: 'GET',
        url: "/api/classroom/"+id,
        xhrFields: {
            withCredentials: true
        },
        async: false,
        contentType: "application/json",
        success: function(result) {
            alert(JSON.stringify(result));
            console.dir(result);
        },
        error: function(e) {
            alert(JSON.stringify(e));
            console.log(e.message);
        }
    });	
}

$(document).ready(getclass('6473924464345088'))
