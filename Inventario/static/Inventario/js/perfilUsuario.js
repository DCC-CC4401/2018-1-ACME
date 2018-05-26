$(document).ready(function () {
    window.setTimeout(function () {
        showAlert();
    }, 100);
});

function showAlert() {
    $("#myAlert").addClass("show");
}