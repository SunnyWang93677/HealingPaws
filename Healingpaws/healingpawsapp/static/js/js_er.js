function nameTest(obj){
    var myreg = /^[A-Za-z]{1,8}$/;
    if(myreg.test(obj))
    {
        alert('Your username is ' + obj + '.');
        return true
    }else if(obj.length == 0){
        alert('Username cannot be empty.');
        return false
    }else{
        alert('Only enter English characters between one and eight characters.');
        document.getElementById("username").value = "";
        return false
    }
}
function nameTest2(obj){
    var myreg = /^[A-Za-z]{3,10}$/;
    if(myreg.test(obj))
    {
        alert('Your realname is ' + obj + '.');
        return true
    }else if(obj.length == 0){
        alert('Real name cannot be empty.');
        return false
    }else{
        alert('Only enter English characters between three and ten characters.');
         document.getElementById("realname").value = "";
        return false
    }
}
function Tel(mobile) {
    if(mobile.length == 0) {
        alert('The phone number cannot be empty.');
        document.getElementById("telphone").value = "";
        return false
    }
    var myreg = /^(((13[0-9]{1})|(15[0-9]{1})|(18[0-9]{1}))+\d{8})$/;
    if(!myreg.test(mobile))
    {
        alert('Please enter a valid cell phone number!');
        document.getElementById("telphone").value = "";
        return false
    }else{
        alert('Your Telphone is' + mobile+'.');
        return true
    }

}
function emails(obj){
    var myreg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
    if(myreg.test(obj))
    {
        alert('Your email is ' + obj + '.');
        return true
    }else if(obj.length == 0){
        alert('Input information cannot be empty.');
        return false
    }
    else{
        alert('Incorrect email format.');
        document.getElementById("useremail").value = "";
        return false
    }
}
function pwdTest(pwd){
    var reg = /^[A-Za-z0-9]{4,40}$/;
    if(pwd.length == 0){
        alert('Password cannot be empty.');
        return false
    }else if(reg.test(pwd)){
        alert('Password set successfully.');
        return true
    }else {
        alert('Password must be a combination of 4-40 numbers and letters.');
        document.getElementById("pwd").value = "";
        return false
    }
}
function pwdTest2(pwd2){
    varPwd = $("#pwd").val();
    if(pwd2.length == 0){
        alert('Password cannot be empty.');
        return false
    }else if(pwd2 == varPwd){
        alert('Password consistency.');
        return true
    }else if(pwd2 != varPwd){
        alert('Password inconsistency.');
        document.getElementById("pwd2").value = "";
        return false
    }
    else{
        alert('Password must be a combination of 4-40 numbers and letters.');
        document.getElementById("pwd2").value = "";
        return false
    }
}
function emailb(obj){
    var myreg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
    var bossemail = 'boss@163.com';
    if(obj == bossemail)
    {
        alert('Correct information.');
        return true
    }else if(obj.length == 0){
        alert('Input information cannot be empty.');
        return false
    }
    else{
        alert('Failure to certify information.');
        document.getElementById("bossemail").value = "";
        return false
    }
}
function pets(pet) {
    if(pet.length == 0){
        alert('Input information cannot be empty.');
        return false
    }else{
        alert('Your enter is '+pet +'.');
        return true
    }
}
