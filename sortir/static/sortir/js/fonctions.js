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
    requeteAjax(id);
}

window.addEventListener('popstate', function(event) {
    if (event.state) {
        requeteAjax(event.state.page)
    }
}, false);

window.addEventListener('load', function() {
    var adresseActuelle = window.location.pathname;
    var index = adresseActuelle.lastIndexOf("/");
    if(adresseActuelle.length > 1){
        var id = adresseActuelle.substring(index+1);

        requeteAjax(id);
    }
}, false);


function requeteAjax(id){
     $(".nav-item").removeClass('active');
     $('#'+id).addClass('active');
    $.ajax({
        url : '/Ajax/'+ id,
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

function majHistorique(adresseSuivante, page) {
    window.history.pushState( {page: page }, "", adresseSuivante);
}