$(document).ready(function () {
    $('.list-group-item .custom-control-label').on('click', function () {
        var checkBox = $(this).prev('input');

        if ($(checkBox).attr('checked'))
            $(checkBox).removeAttr('checked');
        else
            $(checkBox).attr('checked', 'checked');
        return false;
    });
    $('.list-group-link').on('click', function () {
        window.location.href = $(this).attr('href');
        return false;
    });
});
