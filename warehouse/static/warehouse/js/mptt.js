$(document).ready(function(){

    $("#id_category").change(function () {
        $.get(location.href, { 'category': $("#id_category").val() })
            .done(function(data) {
                $('#id_item').empty();
                $('#id_item').prepend('<option values="">---------</option>');
                $.each(data, function(pk, value) {
                    $('#id_item').append('<option value="' + pk + '">' + value + '</option>');
                });
            });
    })

})