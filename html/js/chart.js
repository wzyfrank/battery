let lmp = [0.03617, 0.03688, 0.03338, 0.03082, 0.03211, 0.03424, 0.03486, 0.03563, 0.04295,
 0.05626, 0.11322, 0.08718, 0.1373,  0.17736, 0.20782, 0.18566, 0.19912, 0.23981,
 0.1903, 0.09727, 0.15398, 0.16292, 0.04909, 0.04853];

let power = [ -0, -0, 25, 25, 25, 14.48, 0, 0, 0, 0, -22.56, 25, 0, 0, -25, 0, -25, -25, -5.75, 25, 0, -22.56, 0, 0];

let energy = [10, 10, 10, 33.75, 57.5, 81.25, 95, 95, 95, 95, 95, 71.25, 95, 95, 95, 68.68, 68.68, 42.37, 16.05, 10, 33.75, 33.75, 10, 10];

function PopulateDataPoints(data) {
    let dps = [];
    for (let i = 0; i < lmp.length; i++) {
        dps.push({
            x: i,
            y: data[i]
        });
    }
    return dps;
}


function ComposeChart(id, chart_title, axis_x, axis_y, data_points, chart_type) {
    let chart = new CanvasJS.Chart(id, {
        title: {
            text: chart_title
        },
        axisX: {
            title: axis_x
        },
        axisY: {
            title: axis_y
        },
        data: [{
            type: chart_type,
            color: "green",
            dataPoints: data_points
        }]
    });

    chart.render();
}
//Taking user input and adding it to dataPoint
window.onload = function(){
    // addDataPoints();
    ComposeChart("chart1", "locational marginal price",
        "hour", "price $/kWh", PopulateDataPoints(lmp), "line");
    ComposeChart("chart2", "charging/discharging power",
        "hour", "kW", PopulateDataPoints(power), "column");
    ComposeChart("chart3", "energy stored in battery",
        "hour", "kWh", PopulateDataPoints(energy), "line");
};
