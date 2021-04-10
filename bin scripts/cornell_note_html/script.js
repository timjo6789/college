$(document).ready(function () {
    $('li').click(function (event) {
        event.stopPropagation();
        $(event.target).siblings('ul').slideToggle();
    });
    $('li img').click(function (event) {
        $(event.target).parent().siblings('ul').slideToggle();
    });
    // setTimeout(function(){ document.location.reload(true) }, 5000);
});
