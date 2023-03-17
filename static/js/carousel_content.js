
$( document ).ready(function() {
    var sync1 = $("#sync1");
    var sync2 = $("#sync2");
    sync1.owlCarousel({
        items: 1,
        URLhashListener: true,
        startPosition: 'URLHash'
    });
    // Initialize second carousel
    sync2.owlCarousel({
        items: 3,
        URLhashListener: true,
        startPosition: 'URLHash'
    });
    $('.slide-link').click(function(e){
        e.preventDefault();
        var hash = $(this).attr('href');
        $('#carousel1').trigger('to.owl.carousel', [$(hash).index(), 500, true]);
        $('#carousel2').trigger('to.owl.carousel', [$(hash).index(), 500, true]);
    });
});