$(function () {
    $('[data-toggle="tooltip"]').tooltip();
    $("#savePrintItem").click(function () {
        let condition = $("input[type=radio][name=condition]:checked").val()
        let notes = $("#TA_PrinterItemCommentary").val()
        $.ajax({
            type: "POST",
            url: request_path,
            data: {
                condition: condition,
                notes: notes,
                action: "savePrinterItem",
            },
            dataType: "json",
            success: function (data) {
                let json = JSON.parse(JSON.stringify(data));
                if (json.success) {
                    $(document).trigger("add-alerts", [{
                        'message': json.success, //
                        'priority': 'success' // error, warning, success
                    }]);
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
    });
    $(".issuing").click(function () {
        let cartridge_id = $(this).attr('data-cartridge_item_id');
        $.ajax({
            type: "POST",
            url: request_path,
            data: {
                cartridge_id: cartridge_id,
                action: "cartridgeIssue",
            },
            dataType: "json",
            success: function (data) {
                let json = JSON.parse(JSON.stringify(data));
                if (json.success) {
                    $(document).trigger("add-alerts", [{
                        'message': json.success, //
                        'priority': 'success' // error, warning, success
                    }]);
                    $('.instock').each(function () {
                        if ($(this).attr('data-cartridge_item_id') == json.cartridge_item_id) {
                            $('h3', this).text(json.instock)
                        }
                    })
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

    });

});