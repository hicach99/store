$('.cartIcon').hover(function(){
    fetch(cartApi, {
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
            $.simplyToast(warningError,'danger',toast_options);
        }
    })
    .catch(error => {
        $.simplyToast(error,'danger',toast_options);
    });
    $(this).unbind('mouseenter mouseleave');
});
$('.cartRemoveProducts').click(function() {
    var id=parseInt($(this).attr('data-prod'));
    fetch(cartRemoveApi+id, {
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
            $.simplyToast(warningError,'danger',toast_options);
        }
    })
    .catch(error => {
        $.simplyToast(error,'danger',toast_options);
    });
})