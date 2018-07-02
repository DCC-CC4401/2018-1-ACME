$(document).ready(function () {
    $(function () {
        var hash = window.location.hash;
        hash && $('ul.nav a[href="' + hash + '"]').tab('show');

        $('.nav-tabs a, .nav-pills a').click(function (e) {
            $(this).tab('show');
            window.location.hash = this.hash;
        });
    });

    var tabs$ = $(".nav-tabs a, .nav-pills a");

    $(window).on("hashchange", function () {
        var hash = window.location.hash, // get current hash
            menu_item$ = tabs$.filter('[href="' + hash + '"]'); // get the menu element

        menu_item$.tab("show"); // call bootstrap to show the tab
    }).trigger("hashchange");

    $('html').show();

    window.setTimeout(function () {
        showAlert();
    }, 100);
});

function showAlert() {
    $("#myAlert").addClass("show");
}

