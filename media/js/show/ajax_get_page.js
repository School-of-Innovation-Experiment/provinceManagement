$(function(){
  var $container = $('#flow_container');
  $container.imagesLoaded(function(){
    $container.masonry({
      itemSelector: '.box',
      isAnimatedFromBottom:true,
      columnWidth: 100
    });
  });
  $container.infinitescroll({
    navSelector  : 'div#page-nav',    // selector for the paged navigation
    nextSelector : 'div#page-nav a',  // selector for the NEXT link (to page 2)
    itemSelector : '.box',     // selector for all items you'll retrieve
    animate: true,
    loading: {
      msgText: "<em>正在载入...</em>",
      finishedMsg: '已是全部内容',
      // img: 'http://i.imgur.com/6RMhx.gif'
      img: '/static/images/loading-black.gif'
    } // trigger Masonry as a callback
  }, function( newElements ) {
    // hide new items while they are loading
    var $newElems = $( newElements ).css({ opacity: 0 });
    // ensure that images load before adding to masonry layout
    // $("#page-nav").html($(newElements).find("#page-nav").html());
    $newElems.imagesLoaded(function(){
      // show elems now they're ready
      $newElems.animate({ opacity: 1 });
      $container.masonry( 'appended', $newElems, true );
      // $container.masonry('reload');
    });
  });
});
