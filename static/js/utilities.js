const $ = jQuery.noConflict();

function openModal(modal_id, url) {
  $(modal_id).load(url, function () {
    $(modal_id).modal("show");
  });
}
