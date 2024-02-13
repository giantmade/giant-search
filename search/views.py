from watson.views import SearchView as WatsonSearchView


class SearchView(WatsonSearchView):
    template_name = "search/results.html"

    def get_queryset(self):
        q = super().get_queryset()
        return q
