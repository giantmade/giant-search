from django.db.models import QuerySet

from search.utils import is_page_title


class SearchableMixin:
    @classmethod
    def get_search_queryset(cls) -> QuerySet:
        """
        Override this method to provide your own Queryset to be indexed.
        For example, for some models, you might use cls.objects.published() or apply filters etc.

        This is a class method as we won't have an instance of the model when registering it with search.
        """

        return cls.objects.all()

    @staticmethod
    def get_search_fields() -> tuple:
        """
        Override this method to provide a tuple containing the fields to search.
        If the method returns an empty tuple, all text fields will be indexed as per Watson's defaults.
        """

        return tuple()

    @property
    def is_searchable(self):
        """
        This always needs to return True in order for the model that implements this Mixin to be searchable.
        """

        return True

    @property
    def search_result_title(self) -> str:
        """
        By default, search_result_title will return the string representation of the model as defined in __str__.
        Override this property to provide a different search result title.
        """

        # If the model is a Django CMS Page Title model use the title field.
        # TODO move this back to adapter.py since it will try to call methods that Title doesn't have :(
        if self._is_page_title():
            return self.title

        # If the model is a Django CMS Plugin model, we can try to get the Page title.
        if self._is_cms_plugin():
            try:
                return self.page.get_page_title()
            except AttributeError:
                pass

        # Finally, just try to return the string representation of the model.
        return str(self)

    @property
    def search_result_description(self) -> str:
        """
        By default, search_result_description returns an empty string. If you want to define a description, for example
        if your model has a description field, you could override search_result_description to provide it.
        """

        if self._is_page_title():
            return self.meta_description or ""

        return ""

    @property
    def search_url(self):
        """
        Define how to get the URL that the search result should point to.

        By default, we attempt to call get_absolute_url on the object. If your model doesn't implement this method, or
        needs something more complex, you must override this property method.
        """

        # If the model is a Django CMS Page Title model or a Plugin, try to get the URL from the Page.
        if self._is_page_title() or self._is_cms_plugin():
            try:
                return self.page.get_absolute_url()
            except AttributeError:
                pass

        # One last try to get the URL.
        try:
            return self.get_absolute_url()
        except AttributeError:
            pass

        # Fallback to returning an empty string since the URL field on the SearchResult model is not nullable. Note that
        # we will filter out any search results that don't have a valid URL because they're a bit pointless.
        return ""

    @property
    def search_result_category(self) -> str:
        """
        By default, the search result category is the human readable name of the Model, but of course, you can override
        this by overriding this property method on your model.

        If this Model is a Django CMS Title instance, we tell a lie and say that it is a Page because that makes more
        sense for end users.
        """

        if is_page_title():
            # Use "Page" instead of "Title" for CMS Title objects.
            return "Page"

        return self._meta.object_name
