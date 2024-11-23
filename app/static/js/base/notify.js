function notify(message, category) {
    const categoryColors = {
        'success': '#2ecc71',
        'warning': '#e74c3c',
        'error': '#ffc107',
    };

    const backgroundColor = categoryColors[category] || categoryColors['success'];

    Toastify({
        text: message,
        duration: 3000,
        close: true,
        gravity: "top",
        position: "right",
        style: {
            background: backgroundColor,
        },
        stopOnFocus: true,
        escapeMarkup: false
    }).showToast();
}

socketio.on("notify", (data) => {
    notify(data.message, data.category);
})