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
    var anciennePage = $('.active');
    $(".nav-item").removeClass('active');
    $('#'+id).addClass('active');
    $.ajax({
        url :'/Ajax/'+ id + '/',
        contentType: "application/x-www-form-urlencoded;charset=utf-8",
        method : 'GET',
        success : function(resultText) {
            $('#contenu').html(resultText);
            if(id === 'Deconnexion'){
                changerPage($('#'+anciennePage.get(0).id))
            }
        },
        error : function(jqXHR, exception) {
            alert('Une erreur est survenue');
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
    }else{
        changerPageAjax("Accueil");
    }
}, false);
