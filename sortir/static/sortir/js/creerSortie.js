var lieux;


$('#AjouterSortie > div > label').addClass('col-sm-12 col-md-5 col-form-label');
$('#AjouterSortie > div > div > input').addClass('form-control');
$('#AjouterSortie > div > div > select').addClass('form-control');

$.ajax({
    method: "GET",
    dataType: 'json',
    url:'/Ajax/GetLieux/',
    success : function(response) {
        try {
            lieux = JSON.parse(response.lieux);
        }
        catch(e){
            alert(e.toString())
        }
    },
    error : function(jqXHR, exception) {
        alert('Une erreur est survenue');
    }
});


var frm = $('#AjouterSortie');
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
             alert('3');
        },
        error: function(data) {
             alert('4');
        }
    });
    return false;
});

function afficherLieux(select){
    $('#lieux').html('');
    $('#lieux').append($('<div class="form-group row text-right" id="div-lieux"></div>'));
    $('#div-lieux').append($('<label class="col-sm-12 col-md-5 col-form-label" for="selectLieu">Lieu :</label>'));
    $('#div-lieux').append($(' <div class="col-sm-12 col-md-7" id="div-select"></div>'));
    $('#div-select').append($('<select>', {id: 'id_lieu', class:'form-control', name:'lieu', required:''}));

    for(lieu of lieux){
        if(lieu.ville_id == select.children('select').val()) {
            $('#id_lieu').append($('<option value="' + lieu.id + '">' + lieu.nom + '</option>'));
        }
    }
    $('#lieux').append($('<div id="detailLieu"></div>'));
    detailLieu();
}

function detailLieu(){
     $('#detailLieu').html('');
    for(lieu of lieux){
        if(lieu.id == $('#id_lieu').val()){
            $('#detailLieu').append($('<div class="form-group row text-right" id="div-labelrue"></div>'));
            $('#div-labelrue').append($('<label class="col-sm-12 col-md-5 col-form-label">Adresse :</label>'));
            $('#div-labelrue').append($(' <div class="col-sm-12 col-md-7" id="div-detailrue"></div>'));
            $('#div-detailrue').append($('<label>'+lieu.rue+'</label>'));

            $('#detailLieu').append($('<div class="form-group row text-right" id="div-labelcp"></div>'));
            $('#div-labelcp').append($('<label class="col-sm-12 col-md-5 col-form-label">Code postal :</label>'));
            $('#div-labelcp').append($(' <div class="col-sm-12 col-md-7" id="div-detailcp"></div>'));
            $('#div-detailcp').append($('<label>'+lieu.ville__codePostal+'</label>'));

            $('#detailLieu').append($('<div class="form-group row text-right" id="div-labellatitude"></div>'));
            $('#div-labellatitude').append($('<label class="col-sm-12 col-md-5 col-form-label">Latitude :</label>'));
            $('#div-labellatitude').append($(' <div class="col-sm-12 col-md-7" id="div-detaillatitude"></div>'));
            $('#div-detaillatitude').append($('<label>'+lieu.latitude+'</label>'));

            $('#detailLieu').append($('<div class="form-group row text-right" id="div-labellongitude"></div>'));
            $('#div-labellongitude').append($('<label class="col-sm-12 col-md-5 col-form-label">Longitude :</label>'));
            $('#div-labellongitude').append($(' <div class="col-sm-12 col-md-7" id="div-detaillongitude"></div>'));
            $('#div-detaillongitude').append($('<label>'+lieu.longitude+'</label>'));




        }
    }
}