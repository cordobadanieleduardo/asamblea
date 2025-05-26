function checkerConyugue(element) {
    if (element.checked) {
        document.getElementById('contenedor_conyugue').style.display = 'block';
    } else {
        document.getElementById('contenedor_conyugue').style.display = 'none';
    }
}

function soloNumeros(e) {
    var key = window.Event ? e.which : e.keyCode
    return (key >= 48 && key <= 57)
}
function sumar() {
    var salarios = document.getElementById('salarios').value;
    var cesantias = document.getElementById('cesantias').value;
    var representacion = document.getElementById('representacion').value;
    var arriendos = document.getElementById('arriendos').value;
    var honorarios = document.getElementById('honorarios').value;
    var otros_ingresos = document.getElementById('otros_ingresos').value;
    var total_ingresos = parseInt(salarios) + parseInt(cesantias) + parseInt(representacion) +  parseInt(arriendos) + parseInt(honorarios) + parseInt(otros_ingresos);
    document.getElementById('total_ingresos').value = total_ingresos;
}

$('form').submit(function(event) {
  event.preventDefault();
});

function guardar_declaracion() {
    formData = new FormData;

    formData.append('formacion_academica', $('#formacion_academica').val());
    formData.append('experiencia_laboral', $('#experiencia_laboral').val());
    formData.append('experiencia_social', $('#experiencia_social').val());
    formData.append('logros_reconocimientos', $('#logros_reconocimientos').val());
    formData.append('referencia_personal', $('#referencia_personal').val());
    formData.append('referencia_pav', $('#referencia_pav').val());
    formData.append('vida_politica', $('#trayectoria_politica').val());

    formData.append('antecedentes_penales', $('#antecedentes_penales').val());


    formData.append("solicitud_aval_check1", document.getElementById("solicitud_aval_check1").checked ? "True" : "False");
    formData.append("solicitud_aval_check2", document.getElementById("solicitud_aval_check2").checked ? "True" : "False");
    formData.append("solicitud_aval_check3", document.getElementById("solicitud_aval_check3").checked ? "True" : "False");
    formData.append("compromiso_check", document.getElementById("compromiso_check").checked ? "True" : "False");
    formData.append('boton_presionado', $('#boton_presionado').val());
    formData.append('dj_id', $('#dj_id').val());
    formData.append('eleccion', $('#eleccion').val());
    formData.append('corporacion', $('#corporacion').val());
    formData.append('historial', $('#historial').val());
    formData.append('dj_parientes', $('#dj_parientes').val());
    formData.append('csrfmiddlewaretoken', $('input[name=csrfmiddlewaretoken]').val());
    formData.append('salarios', $('#salarios').val());
    formData.append('cesantias', $('#cesantias').val());
    formData.append('representacion', $('#representacion').val());
    formData.append('arriendos', $('#arriendos').val());
    formData.append('honorarios', $('#honorarios').val());
    formData.append('otros_ingresos', $('#otros_ingresos').val());
    formData.append('total_ingresos', $('#total_ingresos').val());
    formData.append('dj_bancos', $('#dj_bancos').val());
    formData.append('dj_bienes', $('#dj_bienes').val());
    formData.append('dj_obligaciones', $('#dj_obligaciones').val());
    formData.append('dj_miembro', $('#dj_miembro').val());
    formData.append('dj_corporacion_socios', $('#dj_corporacion_socios').val());
    formData.append('dj_ecom_privada', $('#dj_ecom_privada').val());
    //checkConyugue
    formData.append('checkConyugue', $('#checkConyugue').prop('checked'));
    formData.append('dj_num_doc_conyuge', $('#dj_num_doc_conyuge').val());
    formData.append('dj_nombre_coyuge', $('#dj_nombre_coyuge').val());
    formData.append('dj_tipo_de_documento', $('#dj_tipo_de_documento').val());




    //ajax declaration-jurada
    $.ajax({
        url: '/formularios/declaracion-jurada/',
        type: 'POST',
        data: formData,
        contentType: false,
        processData: false,
        success: function (data) {
             if (data != '') {
            Swal.fire({
                title: 'Información',
                text: data,
                icon: 'info',
                confirmButtonText: 'Aceptar'
            });
        }}
    });

}
