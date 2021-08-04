$(function () {

    let loadForm = function () {
        let btn = $(this);
        $.ajax({
            type: "GET",
            url: btn.attr('data-url'),
            success: function (data) {
                $('#pgModal').modal("show");
                $('#pgModal .modal-content').html(data);
            },
            error: function (xhr) {
                if (xhr.status === 403) {
                    console.log('invalid');
                    alert(xhr.responseJSON.msg);
                }
            },
        });
    }

    // load create receipt form
    $(".js-btn").on('click', loadForm);

    // delete receipt
    $('#receipt-list').on('click', '.js-delete-receipt', loadForm);

    // show receipt image
    $('.pgImg').on('click', loadForm);
})

