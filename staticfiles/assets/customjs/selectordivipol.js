

        //Obtener el departamento que viene de la vista
        document.getElementById("departamento").value = codigoDepartamento;
        //Obtener la eleccion que viene de la vista
        if (codigoEleccion >= 0) {
            document.getElementById("eleccion").value = codigoEleccion;
            seleccion_eleccion();
        }


        //Obtener los municipios del departamento seleccionado
        var codDepartamento = codigoDepartamento;
        $.getJSON('/municipio_select/', {departamento_id: codDepartamento}, function(data) {
            $.each(data, function(index, municipio) {
                $('#municipio').append($('<option>', {
                    value: municipio.id,
                    text: municipio.nombre
                }));
            });
            document.getElementById("municipio").value = codigoMunicipio;
        });



        window.addEventListener('load', function() {

             if($('#corporacion').val() != 5) {
                 $('#comuna').prop('disabled', true);
                 $('#comuna').hide();
                 $('#comunalbl').hide();
             } else {
                 seleccion_corporacion()
             }


        });


// Obtener los municipios del departamento seleccionado
        function seleccion_departamento() {
                var departamentoId = $('#departamento').val();
                if (departamentoId) {
                    $.getJSON('/municipio_select/', {departamento_id: departamentoId}, function(data) {
                        // Limpiar opciones antiguas
                        $('#municipio').empty();
                        // Agregar opciones nuevas
                        $('#municipio').empty().append($('<option>', {
                            value: '*',
                            text: 'todos los municipios'
                        }));
                        // Deshabilitar select de comunas
                        $('#comuna').hide();
                        $('#comunalbl').hide();
                        $('#comuna').prop('disabled', true);
                        // Limpiar opciones antiguas
                        $('#comuna').empty().append($('<option>', {
                            value: '',
                            text: '---------'
                        }));
                        $.each(data, function(index, municipio) {
                            $('#municipio').append($('<option>', {
                                value: municipio.id,
                                text: municipio.nombre
                            }));
                        });
                        // Habilitar select de municipios
                        $('#municipio').prop('disabled', false);

                    });
                } else {
// Deshabilitar select de municipios
                    $('#municipio, #comuna').prop('disabled', true);
                    $('#comuna').hide();
                    $('#comunalbl').hide();

// Limpiar opciones antiguas
                    $('#municipio, #comuna').empty().append($('<option>', {
                        value: '*',
                        text: 'todos los municipios'
                    }));
                }
            }

        // Obtener las comunas del municipio seleccionado


        function select_municipio() {
            //establece la corporacion a todas las corporaciones
            document.getElementById("corporacion").value = "*";
               $('#comuna').prop('disabled', true);
                $('#comuna').hide();
                $('#comunalbl').hide();
// Limpiar opciones antiguas
                $('#comuna').empty().append($('<option>', {
                    value: '',
                    text: '---------'
                }));

        }


        //seleccion_eleccion_corporacion
        function seleccion_eleccion(){



            let select = $('#corporacion');
            select.empty()
            select.append('<option value="*" selected>todas las corporaciones</option>');

            formData = new FormData();
            formData.append('eleccion', $('#eleccion').val());
            formData.append('csrfmiddlewaretoken', csrf_token)

            $.ajax({
                url: '/seleccion_eleccion_corporacion/',
                type: 'POST',
                data: formData,
                processData: false,
                contentType: false,
                success: function (data) {
                    $.each(data, function(index, opcion) {
                        select.append('<option value="' + opcion.codigo + '">' + opcion.nombre + '</option>');
                    });
                   if (codigoCorporacion) {
                        document.getElementById("corporacion").value = codigoCorporacion;
                    }
                },
                error: function (data) {
                    console.log(data);
                }
            });
        }

        function seleccion_corporacion() {
            if($('#corporacion').val() == 5){

       var municipioId = $('#municipio').val();
            if (municipioId) {
                $.getJSON('/comuna_select/', {municipio_id: municipioId}, function(data) {
                 // Verificar si el JSON devuelto está vacío
                    if($.isEmptyObject(data)){
                        // Deshabilitar select de comunas
                        $('#comuna').prop('disabled', true);
                        $('#comuna').hide();
                        $('#comunalbl').hide();
                        // Limpiar opciones antiguas
                        $('#comuna').empty().append($('<option>', {
                            value: '',
                            text: '---------'
                        }));
                    }else{
                        // Limpiar opciones antiguas
                        $('#comuna').empty();
                        // Agregar opciones nuevas
                        $.each(data, function(index, comuna) {
                            $('#comuna').append($('<option>', {
                                value: comuna.id,
                                text: comuna.nombre
                            }));
                        });
                        // Habilitar select de comunas
                        $('#comuna').prop('disabled', false);
                        $('#comuna').show();
                        if (codigoComuna) {
                            document.getElementById("comuna").value = codigoComuna;
                        }
                        $('#comunalbl').show();
                    }
                });
            } else {
// Deshabilitar select de comunas
                $('#comuna').prop('disabled', true);
                $('#comuna').hide();
                $('#comunalbl').hide();
// Limpiar opciones antiguas
                $('#comuna').empty().append($('<option>', {
                    value: '',
                    text: '---------'
                }));
            }



            }else{
                $('#comuna').prop('disabled', true);
                $('#comuna').hide();
                $('#comunalbl').hide();
                $('#comuna').empty().append($('<option>', {
                    value: '',
                    text: '---------'
                }));
            }

        }
