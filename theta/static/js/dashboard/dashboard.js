$(function () {
    $("#search_str").on("keydown", function (event) {
        if (event.which == 13) {
            let search_str = $("#search_str").val()
            let search_action = $("#search_action").val()
            console.log(search_str)
            console.log(search_action)
            $.ajax({
                type: "POST",
                url: request_path,
                data: {'search_str': search_str, 'action': search_action},
                success: function (data) {
                    console.log(data)
                    $('#search-result').html(data);
                }
            });
        }
    });
})