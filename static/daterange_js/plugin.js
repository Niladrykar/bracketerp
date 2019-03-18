
$(document).ready(function () {
  var ShowForm = function () {
    var btn = $(this)
    $.ajax({
      url: btn.attr('data-url'),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        jQuery.noConflict()
        $('#modal-book-date').modal('show')
      },
      success: function (data) {
        $('#modal-book-date .modal-content').html(data.html_form)
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
          $('#book-table-date tbody').html(data.selectdatefields_list)
          $('#modal-book-date').modal('hide')
        } else {
          $('#modal-book-date .modal-content').html(data.html_form)
        }
      }
    })
    return false
  }

  // create
  $('.show-form').click(ShowForm)
  $('#modal-book-date').on('submit', '.create-form', SaveForm)

  // update
  $('.show-form-update').click(ShowForm)
  $('#modal-book-date').on('submit', '.update-form', SaveForm)
})
