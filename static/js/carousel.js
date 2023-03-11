var sync1 = $("#sync1");
var sync2 = $("#sync2");

sync1.owlCarousel({
    items:1,
    loop:false,
    center:true,
    margin:10,
    URLhashListener:true,
    autoplayHoverPause:true,
    startPosition: 'URLHash'
});
sync2.owlCarousel({
    items: 4,
    loop:false,
    pagination: false,
});
