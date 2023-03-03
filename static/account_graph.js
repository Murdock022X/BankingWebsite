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
                    borderColor: "rgb(35, 209, 96)",
                    lineTension: 0.1
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
                yAxes: [{
                    display: true,
                    ticks: {
                        beginAtZero: true,
                        steps: 20,
                        stepValue: data.step_val,
                        max: data.chart_max
                    }
                }]
            }
        }
    });
}

fetch(url).then(data => data.json()).then((data) => make_chart(data))
