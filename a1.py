def test(news_list):
    for new in news_list:
        str_list = new.news_document.url.split('/')
        for i in range(len(str_list)):
            if str_list[i] == 'media':
                str_list = str_list[i+1:]
                break
        new.news_document = str('/'.join(str_list))
    return news_list
