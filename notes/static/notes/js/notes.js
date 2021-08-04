/*
const tableBody = document.getElementById('table-body-box')

$.ajax({
    type: 'GET',
    url: '/notes/data-json/',
    success: function (response){
        const data = JSON.parse(response.data)
        data.forEach(el=>{
            //console.log(el.fields.date)
            //console.log(el.fields.date.slice(0, 10))
            tableBody.innerHTML += `
            <tr><td>${el.fields.title}</td><td>${el.fields.date.slice(0, 10)}</td> </tr>
            `
        })

    },
    error: function (error){
        console.log(error)
    }
});


$("#createNoteModal").on("submit", ".js-note-create-form", function (){
    const form = $(this);
    $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        success: function (data){
            if (data.form_is_valid){
                $("#createNoteModal").modal("hide");
                window.location.href = ""
                window.location.reload()
            }
            else{
                $("#createNoteModal .modal-content").html(data.html_form);
            }
        }
    });
    return false;
});

$(function() {$(".js-create-note").click(function () {
    var btn = $(this)
    $.ajax({
        type: 'GET',
        url: btn.attr("data-url"),
        beforeSend: function (){
            $("#createNoteModal").modal("show");
        },
        success: function (data){
            $("#createNoteModal .modal-content").html(data.html_form);
        }
        });
    });
});
*/

$(function (){
    let loadForm = function () {
        let btn = $(this);
        $.ajax({
            type: 'GET',
            url: btn.attr("data-url"),
            beforeSend: function (){
                $("#createNoteModal").modal("show");
            },
            success: function (data){
                $("#createNoteModal .modal-content").html(data.html_form);
        }
        });
    };

    let saveForm = function () {
        let form = $(this);
        $.ajax({
            url: form.attr("action"),
            data: form.serialize(),
            type: form.attr("method"),
            success: function (data){
                if (data.form_is_valid){
                    $("#createNoteModal").modal("hide");
                    window.location.href = "";
                    window.location.reload();
                }
                else{
                    $("#createNoteModal .modal-content").html(data.html_form);
                }
            }
        });
        return false;
    };

    /* Binding */

    // Create note
    $(".js-create-note").click(loadForm);
    $("#createNoteModal").on("submit", ".js-note-create-form", saveForm);

    // Update note
    $('#note-table').on("click", ".js-update-note", loadForm);
    $("#createNoteModal").on("submit", ".js-note-update-form", saveForm);


    // Delete note
    $('#note-table').on("click", ".js-delete-note", loadForm);
    $("#createNoteModal").on("submit", ".js-note-delete-form", saveForm);
})