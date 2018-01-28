/* DjangoMultiUploadJS */
(function ($) {
  jQuery(document).ready(function () {

    var $block = jQuery('.js-multi-upload'),
      $text = $('.js-multi-upload-text'),
      $progress = $('.js-multi-upload-progress'),
      activeText = $text.text(),
      activeClass = 'active',
      disableClass = 'disabled',
      hoverClass = 'hover';

    var images;

    var app_model = $block.data('app-model');
    console.log(app_model);
    var row_class = '.dynamic-' + app_model + '-content_type-object_id .file-link[href=""]';
    console.log(row_class);

    function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
          var cookie = jQuery.trim(cookies[i]);
          // Does this cookie string begin with the name we want?
          if (cookie.substring(0, name.length + 1) == (name + '=')) {
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
    }

    function sameOrigin(url) {
      // test that a given url is a same-origin URL
      // url could be relative or scheme relative or absolute
      var host = document.location.host; // host + port
      var protocol = document.location.protocol;
      var sr_origin = '//' + host;
      var origin = protocol + sr_origin;
      // Allow absolute or scheme relative URLs to same origin
      return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
      beforeSend: function (xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
          // Only send the token to relative URLs i.e. locally.
          xhr.setRequestHeader("X-CSRFToken",
            $('input[name="csrfmiddlewaretoken"]').val());
        }
      }
    });

    initForm();

    $block.on('drag dragstart dragend dragover dragenter dragleave drop', function (e) {
      e.preventDefault();
      e.stopPropagation();
    })
      .on('dragover dragenter', function () {
        $block.addClass(hoverClass);
      })
      .on('dragleave dragend drop', function () {
        $block.removeClass(hoverClass);
      })
      .on('drop', function (e) {
        if (!$block.hasClass(disableClass)) {
          var $input = $block.find('input[type="file"]');
          images = e.originalEvent.dataTransfer.files;
          jQuery.each(images, function (i, item) {
            $block.find('input[type="file"]').prop('file', item);
            var data = new FormData($block.get(0));
            data.append($input.attr('name'), item);
            $.ajax({
              method: 'POST',
              url: $block.attr('action'),
              data: data,
              dataType: 'json',
              cache: false,
              contentType: false,
              processData: false,
              xhr: function () {
                var xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener("progress", function (evt) {
                  if (evt.lengthComputable) {
                    var percentComplete = Math.round(evt.loaded / evt.total * 100);

                    uploadProgress(percentComplete);
                  }
                }, false);
                xhr.addEventListener("progress", function (evt) {
                  if (evt.lengthComputable) {
                    var percentComplete = Math.round(evt.loaded / evt.total * 100);

                    uploadProgress(percentComplete);
                  }
                }, false);
                return xhr;
              },
              beforeSend: function (xhr) {
                xhr.setRequestHeader('X-CSRFToken', csrftoken);
              },
              complete: function () {
                makeFormActive(activeText);
              },
              success: function (data) {
                addImagesToList(data);
              }
            });
          });
        }
      });

    function uploadProgress(precents) {
      $block.removeClass(activeClass);
      $block.addClass(disableClass);

      $progress.children().eq(0).text(precents + '%');
      $progress.children().eq(1).text(precents + '%');
      $progress.children().eq(1).css({
        height: precents + '%'
      });
      $text.text('Терпение, мой друг');
    }

    function makeFormActive(text) {
      $block.removeClass(disableClass);
      $block.addClass(activeClass);
      $text.text(text);
    }

    function addImagesToList(data) {
      $('.add-row').find('a').trigger('click');

      var row = $('.dynamic-image-image-content_type-object_id');

      var link = $(document).find(row_class);
      if (link.attr('href') === '') {
        link.attr('href', data.url);
        link.children('img').attr('src', data.url);
      }

      var input = link.siblings('input.file-path');

      input.val(data.filename);

      var parent = link.parent('.form-active');

      parent.removeClass('form-active');
      parent.addClass('img-active');
    }

    function initForm() {
      $block.addClass(activeClass);
    }
  });
})(django.jQuery);
