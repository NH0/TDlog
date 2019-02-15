alert('helloOne')
let button = $('#form-rate');
button.on('click',function() {
    $.get( '/rateArticle', {"note":$('#note').val(), "idA":$('#form-rate').attr('idA')} )
 });
