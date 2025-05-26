// static/js/buscar_dato.js

document.getElementById("corporacion").addEventListener("change", function() {
  var corporacion_id = this.value;
  if (corporacion_id) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/estructura/circunscripcion/' + corporacion_id, true);
    xhr.onload = function() {
      if (xhr.status === 200) {
        var data = JSON.parse(xhr.responseText);
        document.getElementById("circunscripcion").value =  data.circunscripcion_id;
        if (data.circunscripcion_id == 1){
            document.getElementById("municipio").style.display = "none";
            document.getElementById("comuna").style.display = "none";
        }
         if (data.circunscripcion_id == 2){
            document.getElementById("municipio").style.display = "block";
            document.getElementById("comuna").style.display = "none";
        }
        if (data.circunscripcion_id == 3){
            document.getElementById("municipio").style.display = "block";
            document.getElementById("comuna").style.display = "block";
        }

      } else {
        console.log('Error al buscar el dato');
      }
    };
    xhr.send();
  }
});

