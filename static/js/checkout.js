$().ready(function() {
    $("#checkout_form").validate({
        rules: {
            name: "required",
            phone: "required",
            address: "required",
            city: "required",
            email: "required",
            payment_method:{
                required:true,
                filter:true,
            },
        },
        messages: {
            name: "please enter your name",
            phone: "please enter your phone number",
            address: "please enter your address",
            city: "please enter your city",
            email: "please enter your email address",
            payment_method:{
                required:"please select your payment method"
            },
        },
    });
    jQuery.validator.addMethod("filter", function(value, element) {
        return (value=='1')//||(value=='2')||(value=='3');
    }, "Something is wrong");
    $('.placeOrderBTN').click(function() {
        if ($("#checkout_form").valid() && ($("#checkout_form").attr('action')=='/checkout_process') && ($("#checkout_form").attr('method')=='post' || $("#checkout_form").attr('method')=='POST')) {
            if($('input[name=payment_method]:checked').val()=='1'){
                $("#checkout_form").submit();
            }
        }else{
            $.simplyToast('please check your info','danger',toast_options);
        }
    });
});
