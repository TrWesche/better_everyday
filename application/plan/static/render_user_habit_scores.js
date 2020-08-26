const dataSrcRoot = `${window.location.origin}/tracking/user_habit_scores`

let chartJson;

// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['corechart']});

google.charts.setOnLoadCallback(drawChart)

function drawChart() {
    const stepchart_objs = $(".gviz_user_scores_h")

    for (let index = 0; index < stepchart_objs.length; index++) {
        const element = stepchart_objs[index];

        drawStepChart(element.dataset.habit_id, element.dataset.qty_days, element.id)
    }
}

async function getChartData(habit_id, qty_days) {
    const res = await axios.get(`${dataSrcRoot}`, { params: {habit_id, qty_days} });
    return res;
}

async function drawStepChart(habit_id, qty_days, target_div) {
    if (!chartJson) {
        chartJson = await getChartData(habit_id, qty_days)
    }
    
    // Create our data table out of JSON data loaded from server.
    var data = new google.visualization.DataTable(chartJson.data);

    // Instantiate and draw our chart, passing in some options.
    var chart = new google.visualization.LineChart(document.getElementById(target_div));

    var options = {
        hAxis: {
            showTextEvery: 1,
            format: 'M/d',
            minorGridlines: {
                count: 0
            }
        },
        vAxis: {
            title: 'Score',
            minValue: 0
        },
        legend: { position: 'none' }
    };

    chart.draw(data, options);
}

$(window).resize(function(){
    drawChart();
});