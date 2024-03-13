from django.conf import settings

from watson.views import SearchView as WatsonSearchView

from giant_search.utils import SearchResultDeduplicator


class SearchView(WatsonSearchView):
    template_name = "search/results.html"
    paginate_by = getattr(settings, 'GIANT_SEARCH_PAGINATE_BY', 10)

    def get_queryset(self):
        queryset = super().get_queryset().exclude(url="")
        return SearchResultDeduplicator(queryset).deduplicate()
