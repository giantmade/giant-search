from django.apps import AppConfig

from giant_search.utils import register_for_search


class GiantSearchAppConfig(AppConfig):
    name = "giant_search"

    def ready(self) -> None:
        # Get a list of all models that implement the SearchableMixin?
        for app in self.apps.all_models.values():
            for model in app.values():
                if hasattr(model, "is_searchable"):
                    # We have search_fields, try to register the model.
                    register_kwargs = {"model": model.get_search_queryset()}

                    # If the model defines which fields should be searchable, pass them to the register() call.
                    try:
                        search_fields = model.get_search_fields()
                        if search_fields:
                            register_kwargs["fields"] = search_fields
                    except AttributeError:
                        pass

                    # Now we register this Model with the kwargs built up from above.
                    register_for_search(**register_kwargs)

        # Register Page Titles
        try:
            from cms.models import Title

            register_for_search(
                Title.objects.filter(published=True, publisher_is_draft=False)
            )
        except ImportError:
            from cms.models import PageContent
            from cms.utils import get_current_site
            from cms.utils.i18n import get_public_languages

            site = get_current_site()
            languages = get_public_languages(site_id=site.pk)
            register_for_search(PageContent.objects.filter(language__in=languages))
