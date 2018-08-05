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
    // $(window).scroll(function(){
    //   var sticky = $('.header'),
    //       scroll = $(window).scrollTop();
    //
    //   if (scroll >= 100) sticky.addClass('fixed');
    //   else sticky.removeClass('fixed');
    // });
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
        console.log('sdfsdlkfjsldf');
        $(".selected").removeClass("selected");
        $(this).addClass("selected");
        // $("input[type=text][name=place_input]").val($(this).find('span').text());
        // $(this).find('span').text()
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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
};
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
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
<div class="container">
    <div class="row">

        <div class="header">
            <div class="input-group mb-3 former" id="input_group">
                <input type="checkbox" data-toggle="toggle" data-on="Edit" data-off="Freeze" data-onstyle="success"
                       id="edit_toggle">
                <div class="input-group-prepend">
                    <button type="button" class="btn btn-outline-secondary hidable" id="add_place">add place</button>
                </div>
                <input type="text" class="form-control hidable" placeholder="Places' name"
                       aria-label="Places' name" name="place_input">
                <div class="input-group-append">
                    <button class="btn btn-outline-primary hidable" id="save_place_name" type="button">Save</button>
                    <button class="btn btn-outline-danger hidable" id="delete_place" type="button">Delete</button>
                </div>
            </div>
        </div>
        <div id="parent">
            <img src="{{MEDIA_URL}}{{floor.plan}}" alt="" id="plane_img" style="max-width: none;">
          {% for place in places %}
          <div class="place" id="{{place.id}}" style="position: absolute; left: {{place.left}}px; top: {{place.top}}px;">
                <span>{{place.name}}</span>
            </div>
          {% endfor %}
          <div class="place" id="55" style="position: absolute; left: 330px; top: 400px;">
    <span>1234534535345</span>
</div>

      </div></div></div>
body {
  -moz-user-select: none;
  -webkit-user-select: none;
  -ms-user-select: none;
  user-select: none;
  -o-user-select: none;
}

.header {
  height: 60px;
  padding: 1em;
  background: rgba(178, 178, 178, .2);
}

.fixed {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
}

.place {
  display: table;
  padding: 1px;
  min-height: 20px;
  border-radius: 3px;
  border: 1px solid black;
  background-color: grey;
  text-align: center;
}

.place span {
  font-size: 0.8em;
}

.selected {
  box-shadow: 0 0 3pt 2pt;
}

#parent {
  z-index: -1;
  position: relative;
  padding: 0;
  height: 920px;
  background-color: aqua;
}
