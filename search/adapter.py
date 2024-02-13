import json

from django.core.serializers.json import DjangoJSONEncoder
from watson.search import SearchAdapter


class GiantSearchAdapter(SearchAdapter):
    """
    This adapter allows us to define how we populate the title, description, URL and other fields on the Watson
    SearchResult instances.

    Each method assumes that the model set on this Adapter class implements the SearchableMixin.
    """

    def get_title(self, obj):
        """
        Returns the title of this search result.
        This is given high priority in search result ranking.

        You can access the title of the search entry as `entry.title` in your search results.
        """

        return obj.search_result_title[:1000]

    def get_description(self, obj):
        """
        Returns the description of this search result.
        This is given medium priority in search result ranking.

        You can access the description of the search entry as `entry.description`
        in your search results. Since this should contains a short description of the search entry,
        it's excellent for providing a summary in your search results.
        """

        return obj.search_result_description

    def get_url(self, obj):
        """
        Get the URL of this search result.
        """

        return obj.search_url

    def serialize_meta(self, obj):
        """
        Implement the serialize_meta method in order to get some useful information about our search result and put it
        into the search result object for use on the front end.

        If you want to add some data here, please ensure that you update the SearchableMixin to provide a default
        value for it.
        """

        meta_obj = {"category": obj.search_result_category}
        return json.dumps(meta_obj, cls=DjangoJSONEncoder)
