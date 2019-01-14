let button = $('#form-rate input');
button.on('click',function(idA) {
    // alert($("#note").val())
     $.post('/rateArticle/'+idarticle,{"note":$('#note').val()})
 });
