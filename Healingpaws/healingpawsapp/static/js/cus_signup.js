$(function () {
    $("#submit").click(function () {
        event.preventDefault();
        var username = $("input[name='username']");
        var password1 = $("input[name='password1']").val();
        var password2 = $("input[name='password2']").val();
        var phonenumber = $("input[name='phonenumber']").val();
        var email = $("input[name='email']").val();

        $.ajax({
        type: "POST",
        url: "/sign up/",
        data: {
            'username': username,
            'password1': password1,
            'password2': password2,
            'phonenumber': phonenumber,
            'email': email
        },
        success : function(data){
            if (text == "success"){
                formSuccess();
            } else {
                formError();
                submitMSG(false,text);
            }
        }
    });
    });
});