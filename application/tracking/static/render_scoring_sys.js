const dataSrcRoot = `${window.location.origin}/tracking/scoring_sys` //"http://localhost:5000/tracking/scoring_sys"

// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['corechart']});

google.charts.setOnLoadCallback(drawChart)

function drawChart() {
    const stepchart_objs = $(".gviz_scoring_sys")

    for (let index = 0; index < stepchart_objs.length; index++) {
        const element = stepchart_objs[index];

        drawStepChart(element.dataset.sys, element.id, element.dataset.title)
    }
}

async function getChartData(system) {
    const res = await axios.get(`${dataSrcRoot}`, { params: {system} });
    return res;
}

//  TODO: The stepchart display is not working currently.
async function drawStepChart(system, target_div, chart_title) {
    const jsonData = await getChartData(system)
    
    // Create our data table out of JSON data loaded from server.
    var data = new google.visualization.DataTable(jsonData.data);

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.SteppedAreaChart(document.getElementById(target_div));

    var options = {
        title: chart_title,
        hAxis: {title: 'Time Input'},
        vAxis: {title: 'Score Output'},
        legend: { position: 'none' }
    };

    chart.draw(data, options);
}