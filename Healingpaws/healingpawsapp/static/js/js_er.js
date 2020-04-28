function getCode(){
                varRand = parseInt(Math.random()*9000+1000);
                $("#spanCodeId").html(varRand);
            }

            var varRand = 0;

            var varPwd;
            $(function(){
                getCode();
            })
            function unameTest(){

                var varUname = $("#username").val();

                var varReg = /^[\u4e00-\u9fa5]{1,8}$/;
                if(varUname.length == 0){

                    $("#spanUnameId").html("<span style='color: red;font-size: 18px;margin-left: 530px'>× username cannot be empty</span>");
                    return false;
                }else{
                    $("#spanUnameId").html("<span style='color: green;font-size: 18px;margin-left: 530px'>√</span>");
                    return true&&unameTest();
                }

            }
            function unameTest2(){

                var varUname = $("#realname").val();

                var varReg = /^[\u4e00-\u9fa5]{1,16}$/;
                if(varUname.length == 0){

                    $("#spanUnameId2").html("<span style='color: red;font-size: 18px;margin-left: 530px;'>× real name cannot be empty</span>");
                    return false;
                }else {
                    $("#spanUnameId2").html("<span style='color: green;font-size: 18px;margin-left: 530px'>√</span>");
                    return true&&unameTest2();
                }

            }
            function unameTel(){

                var varUname = $("#telphone").val();


                if(varUname.length == 0){

                    $("#spanTel").html("<span style='color: red;font-size: 18px;margin-left: 530px;'>× TEL cannot be empty</span>");
                    return false;
                }else {
                    $("#spanTel").html("<span style='color: green;font-size: 18px;margin-left: 530px;'>√</span>");
                    return true;
                }

            }


            function pwdTest(){

                varPwd = $("#pwdId").val();

                var varReg = /^[A-Za-z0-9]{4,40}$/;
                if(varPwd.length == 0){

                    $("#spanPwdId").html("<span style='color: red;font-size: 18px;margin-left: 530px'>× password cannot be empty</span>");
                    return false;
                }else if(varReg.test(varPwd)){
                    $("#spanPwdId").html("<span style='color: green;font-size: 18px;margin-left: 530px'>√</span>");
                    return true&&pwdTest2();
                }else{
                    $("#spanPwdId").html("<span style='color: #1159dd;font-size: 18px;margin-left: 530px'> Password must be a combination of 4-40 numbers and letters</span>");
                    return false;
                }
            }

            function pwdTest2(){

                var varPwd2 = $("#pwdId2").val();
                if(varPwd2.length == 0){

                    $("#spanPwdId2").html("<span style='color: red;font-size: 18px;margin-left: 530px'>× password cannot be empty</span>");
                    return false;
                }else if(varPwd2 === varPwd){
                    $("#spanPwdId2").html("<span style='color: green;font-size: 18px;margin-left: 530px'>√</span>");
                    return true;
                }else{
                    $("#spanPwdId2").html("<span style='color: red;font-size: 18px;margin-left: 530px'>×  Password input error</span>");
                    return false;
                }
            }
            function emails() {
                varSemail = $("#useremail").val();

                var varRegE =  /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
                if(varSemail.length == 0){

                    $("#spanEmailSId").html("<span style='color: red;font-size: 18px;margin-left: 530px'>× email cannot be empty</span>");
                    return false;
                }else if(varRegE.test(varSemail)){
                    $("#spanEmailSId").html("<span style='color: green;font-size: 18px;margin-left: 530px'>√</span>");
                }else{
                    $("#spanEmailSId").html("<span style='color: #205ddd;font-size: 18px;margin-left: 530px'> format error</span>");
                    return false;
                }
            }
            function emailb() {
                varBemail = $("#bossemail").val();

                var varRegB = /^([A-Za-z0-9_\-\.])+\@([A-Za-z0-9_\-\.])+\.([A-Za-z]{2,4})$/;
                if(varBemail.length == 0){

                    $("#spanEmailBId").html("<span style='color: red;font-size: 18px;margin-left: 530px'>× email cannot be empty</span>");
                    return false;
                }else if(varRegB.test(varBemail)){
                    $("#spanEmailBId").html("<span style='color: green;font-size: 18px;margin-left: 530px'>√</span>");
                }else{
                    $("#spanEmailBId").html("<span style='color: #3151dd;font-size: 18px;margin-left: 530px'> format error</span>");
                    return false;
                }
            }
            $(document).ready(function(){
              $("form").submit(function(){
                alert("sumbit");
              });
            });