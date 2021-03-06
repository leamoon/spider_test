import requests
import re
import random
from lxml import etree

user_agent = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]
header = {"User-Agent": random.choice(user_agent)}
HOST = 'http://www.biquges.com'


def search_novel(book_name):
    search_url = 'http://www.biquges.com/modules/article/search.php'
    data_form = {'searchkey': book_name}
    res_search = requests.post(url=search_url, data=data_form, headers=header)
    res_search.encoding = "utf-8"
    temp1 = etree.HTML(res_search.text)
    result_search = temp1.xpath('//td[@class="odd"]//a/@href')[0]
    book_search_url = HOST + result_search
    return book_search_url


def novel_download(book_url):
    response = requests.get(book_url, headers=header)
    response.encoding = 'utf-8'
    data = etree.HTML(response.text)
    bookname = data.xpath("//*[@id='info']/h1/text()")[0]
    chapter_links = []
    for link in data.xpath("//*//dd//a/@href")[9:]:
        chapter_links.append(HOST + link)
    save_path = '{}.txt'.format(bookname)

    with open(save_path, 'w+', encoding="utf-8") as f:
        # 从存放小说章节地址的列表中依次去除小说地址，让requests通过get方法去取货
        for x in chapter_links:
            # 向小说章节所在地址发送请求并获得响应
            res = requests.get(x, headers=header)
            res.encoding = 'utf-8'
            result = etree.HTML(res.text)
            title = result.xpath('//*[@class="bookname"]/h1/text()')[0]
            contents = result.xpath('//div[@id="content"]/text()')
            for content in contents:
                content = re.sub('\xa0\xa0\xa0\xa0', ' ', content)

            f.write('\n\n' + title + '\n\n')
            f.flush()
            for content in contents:
                f.write(content)

            print('\r{}\t{}%\t{}'.format(bookname, format(100 * chapter_links.index(x) / len(chapter_links), '.2f'),
                                         title), end='')


book = input('Book_name：')
print('Download started!')
novel_download(search_novel(book))
print('Download successfully')
