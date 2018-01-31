/**
 * Created by sadjad on 01/01/18.
 */


$('document').ready(function () {
    var item = document.getElementById("id_password_visibility");
    item.addEventListener("click", function () {

        if (item.classList.contains("eye")) {
            $('#id_password').attr('type', 'password');
            item.classList.remove('eye');
            item.classList.add('hide')
        } else {
            $('#id_password').attr('type', 'text');
            item.classList.remove('hide');
            item.classList.add('eye')
        }

    });
    var code = document.getElementById("id_invited_with");
    var url = $("#code-verification").attr('value');
    code.addEventListener('input', function () {
        var text = $(this).val();
        if (text.length != 0) {
            console.log("sadad");
            $('#submit-button').attr('disabled', true);
        } else {
            $('#invitation-error').css('display', 'none')
            $('#submit-button').removeAttr('disabled');
        }

        if (text.length == 10) {
            $.ajax({
                type: 'GET',
                url: url,
                data: {
                    'code': text
                },
                success: function (response) {
                    if (response['is_valid'] == false) {
                        $('#invitation-error').css('display', 'flex')
                    } else {
                        $('#submit-button').removeAttr('disabled');
                        $('#invitation-error').css('display', 'none')
                    }
                }
            });
        }
    })
});