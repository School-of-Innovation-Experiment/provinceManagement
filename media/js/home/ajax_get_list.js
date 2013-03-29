function news_turn_page(page){$('#news-list').html(page.html); turn_page();};
function docs_turn_page(page){$('#docs-list').html(page.html); turn_page();};
function turn_page () {
  var ids = ["#docs-previous-page", "#docs-next-page", "#news-previous-page", "#news-next-page"];
  for(var tagid in ids) {
    tagid = ids[tagid];
    if(tagid.indexOf('docs') >= 0)
      $(tagid).attr('onclick',
                    "Dajaxice.news.docs_turn_page(docs_turn_page, {'docs_page': "
                    + $(tagid).attr("arg") + "}); return false;");
    else
      $(tagid).attr('onclick',
                    "Dajaxice.news.news_turn_page(news_turn_page, {'news_page': "
                    + $(tagid).attr("arg") + "}); return false;");
  };
};
function getinput (tag) {
  return $(tag).attr('value');
}
function search () {
  var ids = ["#search-news", "#search-docs"];
  for(var tagid in ids) {
    tagid = ids[tagid];
    if(tagid.indexOf('docs') >= 0)
      $(tagid).attr('onclick',
                    "Dajaxice.news.docs_search_page(docs_turn_page, {'docs_input': getinput('#docs-search-input')}); return false;");
    else
      $(tagid).attr('onclick',
                    "Dajaxice.news.news_search_page(news_turn_page, {'news_input': getinput('#news-search-input')}); return false;");
  };
};
window.onload= function () {
  turn_page();
  search();
};
