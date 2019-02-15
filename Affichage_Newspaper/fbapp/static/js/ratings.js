alert('helloOne')
let button = $('#form-rate')
button.on('click',function() { $.post( '/rateArticle', {"note":$('#note').val(), "idA":$('#form-rate').attr('idA')} ) });
