$('#add_post_form').on('show.bs.modal', function (event) {
  var button = $(event.relatedTarget);
  var post_id = button.data('post-id');
  var hidden_post_id = $("#add_post_form > .modal-dialog > .modal-content > form > .modal-body > #post_id");
  hidden_post_id.val(post_id || 'None');
})