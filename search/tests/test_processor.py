from unittest.mock import Mock

import pytest

from search.processor import SearchResultProcessor


@pytest.fixture
def search_result_processor():
    return SearchResultProcessor(results=None)


class TestProcessor:
    def test_is_valid_url_no_url(self, search_result_processor):
        assert search_result_processor._is_valid_url(None) is False

    def test_is_valid_url_in_seen(self, search_result_processor):
        search_result_processor.seen_urls = ["example/page"]
        assert search_result_processor._is_valid_url("/example/page/") is False

    def test_is_valid_url(self, search_result_processor):
        assert search_result_processor._is_valid_url("/example/page") is True

    def test_get_url_for_result_url_in_path(self):
        mock_search_result = Mock(["path"])
        mock_search_result.path = "/valid-test-path/"
        assert SearchResultProcessor._get_url_for_result(mock_search_result) == "/valid-test-path/"

    def test_get_url_for_result_url_in_result_object(self):
        mock_search_result = Mock(["object"])
        mock_search_result.object.get_absolute_url.return_value = "/valid-test-object-url/"
        assert (
            SearchResultProcessor._get_url_for_result(mock_search_result)
            == "/valid-test-object-url/"
        )

    def test_get_url_for_result_url_in_result_page_object(self):
        mock_search_result = Mock(["object"])
        mock_search_result.object = Mock(["page"])
        mock_search_result.object.page.get_absolute_url.return_value = (
            "/valid-test-object-page-url/"
        )
        assert (
            SearchResultProcessor._get_url_for_result(mock_search_result)
            == "/valid-test-object-page-url/"
        )
