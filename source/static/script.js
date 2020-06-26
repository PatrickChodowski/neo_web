//jquery functions


$("document").ready(function(){
})

function allowDrop(ev) {
  ev.preventDefault();
}

function drag(ev) {
  ev.dataTransfer.setData("text", ev.target.id);
}

function drop(ev) {
  ev.preventDefault();
  var data = ev.dataTransfer.getData("text");
  ev.target.appendChild(document.getElementById(data));
  var content =  document.getElementById("log_window").innerHTML + '\r\n' + data + ' -> ' + ev.target.id;
  document.getElementById("log_window").innerHTML = content;
}




