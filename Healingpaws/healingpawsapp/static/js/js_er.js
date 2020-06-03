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
    }
}
function emails(obj){
    var myreg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
    if(obj.length == 0){
        alert('Input information cannot be empty.');
        return false
    }else if(!myreg.test(obj)){
        alert('Incorrect email format.');
        document.getElementById("useremail").value = "";
        return false
    }
}
function pwdTest(pwd){
    var reg = /^[A-Za-z0-9]{4,40}$/;
    if(!pwdTest(pwd)){
        alert('Password must be a combination of 4-40 numbers and letters.');
        document.getElementById("pwd").value = "";
        return false
    }
}
function pwdTest2(pwd2){
    varPwd = $("#pwd").val();
    if(pwd2 != varPwd){
        alert('Password inconsistency.');
        document.getElementById("pwd2").value = "";
        return false
    }
}
function emailb(obj){
    var myreg = /^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/;
    var bossemail = 'boss@163.com';
    if (myreg != bossemail){
        alert('Failure to certify information.');
        document.getElementById("bossemail").value = "";
        return false
    }
}
