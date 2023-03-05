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

function make_chart(data) {
    new Chart(document.getElementById("account_history_chart"), {
        type: "line",
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: "Balance",
                    data: data.values,
                    fill: false,
                    backgroundColor: "rgb(35, 209, 96)",
                    borderColor: "rgb(35, 209, 96)",
                    lineTension: 0.0
                }
            ]
        },
        options: {
            title: {
                display: true,
                text: 'Account Balance History'
            },
            hover: {
                mode: 'index',
                intersect: true
            },
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Date',
                        color: 'black'
                    },
                    grid: {
                        tickColor: 'black'
                    },
                    ticks: {
                        color: 'black'
                    }
                },
                y: {
                    display: true,

                    beginAtZero: true,
                    suggestedMax: data.chart_max,
                    title: {
                        display: true,
                        text: 'Balance (USD)',
                        color: 'black'
                    },
                    grid: {
                        tickColor: 'black'
                    },
                    ticks: {
                        color: 'black',
                        callback: (value) => {
                            return Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD'}).format(value);
                        }
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';

                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(context.parsed.y);
                            }
                            return label;
                        }
                    }
                }
            }
        }
    });
}

fetch(url).then(data => data.json()).then((data) => make_chart(data))
