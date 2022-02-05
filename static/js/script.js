window.addEventListener("load", function () {
 var send= document.querySelector("#send");
 var form= document.querySelector("form");


window.addEventListener("scroll", function() {

    if (form.getBoundingClientRect().top < window.innerHeight - 100) {
      form.classList.add("active");
    } else {
      form.classList.remove("active");
    }

})
})
