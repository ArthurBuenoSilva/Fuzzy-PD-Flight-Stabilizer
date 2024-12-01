let charts = {
    error: null,
    deltaError: null,
    power: null,
    result: null,
};

function getData(data) {
    const labels = data.labels;
    const datasets = data.memberships.map(set => ({
        label: set.name,
        data: set.values,
        borderColor: set.color,
        borderWidth: 2,
        fill: false,
    }));

    return {
        labels: labels,
        datasets: datasets,
    };
}

function getOptions(title, x, y, min, max, set_point) {
    return {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
            duration: 0,
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: x,
                    font: {
                        weight: "bold",
                    }
                },
            },
            y: {
                title: {
                    display: true,
                    text: y,
                    font: {
                        weight: "bold",
                    }
                },
                min: min,
                max: max,
            },
        },
        plugins: {
            legend: {
                position: "top",
            },
            title: {
                display: true,
                text: title,
                color: "#000",
                font: {
                    size: "14px",
                    weight: "bold",
                },
            },
            annotation: {
                annotations: {
                    constantLine: {
                        type: 'line',
                        yMin: set_point,
                        yMax: set_point,
                        borderColor: 'red',
                        borderWidth: 2,
                    }
                }
            }
        },
    };
}

function plotChart(chartName, data, canvasId, title, x, y="Pertinência") {
    const ctx = document.getElementById(canvasId);

    if (charts[chartName]) {
        charts[chartName].data.labels = data.labels;
        charts[chartName].data.datasets.forEach((dataset, index) => {
                dataset.data = data.memberships[index].values;
            }
        );
        charts[chartName].options.plugins.annotation.annotations.constantLine.yMax = data.set_point;
        charts[chartName].options.plugins.annotation.annotations.constantLine.yMin = data.set_point;
        charts[chartName].options.scales.y.min = 0;
        charts[chartName].options.scales.y.max = 1000;
        setInterval(() => {
            charts[chartName].update('none');
        }, 750);
        return;
    }

    charts[chartName] = new Chart(ctx, {
        type: 'line',
        data: getData(data),
        options: getOptions(title, x, y, data.min, data.max, data.set_point),
    });
}

socketio.on("result", (data) => {
    const ids = ["set_point", "current_height", "error", "fa", "p_mode"]
    ids.forEach((id) => {
        document.getElementById(id).value = data[id];
    })
    plotChart("result", data, "result_chart", "Resposta do Controle Fuzzy PD", "Tempo [s]", "Altura [m]");
})