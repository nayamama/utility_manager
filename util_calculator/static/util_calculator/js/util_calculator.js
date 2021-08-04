$(function(){

    let loadForm = function () {
        let btn = $(this);
        $.ajax({
            type: 'GET',
            url: btn.attr('data-url'),
            success: function (data){
                $('#pgModal').modal("show");
                $('#pgModal .modal-content').html(data);
            },
            error: function (xhr) {
                if (xhr.status === 403) {
                    alert(xhr.responseJSON.msg);
                }
            },
        });
    };

    // create payment
    $(".js-create-payment").on('click', loadForm);

    // create utility and bill
    $(".js-btn").on('click', loadForm);
/*
    let submitForm = function (e){
        e.preventDefault();
        let form = $(this);
        console.log("before success")

        $.ajax({
            type: form.attr('method'),
            headers: {"X-CSRFToken": '{{ csrf_token }}'},
            url: form.attr('action'),
            data: form.serialize(),

            beforeSend: function (){
                $('#pgModal').modal("show");
            },

            success: function (response){
                console.log('inside');
                console.log(response)
                $('#pgModal .modal-content').html(response.html_form);
            },
            error: function () {
                alert('problem');
            }
        })
    }
    $('#payment-date-form').on('submit', submitForm)

    $('.js-payment-date').on('click', function (e){
        e.preventDefault();
        $.ajax({
            type: 'POST',
            headers: {"X-CSRFToken": '{{ csrf_token }}'},
            url: "{% url 'util_calculator:payment-date' %}",
            data: $('#payment-date-form').serialize(),
             beforeSend: function (){
                $('#pgModal').modal("show");
            },

            success: function (response){
                console.log('inside');
                console.log(response)
                $('#pgModal .modal-content').html(response.html_form);
            },
            error: function () {
                alert('problem');
            }
        })


    });

*/

})