from django.db.models import QuerySet


class SearchableMixin:
    @classmethod
    def get_search_queryset(cls) -> QuerySet:
        """
        Override this method to provide your own Queryset to be indexed.
        For example, for some models, you might use cls.objects.published() or apply filters etc.

        You must not change cls to self as we won't have an instance of the model when registering it with search.
        """

        return cls.objects.all()

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

        return str(self)

    @property
    def search_result_description(self) -> str:
        """
        By default, search_result_description returns an empty string. If you want to define a description, for example
        if your model has a description field, you could override search_result_description to provide it.
        """

        return ""

    @property
    def search_url(self):
        """
        Define how to get the URL that the search result should point to.

        By default, we attempt to call get_absolute_url on the object. If your model doesn't implement this method, or
        needs something more complex, you can override this property method.
        """

        try:
            return self.get_absolute_url()
        except AttributeError:
            return ""
