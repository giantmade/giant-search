from watson import search as watson
from watson.views import SearchView as WatsonSearchView


class SearchView(WatsonSearchView):
    template_name = "watson/search_results.html"

    def get_queryset(self):
        return watson.search(self.query, models=self.get_models())
