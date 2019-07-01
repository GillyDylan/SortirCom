$('#CreerSortie > div > label').addClass('col-sm-12 col-md-5 col-form-label');
$('#CreerSortie > div > div > input').addClass('form-control');
$('#CreerSortie > div > div > select').addClass('form-control');



var frm = $('#CreerSortie');
frm.submit(function () {
    $.ajax({
        method: "POST",
        url:'/Ajax/CreerSortie/',
        data: frm.serialize(),
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("HTTP_X_CSRFTOKEN", jQuery("[name=csrfmiddlewaretoken]").val());
            }
        },
        success: function (data) {

        },
        error: function(data) {
        }
    });
    return false;
});