$(document).ready(function(){
    $('#btnPlus').click( function(e){
        var qty=parseInt($('.qty[name="quantity"]').val());
        $('.qty[name="quantity"]').val(qty+1);
    });
    $('#btnMinus').click(  function(e){
        var qty=parseInt($('.qty[name="quantity"]').val());
        if (qty>1) {
            $('.qty[name="quantity"]').val(qty-1);
        }
    });
    $('.addingBTN').click(function() {
        var properties=[];
        $('.pcVariations input[type="radio"]:checked').each(function() {properties.push(parseInt($(this).val()))});
        var quantity=parseInt($('#quantity').val());
        var id=parseInt($('#productId').val());
        var data={'id':id,'properties':properties,'quantity':(quantity>1)?quantity:1};
        fetch('/api/cart/add', {
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
            $.simplyToast(result.message,(result.status=='ok')?'success':'danger',toast_options);
        })
        .catch(error => {
            $.simplyToast(error,'danger',toast_options);
        });
    })
})
