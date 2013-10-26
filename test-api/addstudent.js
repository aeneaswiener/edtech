
function addclass(classroom) {
    obj = JSON.stringify(classroom);
    $.ajax({
        type: 'POST',
        url: "/api/students",
        xhrFields: {
            withCredentials: true
        },
        async: false,
        contentType: "application/json",
        data: obj,
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

$(document).ready(addclass(
    {
	Name: 'Felix',
	SchoolName: 'Phoenix High School',
	NumberOfStudents: 23,
	Subject: 'Physics',
	SchoolLocation: { Name: 'Phoenix High School, White City',
		    Latitude: 51.514490,
		    Longitude: -0.116849 },
	AverageGrades: [{ Date: '2013-10-13', Grade: 10},
			{ Date: '2013-10-26', Grade: 7}],
	Description: 'I need help'
    }
))
