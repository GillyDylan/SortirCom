function requeteAjax(onglet){

$.ajax({
		url : '/Ajax/'+onglet,
		contentType: "application/x-www-form-urlencoded;charset=utf-8",
		method : 'GET',
		data : {

		},
		success : function(resultText) {
			$('#contenu').html(resultText);
		},
		error : function(jqXHR, exception) {
			console.log('Error occured!!');
		}
});

}