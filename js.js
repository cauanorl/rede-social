var page = 1;
var emptyPage = false;
var blockRequest = false;

$(window).scroll(function() {
  var margin = $(document).height() - $(window).height() - 200;

  if ($(window).scrollTop() > margin && emptyPage == false && blockRequest == false) {
    blockRequest = true;
    page += 1;
    $.get(`?page=${page}`, function(data) {
      if (data == '') {
        emptyPage = true;
      }
      else {
        blockRequest = false;
        $("#image-list").append(data);
      }
    });
  }
});