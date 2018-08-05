$(document).ready(function() {
    var drag_disable_state = true;
    var planeImg = new Image();
    var image_width = '400px';
    var image_height = '400px';
    $(".hidable").hide();
    planeImg.src = $("#plane_img").attr('src');
    planeImg.onload = function() {
        image_width = this.width;
        image_height = this.height;
        $("#parent").css('width', image_width);
        $("#parent").css('height', image_height);
    };
     $(window).scroll(function(){
       var sticky = $('.header'),
           scroll = $(window).scrollTop();

       if (scroll >= 60) sticky.addClass('fixed');
       else sticky.removeClass('fixed');
     });
    function drag_place() {
        $(".place").draggable({
            disabled: drag_disable_state,
            stop: function(e, ui) {
                postSelected("save")
            },
            containment: "parent"
        });
    };
    drag_place();
    $("#add_place").click(function() {
        var left = image_width / 2 + getRandomInt(1, 50);
        var top = image_height / 2 + getRandomInt(1, 50);
        var html = '<div class="place" style="position: absolute; left:' + left + 'px; top:' + top + 'px;">' +
            '<span>new</span></div>';
        $('#parent').append(html);
        drag_place()
    });
    $("#edit_toggle").change(function() {

        if (drag_disable_state === false) {
            drag_disable_state = true;
            $(".hidable").hide('fast');
        } else {
            drag_disable_state = false;
            $(".hidable").show('fast');
        }

        $(".place").draggable({
            disabled: drag_disable_state,
        });

    });
    $(".place").click(function(){
        console.log("sdfsfsdf");
    })
    $("#parent").on("mousedown", ".place", function() {
        $(".selected").removeClass("selected");
        $(this).addClass("selected");
         $("input[type=text][name=place_input]").val($(this).find('span').text());
    });
    $("#save_place_name").click(function() {
        if ($(".selected")[0]) {
            console.log('im in save')
            var place_text = $("input[type=text][name=place_input]").val();
            place_text = place_text.match(/.{1,7}/g).join("<br>");
            $(".selected span").html(place_text);
            postSelected("save");
        }
    });
    $("#delete_place").click(function() {
        if ($(".selected")[0]) {
            if ($(".selected").attr("id") == null) {
                $(".selected").remove();
            } else if ($(".selected").attr("id") > 0) {
                postSelected("delete")
            };
    };
    });
});

function postSelected(action) {
    var id = $(".selected").attr('id');
    var place_left = $(".selected").css("left");
    var place_top = $(".selected").css("top");
    var text = $(".selected span").html();

    console.log("id=", id, "left=", place_left, "top=", place_top, "text=", text, "action=", action)
    $.ajax({
        type: "POST",
        url: request_path,
        data: {
            id: id,
            left: place_left,
            top: place_top,
            text: text,
            action: action
        },
        dataType: "json",
        success: function(data) {
            var json = JSON.parse(JSON.stringify(data));
            console.log(json.id);
            if (id == null) {
                $(".selected").attr('id', json.id);
            }
            if (json.id == 0) {
                $(".selected").remove();
            }
        }
    });
};

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
};
