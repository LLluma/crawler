from ..crawler import get_page, parse_page, to_relative
from unittest import mock


PAGE = '''
<html>
    <body>
        <a href="http://lib.ru/books/prose/">Prose</a>
        <a href="http://lib.ru/poem/">Poem</a>
        <a href="/books/hello/world/">Related Link</a>
        <a href="http://linux.org.ru/linux/">Linux</a>
    </body>
</html>
'''

@mock.patch('crawler.crawler.requests')
def test_get_page(requests_mock):
    url = 'http://lib.ru/FOUNDATION/'
    page = get_page(url)
    requests_mock.assert_called()
    requests_mock.assert_called_with(url)


def test_to_relative():
    base_url='http://lib.ru/books/'
    assert to_relative('http://lib.ru/books/1.html', base_url) == '1.html'
    assert to_relative('http://lib.ru/books/1.html', base_url[:-1]) == '1.html'
    assert not to_relative('http://linux.ru/books/1.html', base_url)
    assert not to_relative('http://lib.ru/hello/1.html', base_url)
    assert to_relative('http://lib.ru/books/hello/1.html', base_url) == 'hello/1.html'
    assert to_relative('/books/hello/1.html', base_url) == 'hello/1.html'


def test_parse_page():
    base_url='http://lib.ru/books/'
    parsed_page, urls = parse_page(PAGE, base_url)
    assert '<html>' in parsed_page
    assert '</html>' in parsed_page
    assert '<a href="prose">Prose</a>' in parsed_page
    assert '<a href="hello/world">Related Link</a>' in parsed_page
