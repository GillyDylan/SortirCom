$('#AnnulerSortie > div > label').addClass('col-sm-12 col-md-5 col-form-label');
$('#AnnulerSortie > div > div > input').addClass('form-control');
$('#AnnulerSortie > div > div > select').addClass('form-control');



var frm = $('#AnnulerSortie');
frm.submit(function () {
    $.ajax({
        method: "POST",
        url:'/Ajax/AnnulerSortie/',
        data: frm.serialize(),
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("HTTP_X_CSRFTOKEN", jQuery("[name=csrfmiddlewaretoken]").val());
            }
        },
        success : function(resultText) {
            $('#contenu').html(resultText);
        },
        error: function(data) {
        }
    });
    return false;
});