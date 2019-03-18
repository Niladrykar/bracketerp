
$(document).ready(function () {
  var ShowForm = function () {
    var btn = $(this)
    $.ajax({
      url: btn.attr('data-url'),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        jQuery.noConflict()
        $('#modal-book').modal('show')
      },
      success: function (data) {
        $('#modal-book .modal-content').html(data.html_form)
      }
    })
  }

  var SaveForm = function () {
    var form = $(this)
    $.ajax({
      url: form.attr('data-url'),
      data: form.serialize(),
      type: form.attr('method'),
      dataType: 'json',
      success: function (data) {
        jQuery.noConflict()
        if (data.form_is_valid) {
          $('#book-table tbody').html(data.comments)
          $('#modal-book').modal('hide')
        } else {
          $('#modal-book .modal-content').html(data.html_form)
        }
      }
    })
    return false
  }

  // create
  $('.show-form').click(ShowForm)
  $('#modal-book').on('submit', '.create-form', SaveForm)

  // update
  $('#book-table').on('click', '.show-form-update', ShowForm)
  $('#modal-book').on('submit', '.update-form', SaveForm)

  // delete
  $('#book-table').on('click', '.show-form-delete', ShowForm)
  $('#modal-book').on('submit', '.delete-form', SaveForm)
})
