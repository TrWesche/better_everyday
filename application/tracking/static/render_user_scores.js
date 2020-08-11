const dataSrcRoot = `${window.location.origin}/tracking/user_scores` //"http://localhost:5000/tracking/scoring_sys"

// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['corechart']});

google.charts.setOnLoadCallback(drawChart)

function drawChart() {
    const stepchart_objs = $(".gviz_user_scores")

    for (let index = 0; index < stepchart_objs.length; index++) {
        const element = stepchart_objs[index];

        drawStepChart(element.dataset.habit_id, element.dataset.qty_days, element.id, element.dataset.title)
    }
}

async function getChartData(habit_id, qty_days) {
    const res = await axios.get(`${dataSrcRoot}`, { params: {habit_id, qty_days} });
    return res;
}

async function drawStepChart(habit_id, qty_days, target_div, chart_title) {
    const jsonData = await getChartData(habit_id, qty_days)
    
    // Create our data table out of JSON data loaded from server.
    var data = new google.visualization.DataTable(jsonData.data);

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.SteppedAreaChart(document.getElementById(target_div));

    var options = {
        title: chart_title,
        vAxis: {title: 'Score'}
    };

    chart.draw(data, options);
}