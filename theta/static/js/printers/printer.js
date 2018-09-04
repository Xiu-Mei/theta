let spareid = undefined;
$(function () {
    $('[data-toggle="tooltip"]').tooltip();
    $("#dialog_add_printer").dialog({
        modal: true,
        autoOpen: false,
        open : function(event, ui) {
                originalContent = $("#dialog_add_spare").html();
                },
        close : function(event, ui) {
                $("#dialog_add_spare").html(originalContent);
                },

        classes: {
            "ui-dialog-titlebar": "custom-info"
        },
        minWidth: 600,
        buttons: [{
            text: "Save",
            icon: "ui-icon-disk",
            click: function () {
                let mask = $("#mask option:selected").text();
                let inv_number = $("#inv_number").val();
                let note = $("#printer_note").val();
                let building = $("#buildingName").val();
                let floor = $("#floorName").val();
                let room = $("#roomName").val();
                let place = $("#placeName").val();
                let action = "addPrinterItem";
                $.ajax({
                    type: "POST",
                    url: request_path,
                    data: {
                        mask: mask,
                        inv_number: inv_number,
                        note: note,
                        building: building,
                        floor: floor,
                        room: room,
                        place: place,
                        action: action,
                    },
                    dataType: "json",
                    success: function (data) {
                        var json = JSON.parse(JSON.stringify(data));
                        if (json.success) {
                            $(document).trigger("add-alerts", [{
                                'message': json.success, //
                                'priority': 'success' // error, warning, success
                            }]);
                            $("#dialog_add_printer").dialog("close");
                            location.reload(true);
                        }
                        if (json.error) {
                            $(document).trigger("add-alerts", [{
                                'message': json.error, //
                                'priority': 'error' // error, warning, success
                            }]);
                        }
                    },
                    error: function () {
                        $(document).trigger("add-alerts", [{
                            'message': "Server not responding.", //
                            'priority': 'error' // error, warning, success
                        }]);

                    },
                });
            }
        }],
    });
    $("#dialog_add_spare").dialog({
        modal: true,
        autoOpen: false,
        open : function(event, ui) {
                originalContent = $("#dialog_add_spare").html();
                },
        close : function(event, ui) {
                $("#dialog_add_spare").html(originalContent);
                },
        classes: {
            "ui-dialog-titlebar": "custom-info"
        },
        minWidth: 600,
        buttons: [{
            text: "Add",
            icon: "ui-icon-disk",
            click: function () {
                var amount = $("#spare_amount").val();
                var action = "addSpareItem";
                $.ajax({
                    type: "POST",
                    url: request_path,
                    data: {
                        spareId: spareid,
                        amount: amount,
                        action: action,
                    },
                    dataType: "json",
                    success: function (data) {
                        var json = JSON.parse(JSON.stringify(data));
                        message.print(json);
                        if (json.success) {
                            $('[data-sparevalue='+spareid+']').text(json.instock);
                            $("#dialog_add_spare").dialog("close");
                        }
                    },
                    error: function () {
                        $(document).trigger("add-alerts", [{
                            'message': "Server not responding.", //
                            'priority': 'error' // error, warning, success
                        }]);

                    },
                });
            }
        }],
    });
    $("#btn_addprinter").click(function () {
        $("#dialog_add_printer").dialog("open");
        $("#inv_number").focus();
    });
    $(".btn_addspare").click(function () {
        spareid = $(this).attr('data-spareid');
        $("#dialog_add_spare").dialog("open");
        $("#add_spare").focus();
    });
    $("#buildingName").on('input', function () {
        var val = this.value;
        if($('#buildings option').filter(function(){
            return this.value === val;
        }).length) {
            $("#floors").empty();
            $("#floorName").val('');
            $("#rooms").empty();
            $("#roomName").val('');
            $("#places").empty();
            $("#placeName").val('');
            $.ajax({
                type: "POST",
                url: request_path,
                data: {
                    building: this.value,
                    action: "getFloors"
                },
                dataType: "json",
                success: function(data) {
                    var json = JSON.parse(JSON.stringify(data));
                    message.print(json);
                    if (json.floors !== undefined) {
                        for (let i=0; i < json.floors.length; i++) {
                            $('#floors').append("<option value='" + json.floors[i] + "'>");
                        }
                    }
                },
                error: function () {
                    $(document).trigger("add-alerts", [{
                        'message': "Server not responding.", //
                        'priority': 'error' // error, warning, success
                }]);

            },
        })
    }
    })
    $("#floorName").on('input', function () {
        var val = this.value;
        if($('#floors option').filter(function(){
            return this.value === val;
        }).length) {
            $("#rooms").empty();
            $("#roomName").val('');
            $("#places").empty();
            $("#placeName").val('');
            let building = $("#buildingName").val();
            $.ajax({
                type: "POST",
                url: request_path,
                data: {
                    building: building,
                    floor: this.value,
                    action: "getRooms"
                },
                dataType: "json",
                success: function(data) {
                    var json = JSON.parse(JSON.stringify(data));
                    message.print(json);
                    if (json.rooms !== undefined) {
                        $('#rooms').append("<option value='--------'>");
                        for (let i=0; i < json.rooms.length; i++) {
                            $('#rooms').append("<option value='" + json.rooms[i] + "'>");
                        }
                    }
                    if (json.places !== undefined) {
                        for (let i=0; i < json.places.length; i++) {
                            $('#places').append("<option value='" + json.places[i] + "'>");
                        }
                    }
                },
                error: function () {
                    $(document).trigger("add-alerts", [{
                        'message': "Server not responding.", //
                        'priority': 'error' // error, warning, success
                }]);

            },
        })
    }
    })
    $("#roomName").on('input', function () {
        var val = this.value;
        if($('#rooms option').filter(function(){
            return this.value === val
        }).length) {
            $("#places").empty();
            $("#placeName").val('');
            let building = $("#buildingName").val();
            let floor = $("#floorName").val();
            $.ajax({
                type: "POST",
                url: request_path,
                data: {
                    building: building,
                    floor: floor,
                    room: this.value,
                    action: "getPlaces"
                },
                dataType: "json",
                success: function(data) {
                    var json = JSON.parse(JSON.stringify(data));
                    message.print(json);
                    if (json.rooms !== undefined) {

                        for (let i=0; i < json.rooms.length; i++) {
                            $('#rooms').append("<option value='" + json.rooms[i] + "'>");
                        }
                    }
                    if (json.places !== undefined) {
                        for (let i=0; i < json.places.length; i++) {
                            $('#places').append("<option value='" + json.places[i] + "'>");
                        }
                    }
                },
                error: function () {
                    $(document).trigger("add-alerts", [{
                        'message': "Server not responding.", //
                        'priority': 'error' // error, warning, success
                }]);

            },
        })
    }
    })
});
let message = {
    print: function (json) {
        if (json.success !== undefined) {
            $(document).trigger("add-alerts", [{
                'message': json.success, //
                'priority': 'success' // error, warning, success
            }]);
        }
        if (json.error !== undefined) {
            $(document).trigger("add-alerts", [{
                'message': json.error, //
                'priority': 'error' // error, warning, success
            }]);

        }
    }
}
