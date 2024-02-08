from django.apps import AppConfig
from watson import search as watson

from search.adapter import GiantSearchAdapter


class SearchAppConfig(AppConfig):
    name = "search"

    def ready(self) -> None:
        # Get a list of all models that implement the SearchableMixin?
        for app in self.apps.all_models.values():
            for model in app.values():
                if hasattr(model, "is_searchable"):
                    # We have search_fields, try to register the model.
                    register_kwargs = {
                        "model": model.get_search_queryset(),
                        "adapter_cls": GiantSearchAdapter,
                    }

                    # If the Model's Meta class has defined search_fields, pass them to the register method.
                    try:
                        register_kwargs["fields"] = model.Meta.search_fields
                    except AttributeError:
                        pass

                    # Now we register this Model with the kwargs built up from above.
                    watson.register(**register_kwargs)

        # Register Page Titles
        from cms.models import Title
        watson.register(Title.objects.filter(publisher_is_draft=False), adapter_cls=GiantSearchAdapter)
