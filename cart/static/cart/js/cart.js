// Listen for change events and update quantities

$(".form-edit-quantity").change(function (e) {
    e.preventDefault();
    $("#form-edit-cart").submit();
})

$(".form-delete-item").click(function (e) {
    e.preventDefault();
    let csrfToken = $("input[name='csrfmiddlewaretoken']").val();
    let plantId = $(this).attr("id").split("delete-")[1];
    let url = `/cart/delete/${plantId}/`;
    let data = {
        'csrfmiddlewaretoken': csrfToken,
    };

    $.post(url, data).done(function() {
        location.reload();
    });
})