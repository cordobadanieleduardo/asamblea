
   function cargarTabla(tabla, textarea, datos, campos) {
    var tbody = tabla.querySelector('tbody');
    tbody.innerHTML = '';
    datos.forEach(function(dato) {
      var tr = document.createElement('tr');
      campos.forEach(function(campo) {
        var td = document.createElement('td');
        td.textContent = dato[campo];
        tr.appendChild(td);
      });
      var td = document.createElement('td');
      var button = document.createElement('button');
      button.type = "button";
      button.classList.add("btn", "btn-danger");
      button.textContent = "Eliminar";
      button.addEventListener("click", function() {
        deleteTableRow(tabla,campos,button,textarea);
      });
      td.appendChild(button);
      tr.appendChild(td);
      tbody.appendChild(tr);
    });
  }
 // Función para eliminar una fila de la tabla
  function deleteTableRow(tabla,campos,btn,textarea) {
    var row = btn.parentNode.parentNode;
    row.parentNode.removeChild(row);
    getDatosTabla(tabla, campos,textarea);
  }


  // Función para agregar una nueva fila a la tabla
  function addTableRow(tabla, campos, textarea) {
    tabla = document.getElementById(tabla);
    // Obtiene los valores de los campos de entrada
    var values = campos.map(function(campo) {
      return document.getElementById(campo).value;
    });

    // Crea una nueva fila y agrega los valores de los campos de entrada
    var newRow = tabla.insertRow();
    values.forEach(function(value) {
      var newCell = newRow.insertCell();
      newCell.textContent = value;
    });
    var newCell = newRow.insertCell();
    var button = document.createElement('button');
    button.type = "button";
    button.classList.add("btn", "btn-danger");
    button.textContent = "Eliminar";
    button.addEventListener("click", function() {
        deleteTableRow(tabla,campos,button,textarea);
    });
    newCell.appendChild(button);
    getDatosTabla(tabla, campos,textarea);
  }

  function getDatosTabla(tabla, campos,textarea){
  var datos = [];
  var filas = tabla.getElementsByTagName('tr');
  for (var i = 1; i < filas.length; i++) {
    var fila = filas[i];
    var celdas = fila.getElementsByTagName('td');
    var dato = {};
    for (var j = 0; j < campos.length; j++) {
      dato[campos[j]] = celdas[j].textContent;
    }
    datos.push(dato);
  }
  document.getElementById(textarea).value = JSON.stringify(datos);
}


