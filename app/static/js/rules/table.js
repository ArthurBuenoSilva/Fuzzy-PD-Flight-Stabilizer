function renderGrid(data) {
    const grid = new gridjs.Grid({
        columns: data.columns,
        data: data.data,
        pagination: false,
        search: false,
        sort: false,
        language: {
            'pagination': {
                'previous': 'Previous',
                'next': 'Next',
                'showing': ''
            }
        },
        width: '100%',
        height: '100%',
        style: {
            table: {
                'font-size': '12px',
                'text-align': 'center',
                'font-weight': 'bold',
            },
            th: {
                'background-color': 'rgb(31 41 55)',
                'color': 'rgb(250, 250, 250)'
            }
        },
    });

    grid.render(document.getElementById('table_container'));
}

const tableExampleData = {
    columns: [
        'E', 'MN', 'PN', 'ZE', 'PP', 'MP'
    ],
    data:
    [
        ['MN', 'MP', 'MP', 'P', 'M', 'M'],
        ['PN', 'MP', 'P', 'P', 'A', 'A'],
        ['ZE', 'MP', 'P', 'M', 'A', 'MA'],
        ['PP', 'P', 'P', 'M', 'A', 'MA'],
        ['MP', 'M', 'M', 'A', 'MA', 'MA']
    ],
}

renderGrid(tableExampleData);
