$(document).ready(function () {
    function cargarTablaCompleta() {
        const columnasSeleccionadas = obtenerColumnasSeleccionadas();

        $.ajax({
            url: '/filtrar',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                'columna': '',
                'valor': '',
                'columnas_seleccionadas': columnasSeleccionadas,
            }),
            success: function (response) {
                $('#tabla-datos').html(response.tabla);
            },
        });
    }

    // $('#download-filtered').click(function() {
    //     window.location.href = '/download_filtered';
    // });
    
    let isReload = false;

    // Detecta si la página está siendo recargada
    window.addEventListener("beforeunload", function () {
        isReload = true;
    });

    // Envía la notificación al servidor si es una recarga
    window.addEventListener("unload", function () {
        if (isReload) {
            navigator.sendBeacon('/delete_table');
        }
    });
    
    $('#download-filtered').click(function () {
        // Captura las columnas seleccionadas
        const columnasSeleccionadas = $('input[name="column-checkbox"]:checked')
            .map(function () {
                return $(this).val();
            })
            .get()
            .join(',');
    
        // Generar la URL con las columnas seleccionadas como query string
        const downloadUrl = `/download_filtered?columnas=${encodeURIComponent(columnasSeleccionadas)}`;
    
        // Redirigir para descargar
        window.location.href = downloadUrl;
    });
    

    function obtenerColumnasSeleccionadas() {
        return $('input[name="column-checkbox"]:checked')
            .map(function () {
                return $(this).val();
            })
            .get();
    }

    // Cuando se selecciona una columna, obtener los valores correspondientes
    $('#column-selector').change(function () {
        var columna = $(this).val();
        if (columna) {
            $.ajax({
                url: '/obtener_valores',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({'columna': columna}),
                success: function (response) {
                    var valores = response.valores;
                    var valueSelector = $('#value-selector');
                    valueSelector.empty(); // Limpiar los valores anteriores
                    valueSelector.append('<option value="">-- Selecciona un valor --</option>');
                    $.each(valores, function (index, value) {
                        valueSelector.append('<option value="' + value + '">' + value + '</option>');
                    });
                }
            });
        } else {
            $('#value-selector').empty();
            $('#value-selector').append('<option value="">-- Selecciona un valor --</option>');
        }
    });

    $('#filter-button').click(function () {
        const columna = $('#column-selector').val();
        const valor = $('#value-selector').val();
        const columnasSeleccionadas = obtenerColumnasSeleccionadas();

        $.ajax({
            url: '/filtrar',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                'columna': columna,
                'valor': valor,
                'columnas_seleccionadas': columnasSeleccionadas,
            }),
            success: function (response) {
                $('#tabla-datos').html(response.tabla);
            },
        });
    });

    $('input[name="column-checkbox"]').change(function () {
        cargarTablaCompleta();
    });

    $('#select-all-columns').click(function () {
        $('input[name="column-checkbox"]').prop('checked', true); // Marca todas las casillas
        cargarTablaCompleta(); // Actualiza la tabla con las columnas seleccionadas
    });

    // Botón "Deseleccionar Todas"
    $('#deselect-all-columns').click(function () {
        $('input[name="column-checkbox"]').prop('checked', false); // Desmarca todas las casillas
        cargarTablaCompleta(); // Actualiza la tabla con las columnas seleccionadas
    });

    $('#reset-filters-btn').click(function () {
        // Obtener las columnas actualmente seleccionadas en las casillas de verificación
        const columnasSeleccionadas = obtenerColumnasSeleccionadas();
    
        // Solicitar al backend que restaure los datos originales pero solo para las columnas seleccionadas
        $.ajax({
            url: '/reset_filters',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({'columnas_seleccionadas': columnasSeleccionadas}),
            success: function (response) {
                // Actualizar la tabla con los datos restaurados y las columnas seleccionadas
                $('#tabla-datos').html(response.tabla);
    
                // Mantener el estado actual de los selectores (no limpiar valores)
            },
        });
    });
    
    
    

    cargarTablaCompleta();


    // Función para resetear la tabla al estado original al cargar la página
    function cargarTablaOriginal() {
        $.ajax({
            url: '/reset_filters',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({'columnas_seleccionadas': obtenerColumnasSeleccionadas()}),
            success: function (response) {
                $('#tabla-datos').html(response.tabla);
            },
        });
    }

    $(document).ready(function () {
        cargarTablaOriginal(); // Asegura que la tabla esté en su estado original al cargar
    });

});
