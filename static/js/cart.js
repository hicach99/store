$('.cartIcon').hover(function(){
    fetch('/api/cart', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        }
    })
    .then(response => response.json())
    .then(result => {
        if (result.status=='ok') {
            $('.anCart').html(result.html);
        }
        else{
            $.simplyToast(result.message,'danger',toast_options);
        }
    })
    .catch(error => {
        $.simplyToast(error,'danger',toast_options);
    });
});
$('.cartRemoveProducts').click(function() {
    var id=parseInt($(this).attr('data-prod'));
    fetch('/api/cart/remove/'+id, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        }
    })
    .then(response => response.json())
    .then(result => {
        if (result.status=='ok') {
            $('.anCart').html(result.html);
        }
        else{
            $.simplyToast(result.message,'danger',toast_options);
        }
    })
    .catch(error => {
        $.simplyToast(error,'danger',toast_options);
    });
})