$('#ModifierSortie > div > label').addClass('col-sm-12 col-md-5 col-form-label');
$('#ModifierSortie > div > div > input').addClass('form-control');
$('#ModifierSortie > div > div > select').addClass('form-control');



var frm = $('#ModifierSortie');
frm.submit(function () {
    $.ajax({
        method: "POST",
        url:'/Ajax/ModifierSortie/',
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