document.addEventListener("DOMContentLoaded", () => {
    const rth_button = document.getElementById("rth");

    rth_button.addEventListener("click", () => {
        socketio.emit("rth")
    });

    const go_to = document.getElementById('go_to');
    go_to.addEventListener("click", function() {
        const set_point = document.getElementById('set_point').value;
        socketio.emit("go_to", set_point);
    })
})