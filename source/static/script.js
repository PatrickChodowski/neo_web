//jquery functions


$("document").ready(function(){

    $(".node").on("click", find_rels)

    function find_rels() {
        console.log('REQUEST SENT')
        var node_name = $.trim(this.innerHTML);

              $.ajax({
              url:"/find_rels",
              type:"POST",
              data: JSON.stringify(node_name),
              contentType:"application/json;charset=UTF-8",
              success:       function(data, status){
                    alert("Data: " + data + "\nStatus: " + status);
                  }
            })
      }
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




