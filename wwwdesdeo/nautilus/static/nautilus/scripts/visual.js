$(document).ready(() => {
    /* Create a click handler that works with bar graphs. On click, send the 
       solution corresponding to he graph(s) as a post request back to the backend.
     */
    if (visualizationDivId) {
	var myPlot = document.getElementById(visualizationDivId);
	if (myPlot) {
	    const preference = [];
	    myPlot.on('plotly_click', data => {
		// Get the index of the solution
		const index = data.points[0].x;
		// for (var i=0; i < data.points.length; i++) {
		//     preference.push(data.points[i].y);
		// }
		post({selection: index});
	    });
	}
    }
});

/* Accesses the rendered 'iteration-response-form' and creates field in it with 
   the contents of params. 
*/
function post(params, method='post') {
    const form = document.getElementById('iteration-response-form');

    for (const key in params) {
	if (params.hasOwnProperty(key)) {
	    const hiddenField = document.createElement('input');
	    hiddenField.type = 'hidden';
	    hiddenField.name = key;
	    hiddenField.value = params[key];

	    form.appendChild(hiddenField);
	}
    }
    document.body.appendChild(form);
    form.submit();
}		  


