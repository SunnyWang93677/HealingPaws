function addloadEvent(func){
 var oldonload=window.onload;
 if(typeof window.onload !="function"){
  window.onload=func;
 }
 else{
  window.onload=function(){
  if(oldonload){
   oldonload();
  }
  func();
  }
 }
 }
 addloadEvent(b);
 function b(){
 var pn=document.getElementById("pn");
 var lists=pn.children;

 function remove(node){
 node.parentNode.removeChild(node);
 }

 function praisebox(box,el){

 var praise=box.getElementsByClassName("people")[0];

 var total=parseInt(praise.getAttribute("total"));

 var txt=el.innerHTML;

 var newtotal;

 if(txt=="heart"){

 newtotal=total+1;

 praise.innerHTML=newtotal==1 ? "I like it" : "I and" + total +"like it";
 el.innerHTML="cancel heart";
 }
 else{

 newtotal=total-1;
 praise.innerHTML=newtotal==0 ? "" : newtotal +"like it";
 el.innerHTML="heart";
 }

 praise.setAttribute("total",newtotal);

 praise.style.display=(newtotal==0) ? "none" : "block";
 }

 function reply(box){

 var textarea=box.getElementsByTagName("textarea")[0];

 var comment=box.getElementsByClassName("comment-list")[0];

 var div=document.createElement("div");

 div.className="comment";

 div.setAttribute("user","self");

 var html='<div class="comment-left">'+'<img src="images/T2.jpg" alt=""/>'+'</div>'+
  '<div class="comment-right">'+
  '<div class="comment-text"><span>Me:</span>'+textarea.value+'</div>'+
  '<div class="comment-date">'+
  getTime()+
  '<a class="comment-zan" href="javascript:;" total="0" my="0">heart</a>'+
  '<a class="comment-dele" href="javascript:;">delete</a>'+
  '</div>'+
  '</div>';

 div.innerHTML=html;

 comment.appendChild(div);
 //评论后初始化textarea输入框
 textarea.value="comment...";
 textarea.parentNode.className="hf";
 }

 function getTime(){
 var t=new Date();
 var y=t.getFullYear();
 var m=t.getMonth()+1;
 var d=t.getDate();
 var h=t.getHours();
 var mi=t.getMinutes();
 m=m<10?"0"+m:m;
 d=d<10?"0"+d:d;
 h=h<10?"0"+h:h;
 mi=mi<10?"0"+mi:mi;
 return y+"-"+m+"-"+d+""+h+":"+mi;
 }

 function praiseReply(el){

 var total=parseInt(el.getAttribute("total"));

 var my=parseInt(el.getAttribute("my"));

 var newtotal;

 if(my==0){

 newtotal=total+1;

 el.setAttribute("total",newtotal);

 el.setAttribute("my",1);

 el.innerHTML=newtotal+" cancel heart";
 }else{

 newtotal=total-1;
 el.setAttribute("total",newtotal);
 el.setAttribute("my",0);
 el.innerHTML=(newtotal==0)?" heart":newtotal+" heart";
 }
 }

 function operateReply(el){

 var comment=el.parentNode.parentNode.parentNode;

 var box=comment.parentNode.parentNode.parentNode;

 var textarea=box.getElementsByTagName("textarea")[0];

 var user=comment.getElementsByClassName("user")[0];

 var txt=el.innerHTML;

 if(txt=="reply"){

 textarea.onfocus();

 textarea.value="reply "+user.innerHTML;

 textarea.onkeyup();
 }else{

 remove(comment);
 }
 }

 for(var i=0;i<lists.length;i++){

 lists[i].onclick=function(e){

 var e=e||window.event;
 var el=e.srcElement;
 if(!el){
 el=e.target;
 }

 switch(el.className){

 case "close":
 remove(el.parentNode);
 break;

 case "dzan":
 praisebox(el.parentNode.parentNode.parentNode,el);
 break;

 case "hf-btn hf-btn-on":
 reply(el.parentNode.parentNode.parentNode);
 break;

 case "comment-zan":
 praiseReply(el);
 break;
 case "comment-dele":
 operateReply(el);
 break;
 }
 }
 var textarea=lists[i].getElementsByClassName("hf-text")[0];

 textarea.onfocus=function(){
 this.parentNode.className='hf hf-on';
 this.value = this.value == 'comment...' ? '' : this.value;
 }

 textarea.onblur=function(){
 if(this.value==''){
 this.parentNode.className='hf';
 this.value ='comment...';
 }
 }

 textarea.onkeyup=function(){
 var len=this.value.length;
 var textParentNode=this.parentNode;
 var textBtn=textParentNode.children[1];
 var textNub=textParentNode.children[2];
 if(len==0 /*|| len>100*/){
 textBtn.className="hf-btn";
 }else{
 textBtn.className="hf-btn hf-btn-on";
 /*this.style.color="#333"; */
 }
 textNub.innerHTML=len+"/100";
 }
 }

 }