// A plugin from chart.js to affect the chartAreaBorder. Not used currently.
/*
const chartAreaBorder = {
    id: 'chartAreaBorder',
    beforeDraw(chart, args, options) {
      const {ctx, chartArea: {left, top, width, height}} = chart;
      ctx.save();
      ctx.strokeStyle = options.borderColor;
      ctx.lineWidth = options.borderWidth;
      ctx.setLineDash(options.borderDash || []);
      ctx.lineDashOffset = options.borderDashOffset;
      ctx.strokeRect(left, top, width, height);
      ctx.restore();
    }
};
*/

/**
 * Formats a date string of type MM-DD-YYYY into Month Day, Year.
 * @param {string} date The date string.
 *  
 * @returns {string} The new formatted date string.
 */
function format_date(date) {
    // Map the last digit in each day to a correct new ending.
    var day_map = {0: '0th', 1: '1st', 2: '2nd', 3: '3rd', 4: '4th', 
    5: '5th', 6: '6th', 7: '7th', 8: '8th', 9: '9th'};

    // Map integer representations to months in the year.
    var month_map = {1: 'January', 2: 'February', 3: 'March', 4: 'April', 
    5: 'May', 6: 'June', 7: 'July', 8: 'August', 9: 'September', 
    10: 'October', 11: 'November', 12: 'December'};

    // Split the date string into parts.
    var parts = date.split('-');

    // Map the month into the string.
    var res = month_map[parseInt(parts[0])] + ' ';

    // Add the first digit of the day if not 0.
    if (parts[1][0] !== '0') {
        res += parts[1][0];
    }

    // Map the formatted second digit into the string as well as the year.
    res += day_map[parseInt(parts[1][1])] + ', ' + parts[2];

    return res;
}

/**
 * Creates a line chart of previous account history.
 * 
 * @param {JSON} data JSON data which has labels and values, used 
 * to define each point on our chart.
 */
function make_chart(data) {
    // Create the new chart element, target canvas with id 
    // account_history_chart.
    new Chart(document.getElementById("account_history_chart"), {
        // Type of chart is a line chart.
        type: "line",

        // Defines data to be used in our line chart.
        data: {

            // X values
            labels: data.labels,

            // Defines points.
            datasets: [
                {
                    // These points are the balance at the given time.
                    label: "Balance",

                    // Y value corresponding to label at same index.
                    data: data.values,

                    fill: false,
                    backgroundColor: "rgb(35, 209, 96)",
                    borderColor: "rgb(35, 209, 96)",

                    // Makes lines connecting points straight, adjust 
                    // closer to 1.0 to make more curvy.
                    lineTension: 0.0
                }
            ]
        },

        // Customize chart.
        options: {

            // Defines on hover activity.
            hover: {
                mode: 'index',
                intersect: true
            },

            // Axes configurations
            scales: {

                // X axis
                x: {
                    display: true,

                    // Title of X axis.
                    title: {
                        display: true,

                        // X axis is date axis.
                        text: 'Date',

                        // Text is black.
                        color: 'black',

                        // Text size is 16.0.
                        font: {
                            size: 16
                        }
                    },

                    // Target grid.
                    grid: {

                        // Color the ticks on X axis black.
                        tickColor: 'black'
                    },

                    // Target ticks.
                    ticks: {
                        // Color ticks black.
                        color: 'black',

                        // Callback function uses format_date function 
                        // defined above to convert into Month Day, 
                        // Year format.
                        callback: function(label) {
                            return format_date(this.getLabelForValue(label));
                        }
                    }
                },

                // Y axis
                y: {
                    display: true,

                    // Values should begin at 0.
                    beginAtZero: true,

                    // Target title.
                    title: {
                        display: true,

                        // Y axis is balance.
                        text: 'Balance (USD)',

                        // Color title black.
                        color: 'black',

                        // Font
                        font: {
                            // Title font size = 16.0.
                            size: 16
                        }
                    },

                    // Grid ticks colored black.
                    grid: {
                        tickColor: 'black'
                    },

                    // Target ticks.
                    ticks: {

                        // Color ticks black.
                        color: 'black',

                        // Format money into USD monetary format.
                        callback: (value) => {
                            return Intl.NumberFormat('en-US', 
                            { style: 'currency', 
                            currency: 'USD'}).format(value);
                        }
                    }
                }
            },

            plugins: {
                // Target tooltips (the labels that pop up when you 
                // hover over a datapoint).
                tooltip: {

                    // Callback functions
                    callbacks: {

                        // Target the title of tooltip and format the date 
                        // using the previously defined date function.
                        title: (tooltipItems) => {
                            return format_date(tooltipItems[0].label);
                        },

                        // Target the label of the tooltip and 
                        // issue a callback.
                        label: function(context) {

                            // Get the label for the current tooltip.
                            let label = context.dataset.label || '';
                    
                            // Add ': '
                            if (label) {
                                label += ': ';
                            }

                            // Parse y value convert to USD monetary format 
                            // and add to new label.
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-US', 
                                { style: 'currency', 
                                currency: 'USD' }).format(context.parsed.y);
                            }

                            return label;
                        }
                    }
                }
            }
        }
    });
}

// Fetch data from passed url, convert is json and then make the chart.
fetch(url).then(data => data.json()).then((data) => make_chart(data))
