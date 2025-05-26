
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
        var editButton = document.createElement('button');
        editButton.type = "button";
        editButton.classList.add("btn", "btn-secondary");
        editButton.innerText = 'Editar';
        editButton.addEventListener("click", function() {
    var row = this.parentNode.parentNode;
    if (this.innerText === 'Editar') {
        this.innerText = 'Guardar';
        makeRowEditable(row);
    } else {
        this.innerText = 'Editar';
        revertRow(row, tabla, campos, textarea);

    }
});
        td.appendChild(editButton);
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


  function cargarTablaVista(tabla, textarea, datos, campos) {
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
      tr.appendChild(td);
      tbody.appendChild(tr);
    });
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
    var editButton = document.createElement('button');
        editButton.type = "button";
        editButton.classList.add("btn", "btn-secondary");
        editButton.innerText = 'Editar';
      editButton.addEventListener("click", function() {
          var row = this.parentNode.parentNode;
          if (this.innerText === 'Editar') {
                 this.innerText = 'Guardar';
              makeRowEditable(row);
          } else {
               this.innerText = 'Editar';
              revertRow(row, tabla, campos, textarea);

          }
      });
        newCell.appendChild(editButton);


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

// En formularios.js

// Función para convertir una fila en campos de entrada
function makeRowEditable(row) {
    var cells = row.children;
    for (var i = 0; i < cells.length; i++) {
        var cell = cells[i];
        // Verificar si la celda contiene un botón o está vacía
        if (!cell.firstChild || cell.firstChild.nodeName !== 'BUTTON') {
            var text = cell.innerText;
            cell.innerHTML = '';
            var input = document.createElement('input');
            input.type = 'text';
            input.value = text;
            cell.appendChild(input);
        }
    }
}
// Función para revertir la fila a texto normal
// Función para revertir la fila a texto normal y actualizar el textarea
function revertRow(row, tabla, campos, textarea) {
    var cells = row.children;
    for (var i = 0; i < cells.length; i++) {
        var cell = cells[i];
        if (cell.firstChild && cell.firstChild.nodeName !== 'BUTTON') {
    var input = cell.firstChild;
            cell.innerHTML = input.value;
        }
    }
    // Actualizar el textarea con los datos actuales de la tabla
    getDatosTabla(tabla, campos, textarea);
}



