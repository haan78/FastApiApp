import UseJS from "./lib/UseJS";

UseJS().css("/static/base.css")
.css("/static/dist/css/chunk-vendors.css")
.css("/static/dist/css/main.css")
.js("/static/dist/js/chunk-vendors.js")
.js("/static/dist/js/main.js",{ before:()=>{
    document.body.innerHTML = "";
    var div = document.createElement("div");
    div.setAttribute("id","app");
    document.body.appendChild(div);
}})
.load();