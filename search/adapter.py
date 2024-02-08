from watson.search import SearchAdapter


class GiantSearchAdapter(SearchAdapter):
    """
    This adapter allows us to define how we populate the title, description, URL and in future, other fields on the
    Watson search results. You generally won't need to modify this unless we add a new model type that can't be handled
    within our own code (the Title model from Django CMS, for example)
    """

    def get_title(self, obj):
        """
        Returns the title of this search result.
        This is given high priority in search result ranking.

        You can access the title of the search entry as `entry.title` in your search results.
        """

        # If the model is a Django CMS Page Title model, we deal with getting the title here.
        from cms.models import Title
        if isinstance(obj, Title):
            return obj.title

        # Get the title from the object's search_result_title property defined on the model.
        return obj.search_result_title[:1000]

    def get_description(self, obj):
        """
        Returns the description of this search result.
        This is given medium priority in search result ranking.

        You can access the description of the search entry as `entry.description`
        in your search results. Since this should contains a short description of the search entry,
        it's excellent for providing a summary in your search results.
        """

        # If the model is a Django CMS Page Title model, we deal with getting the description here.
        from cms.models import Title
        if isinstance(obj, Title):
            return obj.meta_description or ""

        # Get the description from the object's search_result_description property defined on the model.
        return obj.search_result_description

    def get_url(self, obj):
        """
        Get the URL of this search result.
        """

        # If the model is a Django CMS Page Title model, we deal with getting the URL here.
        from cms.models import Title
        if isinstance(obj, Title):
            return obj.page.get_absolute_url()

        # Get the URL from the object's search_url property defined on the model.
        return obj.search_url

