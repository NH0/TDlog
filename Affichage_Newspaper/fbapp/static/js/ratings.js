alert($)
$(document).ready(function() {
  alert('hello')
  let button = $('#form-rate input');
  button.on('click',function() {
      alert("test")
      $.get( '/rateArticle', {"note":$('#note').val(), "idA":$('#form-rate').attr('idA')} )
   });
});
