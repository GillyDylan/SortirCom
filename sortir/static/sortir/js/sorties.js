var sorties;
var participants;
var userId;

$.ajax({
    method: "GET",
    dataType: 'json',
    url:'/Ajax/GetSorties/',
    success : function(response) {
        try {
            sorties = JSON.parse(response.sorties);
            participants = JSON.parse(response.participants);
            userId = response.userId;
            afficherSorties();
        }
        catch(e){
            alert(e.toString())
        }
    },
    error : function(jqXHR, exception) {
        alert('Une erreur est survenue');
    }
});

function afficherSorties(){

    $('#sorties').html('');
    for(let sortie of sorties) {
        var nbParticipants = 0;
        var inscrit = '';

        for (participant of participants) {
            if (sortie.id === participant.id) {
                if (userId === participant.participants__site_id) {
                    inscrit = 'X'
                }
                nbParticipants++;
            }
        }
        if (($('#recherche').val() === '' || sortie.nom.toLowerCase().indexOf($('#recherche').val().toLowerCase()) >= 0) &&
            (sortie.organisateur__site_id == $("#sites").val()) && ((sortie.organisateur_id === userId && $("#orga").is(':checked')) ||
                                                                   (inscrit === 'X' && $("#inscr").is(':checked')) ||
                                                                   (inscrit === '' && $("#notinscr").is(':checked'))))
        {
            $('#sorties').append($('<tr>', {id: 'sortie' + sortie.id}));
            $('#sortie' + sortie.id).append($('<td>' + sortie.nom + '</td>'))
                .append($('<td>' + sortie.dateHeureDebut + '</td>'))
                .append($('<td>' + sortie.dateLimiteInscription + '</td>'))
                .append($('<td>' + nbParticipants + '/' + sortie.nbinscriptionMax + '</td>'))
                .append($('<td>' + sortie.etat__libelle + '</td>'))
                .append($('<td>' + inscrit + '</td>'))
                .append($('<td>' + sortie.organisateur__nom + '</td>'));
        }
    }
}
