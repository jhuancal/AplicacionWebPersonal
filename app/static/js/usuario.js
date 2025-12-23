// User JS Logic

var ClaseGlobalVar = {};
(function () {
    this.totalRecords = 0;
    this.getRowsTable = function () { return 10; };
    this.getIdEmpty = function () { return "00000000-0000-0000-0000-000000000000"; };
}).apply(ClaseGlobalVar);

var ClaseRegistro = {};
(function () {
    this.itemSelectedFiltro = 10;
    this.totalRecords = 0;
    this.currentPage = 1;
    this.estadoOrden = true;
    this.pagedItem = {
        filtros: [],
        orden: [{ OrderType: "DESC", Property: "Id", Index: "1" }],
        startIndex: 0,
        length: 10
    };

    var insert = true;
    var entity = {};

    this.setEntity = function (objeto) {
        entity.Id = objeto.Id;
        entity.NombreUsuario = objeto.NombreUsuario;
        entity.IdPersona = objeto.IdPersona;
        entity.RowVersion = objeto.RowVersion;
        // Password is not fetched back usually for security, only set on new
    };

    this.setNewEntity = function (objeto) {
        this.setEntity(objeto);
        entity.Id = ClaseGlobalVar.getIdEmpty();
        entity.Contrasena = "123456"; // Default password for new users for now
    };

    this.getEntity = function () { return entity; };
    this.getOperacion = function () { return insert; };
    this.setEdit = function () { insert = false; };
    this.setInsert = function () { insert = true; };

}).apply(ClaseRegistro);

var getFormValues = function () {
    return {
        NombreUsuario: $('#txtNombreUsuario').val(),
        IdPersona: $('#txtIdPersona').val()
    };
}

var setFormValuesEdit = function () {
    var e = ClaseRegistro.getEntity();
    $('#txtNombreUsuario').val(e.NombreUsuario);
    $('#txtIdPersona').val(e.IdPersona);
}

var clearForm = function () {
    $('#txtNombreUsuario').val("");
    $('#txtIdPersona').val("");
}

$(function () {
    initDataTable();
    initEvent();
});

var initDataTable = function () {
    fload("show");

    callAjax(ClaseRegistro.pagedItem.filtros, urlCountAll, "POST").done(function (r1) {
        var total = r1[0];

        callAjax(ClaseRegistro.pagedItem, urlGetPaged, "POST").done(function (data) {
            $("#tableRegistros tbody").empty();

            data.forEach(function (item, index) {
                var btnEdit = $("<button>", {
                    class: "btn btn-default btn-sm",
                    title: "Editar",
                    click: function () { eventClickEditar(item); }
                }).append($("<i>", { class: "fa fa-pencil text-warning" }));

                var btnDelete = $("<button>", {
                    class: "btn btn-default btn-sm",
                    title: "Eliminar",
                    click: function () { eventClickEliminar(item); }
                }).append($("<i>", { class: "fa fa-times text-danger" }));

                var row = $("<tr>").append(
                    $("<td>", { class: "text-center" }).text(getNro(ClaseRegistro.pagedItem.startIndex + index)),
                    $("<td>", { class: "text-center" }).text(item.NombreUsuario),
                    $("<td>", { class: "text-center" }).text(item.IdPersona || "N/A"),
                    $("<td>", { class: "text-center" }).text(item.ESTADO == 1 ? "Activo" : "Inactivo"),
                    $("<td>", { class: "text-center" }).append([btnEdit, " ", btnDelete])
                );
                $("#tableRegistros tbody").append(row);
            });

            getPaginator(total, ClaseRegistro.currentPage);
            getLabelRegistro(total);
            fload("hide");
        });
    });
};

var eventClickNuevo = function () {
    ClaseRegistro.setInsert();
    clearForm();
    $(".label-title").text("NUEVO").removeClass("edit").addClass("new");
    $("#modalRegistro").modal("show");
}

var eventClickEditar = function (data) {
    ClaseRegistro.setEdit();
    ClaseRegistro.setEntity(data);
    setFormValuesEdit();
    $(".label-title").text("EDITAR").removeClass("new").addClass("edit");
    $("#modalRegistro").modal("show");
};

var eventClickSaveRegistro = function () {
    var data = getFormValues();
    if (ClaseRegistro.getOperacion()) {
        ClaseRegistro.setNewEntity(data);
        callAjax(ClaseRegistro.getEntity(), urlInsert, "POST").done(function () {
            initDataTable();
            $("#modalRegistro").modal("hide");
            Noty("success", "Éxito", "Guardado correctamente");
        });
    } else {
        var entity = ClaseRegistro.getEntity();
        entity.NombreUsuario = data.NombreUsuario;
        entity.IdPersona = data.IdPersona;

        callAjax(entity, urlUpdate, "PUT").done(function () {
            initDataTable();
            $("#modalRegistro").modal("hide");
            Noty("success", "Éxito", "Actualizado correctamente");
        });
    }
};

var eventClickEliminar = function (data) {
    bootbox.confirm("¿Está seguro de eliminar el registro?", function (result) {
        if (result) {
            callAjax(data, urlDelete, "DELETE").done(function () {
                initDataTable();
                Noty("success", "Éxito", "Eliminado correctamente");
            });
        }
    });
};

// Reuse Paginator Logic (Could be extracted to shared JS)
var getPaginator = function (count, currentPage) {
    var numRows = $('#numRows').val();
    var numPages = count >= parseInt(numRows) ? Math.ceil(count / parseInt(numRows)) : 1;
    $('.pagination').empty();
    for (var i = 1; i <= numPages; i++) {
        var active = i === currentPage ? 'active' : '';
        (function (page) {
            var li = $('<li>', { class: 'paginate_button ' + active });
            var a = $('<a>', { text: page, href: '#' }).click(function (e) { e.preventDefault(); getPage(page, count); });
            li.append(a);
            $('.pagination').append(li);
        })(i);
    }
};

var getPage = function (currentPage, total) {
    var currentRango = parseInt($('#numRows').val());
    var inicio = (currentPage - 1) * currentRango;
    ClaseRegistro.pagedItem.startIndex = inicio;
    ClaseRegistro.pagedItem.length = currentRango;
    ClaseRegistro.currentPage = currentPage;
    initDataTable();
};

var getLabelRegistro = function (total) {
    var from = ClaseRegistro.pagedItem.startIndex + 1;
    var to = (ClaseRegistro.pagedItem.startIndex + ClaseRegistro.pagedItem.length) < total
        ? (ClaseRegistro.pagedItem.startIndex + ClaseRegistro.pagedItem.length) : total;
    if (total == 0) from = 0;
    $('#labelRegistros').text('Mostrando ' + from + ' - ' + to + ' de ' + total);
};

var initEvent = function () {
    $('#numRows').change(function () {
        ClaseRegistro.pagedItem.length = parseInt($(this).val());
        ClaseRegistro.pagedItem.startIndex = 0;
        ClaseRegistro.currentPage = 1;
        initDataTable();
    });

    $('#txtBuscar').keyup(function () {
        var val = $(this).val().trim();
        ClaseRegistro.pagedItem.filtros = [];
        if (val) {
            ClaseRegistro.pagedItem.filtros.push({
                Logical: "AND",
                PropertyName: "NombreUsuario",
                Value: val,
                Operator: "Contains"
            });
        }
        initDataTable();
    });
};
