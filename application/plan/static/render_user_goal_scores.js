const dataSrcRoot = `${window.location.origin}/tracking/user_goal_scores` //"http://localhost:5000/tracking/scoring_sys"

// TODO: Data caching for responsive website

// Load the Visualization API and the corechart package.
google.charts.load('current', {'packages':['corechart']});

google.charts.setOnLoadCallback(drawChart)

function drawChart() {
    const stepchart_objs = $(".gviz_user_scores_g")

    for (let index = 0; index < stepchart_objs.length; index++) {
        const element = stepchart_objs[index];

        drawStepChart(element.dataset.goal_id, element.dataset.qty_days, element.id)
    }
}

async function getChartData(goal_id, qty_days) {
    const res = await axios.get(`${dataSrcRoot}`, { params: {goal_id, qty_days} });
    return res;
}

async function drawStepChart(goal_id, qty_days, target_div) {
    const jsonData = await getChartData(goal_id, qty_days)
    
    // Create our data table out of JSON data loaded from server.
    var data = new google.visualization.DataTable(jsonData.data);

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

//!**!// Need to look into a better way to do this.  Causes to many queries in this form.
// $(window).resize(function(){
//     drawChart();
// });