let button = $('#form-rate input');
button.on('click',function() {
    $.get( '/rateArticle', {"note":$('#note').val(), "idA":$('#form-rate').attr('idA')} )
 });
