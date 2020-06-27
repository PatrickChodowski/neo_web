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
              success: read_rels
            })
      }
      function read_rels(data, status){
        //alert("Data: " + data + "\nStatus: " + status);
        console.log(data)
      }


      function draw_port(left, top){
            var d = document.createElement('div');
            d.className = "port";
            d.style.position = "absolute";
            d.style.left = left+'px';
            d.style.top = top+'px';
            $("body").append(d);
      }

     function get_element_position(element_id){
        var element = document.getElementById(element_id);
        var rect = element.getBoundingClientRect();
        //console.log(rect.top, rect.right, rect.bottom, rect.left);

        var m_y = (rect.bottom + rect.top)/2;
        var m_x = (rect.right + rect.left)/2;

        //console.log(m_x, m_y)
        var possible_ports = [[m_x, m_y + 12], [m_x, m_y - 15], [m_x + 100, m_y], [m_x - 103, m_y]];

        $.each(possible_ports, function(index, value) {
            console.log(value)
            draw_port(value[0], value[1])
        });

        return possible_ports[0]
        // find center and possible line ports
    }

    function draw_link(){

    }



    function draw_rel(){
        console.log(this.id)
        var res = this.id.split("_");

        start_pos = get_element_position(res[0])
        end_pos = get_element_position(res[1])

        //<svg height="210" width="500">
        //    <line x1=start_pos[0] y1=start_pos[1] x2=end_pos[0] y2=end_pos[1] style="stroke:rgb(255,0,0);stroke-width:2" />
        //</svg>

    }

    $(".rel").each(draw_rel)

})

// position of element


















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




