let charts = {
    error: null,
    deltaError: null,
    speed: null,
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

function getOptions(title, x, y, min, max) {
    return {
        responsive: true,
        maintainAspectRatio: false,
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
        },
    };
}

function plotChart(chartName, data, canvasId, title, x, y="Pertinência", min=0, max=1) {
    const ctx = document.getElementById(canvasId);

    if (charts[chartName]) {
        charts[chartName].data.labels = data.labels;
        charts[chartName].data.datasets.forEach((dataset, index) => {
            dataset.data = data.memberships[index].values;
        });
        charts[chartName].update();
        return;
    }

    if (data.min || data.max) {
        min = data.min;
        max = data.max;
    }

    charts[chartName] = new Chart(ctx, {
        type: 'line',
        data: getData(data),
        options: getOptions(title, x, y, min, max),
    });
}

socketio.on("plot_error_chart", (data) => {
    plotChart("error", data, "error_chart", "Classificação para variável Erro", "Erro");
});

socketio.on("plot_delta_error_chart", (data) => {
    plotChart("deltaError", data, "delta_error_chart", "Classificação para variável Delta Erro", "Delta Erro");
});

socketio.on("plot_speed_chart", (data) => {
    plotChart("speed", exampleData, "speed_chart", "Classificação para variável Altura", "Altura [m]");
});

socketio.on("plot_result_chart", (data) => {
    plotChart("result", exampleData, "result_chart", "Resposta do Controle Fuzzy PD", "Tempo [s]", "Altura [m]");plotChart("result", exampleData, "result_chart", "Resposta do Controle Fuzzy PD", "Tempo [s]", "Velocidade [Km/h]");
})

const exampleData = {
    labels: [0, 10, 20, 30, 40, 50],
    memberships: [
        {
            name: "Low",
            values: [1, 0.5, 0, 0, 0, 0],
            color: "red",
        },
        {
            name: "Medium",
            values: [0, 0.5, 1, 0.5, 0, 0],
            color: "blue",
        },
        {
            name: "High",
            values: [0, 0, 0, 0.5, 1, 0.5],
            color: "green",
        },
    ],
};

plotChart("error", exampleData, "error_chart", "Classificação para variável Erro", "Erro");
plotChart("deltaError", exampleData, "delta_error_chart", "Classificação para variável Delta Erro", "Delta Erro");
plotChart("speed", exampleData, "speed_chart", "Classificação para variável Altura", "Altura [m]");

const exampleResultData = {
    labels: [0, 10, 20, 30, 40, 50],
    memberships: [
        {
            name: "Altura/Tempo",
            values: [0, 15, 22, 31, 33, 33],
            color: "red",
        },
        {
            name: "Set Point",
            values: [30, 30, 30, 30, 30, 30],
            color: "green",
        }
    ],
    min: 0,
    max: 50
};

plotChart("result", exampleResultData, "result_chart", "Resposta do Controle Fuzzy PD", "Tempo [s]", "Altura [m]");