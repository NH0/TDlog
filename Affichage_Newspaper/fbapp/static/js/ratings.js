let button = $('#form-rate input');
button.on('click',function() {
    $.post( '/rateArticle', {"note":$('#note').val(), "idA":$('#form-rate').attr('idA')} )
 });
