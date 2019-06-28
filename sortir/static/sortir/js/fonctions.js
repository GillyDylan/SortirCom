function changerPage(objet){
    const id = objet.attr("id");
    var adresseActuelle = window.location.pathname;
    var adresseSuivante;

    var index = adresseActuelle.lastIndexOf("/");
    if(index === -1){
        adresseSuivante = adresseActuelle + id;
    }
    else {
        adresseSuivante = adresseActuelle.substring(0, index-1) + id;
    }
    majHistorique(adresseSuivante, id);
    changerPageAjax(id);
}


function changerPageAjax(id){
    $(".nav-item").removeClass('active');
    $('#'+id).addClass('active');
    $.ajax({
        url :'/Ajax/'+ id + '/',
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        method : 'GET',
        data : {
        },
        success : function(resultText) {
            $('#contenu').html(resultText);
        },
        error : function(jqXHR, exception) {
            console.log('Une erreur est survenue');
        }
    });
}

function envoiFormulaireAjax(id){
    $.ajax({
        url :'/Ajax/'+ id + '/',
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        method : 'POST',
        data : {
        },
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        },
        success : function(resultText) {
            alert('ok');
        },
        error : function(jqXHR, exception) {
            alert('pas ok');
        }
    });
}

function majHistorique(adresseSuivante, page) {
    window.history.pushState( {page: page }, "", adresseSuivante);
}


function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}



window.addEventListener('popstate', function(event) {
    if (event.state) {
        changerPageAjax(event.state.page)
    }
}, false);

window.addEventListener('load', function() {
    var adresseActuelle = window.location.pathname;
    var index = adresseActuelle.lastIndexOf("/");
    if(adresseActuelle.length > 1){
        var id = adresseActuelle.substring(index+1);
        changerPageAjax(id);
    }
}, false);
