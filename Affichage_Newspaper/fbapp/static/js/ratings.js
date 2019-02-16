function ratingsA(nbArticles) {
  var i;
  var button = [];
  for (i = 0; i<nbArticles; i++) {
    button.push($('#form-rate'+i.toString()));
    button[i].on('click',function() {
      $.post( '/rateArticle', {"note":$('#note').val(), "urlA":$('#form-rate'+i.toString()).attr('urlA')} ) });
  }
}
