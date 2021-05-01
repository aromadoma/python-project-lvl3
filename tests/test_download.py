import os.path
import tempfile
from page_loader.loader import download


def test_download():
    print(os.getcwd())
    url = 'https://help.hexlet.io/ru'
    with tempfile.TemporaryDirectory() as td:
        download(url, td)
        with open(os.path.join(os.path.dirname(__file__), 'fixtures/result.html')) as f:
            expected_result = f.read()
        with open(os.path.join(td, 'help-hexlet-io-ru.html')) as f:
            result = f.read()

    assert result == expected_result


if __name__ == "__main__":
    test_download()
