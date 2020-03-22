var cot=0;//设置一个计数器，初始值为0；作用是用来监听点击切换的时候哪一个图片应该隐藏或者显示
                function nex(){
                 if(cot<=2){
                  $('.imgs img').eq(cot).animate({'margin-left':'-305px'},500);
                  cot++;
                 }
                }
                function pre(){
                 if(cot>0){
                  cot--;
                  $('.imgs img').eq(cot).animate({'margin-left':'0'},500);
                 }
                }



function menuFix() {
        var obj = document.getElementById("index").getElementsByTagName("li");
        for (var i=0; i<obj.length; i++) {
            obj[i].onmouseover=function() {
                this.className+=(this.className.length>0? " ": "") + "sfhover";
            }
            obj[i].onMouseDown=function() {
                this.className+=(this.className.length>0? " ": "") + "sfhover";
            }
            obj[i].onMouseUp=function() {
                this.className+=(this.className.length>0? " ": "") + "sfhover";
            }
            obj[i].onmouseout=function() {
                this.className=this.className.replace(new RegExp("( ?|^)sfhover\\b"),
            "");
            }
        }
}
        window.onload=menuFix;




