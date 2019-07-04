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
            $('#sorties').append($('<tr id="Sortie_'+ sortie.id +'"></tr>'));
            $('#Sortie_' + sortie.id).append($('<td>' + sortie.nom + '</td>'))
                .append($('<td>' + sortie.dateHeureDebut + '</td>'))
                .append($('<td>' + sortie.dateLimiteInscription + '</td>'))
                .append($('<td>' + nbParticipants + '/' + sortie.nbinscriptionMax + '</td>'))
                .append($('<td>' + sortie.etat__libelle + '</td>'))
                .append($('<td>' + inscrit + '</td>'));
            if(userId == sortie.organisateur_id || inscrit === ''){
                $('#Sortie_' + sortie.id).append($('<td>' + sortie.organisateur__prenom + ' ' + sortie.organisateur__nom.substring(0,1) +'.</td>'));
            }else{
                $('#Sortie_' + sortie.id).append($('<td><div id="AfficherProfil_'+ sortie.organisateur_id +'" onclick="changerPage($(this))"><label>' + sortie.organisateur__prenom + ' ' + sortie.organisateur__nom.substring(0,1) +'.</label></div></td>'));
            }
            if(userId == sortie.organisateur_id){
                $('#Sortie_' + sortie.id).append('<td id="tdSortie_' + sortie.id + '">' +
                    '<div id="ModifierSortie_' + sortie.id + '" onclick="changerPage($(this))"><label>Modifier</label></div></td>');

            }else {
                $('#Sortie_' + sortie.id).append('<td id="tdSortie_' + sortie.id + '">' +
                    '<div id="AfficherSortie_' + sortie.id + '" onclick="changerPage($(this))"><label>Afficher</label></div></td>');
            }
            if(inscrit === 'X'){
                $('#tdSortie_' + sortie.id).append(
                '<div id="Inscription_'+ sortie.id +'" onclick="changerPage($(this))">' +
                '<label>Se désister</label>' +
                '</div>')
            }else if(userId != sortie.organisateur_id){
                 $('#tdSortie_' + sortie.id).append(
                '<div id="Inscription_'+ sortie.id +'" onclick="changerPage($(this))">' +
                '<label>S\'inscrire</label>' +
                '</div>')
            }
        }
    }
}
