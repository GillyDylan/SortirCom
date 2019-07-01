$('#Connexion > div > label').addClass('col-sm-12 col-md-5 col-form-label');
$('#Connexion > div > div > input').addClass('form-control');


var frm = $('#Connexion');
frm.submit(function () {
    $.ajax({
        method: "POST",
        url:'/Ajax/Connexion/',
        data: frm.serialize(),
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("HTTP_X_CSRFTOKEN", jQuery("[name=csrfmiddlewaretoken]").val());
            }
        },
        success : function(resultText) {
            verifierUtilisateurActuel();
            $('#contenu').html(resultText);
        },
        error: function(data) {
        }
    });
    return false;
});