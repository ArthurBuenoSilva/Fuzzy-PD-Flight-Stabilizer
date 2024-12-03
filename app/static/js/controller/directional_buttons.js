document.querySelectorAll('.direction-button').forEach(button => {
    button.addEventListener('click', function() {
        const direction = button.id;
        const setPointInput = document.getElementById('set_point');

        if (direction === 'up') {
            setPointInput.value = parseInt(setPointInput.value) + 100;
            socketio.emit("go_to", setPointInput.value);
        } else if (direction === 'down') {
            setPointInput.value = parseInt(setPointInput.value) - 100;
            socketio.emit("go_to", setPointInput.value);
        }
    });
});