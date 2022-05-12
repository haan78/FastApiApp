import UseJS from "./lib/UseJS";

UseJS().css("/static/base.css").js("/static/dist/main.js",{ 
    type:"module",
    before:()=>{
    document.body.innerHTML = "";
    var div = document.createElement("div");
    div.setAttribute("id","app");
    document.body.appendChild(div);
}}).load();