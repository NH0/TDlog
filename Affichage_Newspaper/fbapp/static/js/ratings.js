let button = $('#form-rate');
button.on('click',function() { $.post( '/rateArticle', {"note":$('#note').val(), "idA":$('#form-rate').attr('idA')} ) });
let flashMsg = $('#flash-messages')
setTimeout(function () {}, 100);
flashMsg.load('/templates/projet.html' + 'messages');
