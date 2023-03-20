$().ready(function() {
    $("#checkout_form").validate({
        rules: {
            name: {
                required:true,
                minlength:5,
            },
            phone:{
                required:true,
                minlength:5,
            },
            address: {
                required:true,
                minlength:5,
            },
            city: {
                required:true,
                minlength:3,
            },
            email: {
                required:true,
                minlength:3,
                email_check:true,
            },
            email_optional: {
                minlength:3,
            },
            payment_method:{
                required:true,
                filter:true,
            },
        },
        messages: {
            name: {
                required:"please enter your name",
            },
            phone: {
                required:"please enter your phone number",
            },
            address: {
                required:"please enter your address",
            },
            city: {
                required:"please enter your city",
            },
            email: {
                required:"please enter your email address",
            },
            payment_method:{
                required:"please select your payment method"
            },
        },
    });
    jQuery.validator.addMethod("filter", function(value, element) {
        return (value=='1')||(value=='2')||(value=='3');
    }, "invalid payment method");
    jQuery.validator.addMethod("email_check", function(value, element) {
        return value.toLowerCase().match(/^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/);
    }, "invalid email");

    $("input[name=payment_method]").click(function(){
        var value=$(this).val();
        switch (value) {
            case '1':
                $('.placeOrderBTN').html('<span>Place Order</span>');
                $('.email_container_op').html(op)
                $('.email_container').html('')
                break;
            case '2':
                $('.placeOrderBTN').html('<span>Continue</span>');
                $('.email_container_op').html('')
                $('.email_container').html(req)
                break;
            case '3':
                $('.placeOrderBTN').html('<span>Continue</span>');
                $('.email_container_op').html('')
                $('.email_container').html(req)
                break;
        }
    });
    $('.placeOrderBTN').click(function() {
        if ($("#checkout_form").valid() && ($("#checkout_form").attr('action').endsWith('order/checkout_process')) && ($("#checkout_form").attr('method')=='post' || $("#checkout_form").attr('method')=='POST')) {
            var choice=$('input[name=payment_method]:checked').val();
            switch (choice) {
                case '1':
                    $("#checkout_form").submit();
                    break;
                case '2':case '3':
                    const formDataArray = $("#checkout_form").serializeArray();
                    const formDataObject = formDataArray.reduce((acc, curr) => {
                        acc[curr.name] = curr.value;
                        return acc;
                    }, {});
                    const requestBody = JSON.stringify(formDataObject);
                    fetch('/api/order/create', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': csrfToken,
                        },
                        body: requestBody,
                    })
                    .then(response => response.json())
                    .then(result => {
                        if (result.status=='ok') {
                            window.location.href = result.url;
                        }else{
                            $.simplyToast(result.message,'danger',toast_options);
                        }
                    })
                    .catch(error => {
                        alert("error");
                        $.simplyToast(error.toString(),'danger',toast_options);
                    });
                    break;
            }
        }
        else{
            $.simplyToast('please check your info','danger',toast_options);
        }
    });
});
