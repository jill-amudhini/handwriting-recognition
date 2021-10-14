var nav = document.getElementsByTagName("nav")[0];
var burger = document.getElementsByClassName("burger")[0];

burger.addEventListener("click", clicked);
var j = 0;
function clicked() {
  if (j === 0) {
    nav.style = "left:0";
    j++;
  } else {
    nav.style = "left:-250px";
    j--;
  }
}