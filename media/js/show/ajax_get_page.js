var from;
var stop;
var mode;
var scroll_lock;

function init() {
  from = 0;
  stop = false;
  mode = 'normal';
  scroll_lock = false;
  $('div#load-entry-tip').hide();

  $('div#container').masonry('destroy').html('').masonry({
    itemSelector: '.box',
    columnWidth : 326
  });
  append_entries();
};

function append_entries(date) {
  $('#load-entry-tip').hide();
  if (data.length == 0) {
    stop = true;
    $('#load-entry-tip').html('已是全部内容');
    $('#load-entry-tip').show();
    return;
  }
  $('div#container').append(html).masonry('appended', dboxes);
  scroll_lock = false;
  from = from + 1;
};

$(function(){
  init();
  $(window).bind("scroll",function(){
    if (mode != 'normal') return;
    if( $(document).scrollTop() + $(window).height() > $(document).height() - 10 ) {
      if (stop) return;
      if (scroll_lock) return;
      scroll_lock = true;
      append_entries();
    }
  });
});

