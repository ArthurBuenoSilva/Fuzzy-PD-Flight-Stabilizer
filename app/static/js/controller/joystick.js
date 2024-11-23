const joystick = document.getElementById('joystick');
let stateValue = '';

joystick.classList.add('up');

joystick.addEventListener('click', function() {
    if (joystick.classList.contains('up')) {
        joystick.classList.remove('up');
        joystick.classList.add('down');
        stateValue = 'down';
    } else if (joystick.classList.contains('down')) {
        joystick.classList.remove('down');
        joystick.classList.add('up');
        stateValue = 'up';
    }
});