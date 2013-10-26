
function addclass(classroom) {
    obj = JSON.stringify(classroom);
    $.ajax({
        type: 'POST',
        url: "/api/classroom",
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
	Name: 'Grade 8',
	SchoolName: 'Phoenix High School',
	NumberOfStudents: 23,
	Subjects: [ 'Physics', 'Maths' ],
	Location: { Name: 'Phoenix High School, White City',
		    Latitude: 289133.33,
		    Longitude: 38928.3 },
	AverageGrades: [{ Date: 'Sat Oct 13 13:36:20 2013', Grade: 10},
			{ Date: 'Sat Oct 26 13:36:20 2013', Grade: 7}],
	Description: 'Cool School'
    }
))
