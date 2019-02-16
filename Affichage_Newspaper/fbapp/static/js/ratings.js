function ratingsA(nbArticles) {
  var socket = io.connect('http://' + document.domain + ':' + location.port);
  var button = [];
  for (var i = 0; i<=nbArticles; i++) {
    button.push($('#form-rate'+i.toString()+' input'));
    button[i].click(function() {
      var buttonClicked = $(this);
      socket.emit('notationA',$(this).prev('select').val(), $(this).data('urla'))
      socket.on('response', function (msg) {
        alert(buttonClicked.data('urla'))
        buttonClicked.next('span').html(msg);
        let flashMsg = $('#flash-messages');
        flashMsg.load('/templates/projet.html #flash-messages');
        alert('loaded');
      });
    });
  }
}
