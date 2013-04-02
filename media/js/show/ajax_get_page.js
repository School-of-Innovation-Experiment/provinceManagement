var page;
var stop;
var mode;
var scroll_lock;

function init() {
  page = 0;
  stop = false;
  mode = 'normal';
  scroll_lock = false;
  $('div#load-entry-tip').hide();

  $('div#flow_container').masonry('destroy').html('').masonry({
    itemSelector: '.box',
    columnWidth : 326
  });
  Dajaxice.showtime.project_turn_page(append_entries, {"project_page": page, "project_search": ""});
};

function append_entries(html) {
  $('#loading-entry-tip').hide();
  if (html.length == 0) {
    stop = true;
    return;
  }
  var $boxes = $(html.html);
  $('div#flow_container').append($boxes).masonry('appended', $boxes);
  scroll_lock = false;
  page = page + 1;
  if($('#load-over-entry-tip'))
    {
      stop = true;
    }
};

$(function(){
  init();
  $(window).bind("scroll",function(){
    if (mode != 'normal') return;
    if (stop) return;
    if (scroll_lock) return;
    if( $(document).scrollTop() + $(window).height() > $(document).height() - 10 ) {
      scroll_lock = true;
      $('#loading-entry-tip').show();
      Dajaxice.showtime.project_turn_page(append_entries, {"project_page": page, "project_search": ""});
    }
  });
  var $main= $('#flow_container');
  $main.masonry({
    itemSelector : '.box', //子类元素选择器
    isAnimated:true, //使用jquery的布局变化，是否启用动画效果
    animationOptions:{
      queue: false, duration: 500
    },
    isResizableL:false,// 是否可调整大小
    isRTL : false//使用从右到左的布局
  });
});

