$(document).ready(function(){
    $('.modal #btnPlus').click( function(e){
        var qty=parseInt($('.modal .qty[name="quantity"]').val());
        $('.modal .qty[name="quantity"]').val(qty+1);
    });
    $('.modal #btnMinus').click(  function(e){
        var qty=parseInt($('.modal .qty[name="quantity"]').val());
        if (qty>1) {
            $('.modal .qty[name="quantity"]').val(qty-1);
        }
    });
    $('.modal .addingBTN').click(function() {
        var properties=[];
        $('.modal .pcVariations input[type="radio"]:checked').each(function() {properties.push(parseInt($(this).val()))});
        var quantity=parseInt($('.modal #quantity').val());
        var id=parseInt($('.modal #productId').val());
        var data={'id':id,'properties':properties,'quantity':(quantity>1)?quantity:1};
        fetch(cartCreateApi, {
            method: 'POST',
            body: JSON.stringify(data),
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            }
        })
        .then(response => response.json())
        .then(result => {
            cart_length=result.data
            $('.anCart a span').text(cart_length);
            $.simplyToast((result.status=='ok')?productMessage:productMessageError,(result.status=='ok')?'success':'danger',toast_options);
        })
        .catch(error => {
            $.simplyToast(error,'danger',toast_options);
        });
    })
})
