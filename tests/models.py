from django.db import models
from django.db.models import Q
from django.utils import timezone

from cms.models import CMSPlugin, PlaceholderField

from giant_search.mixins import SearchableMixin


class TimestampMixin(models.Model):
    """
    Helper mixin to add a created at and updated field to a model
    """

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishingQuerySetMixin(models.QuerySet):
    """
    Helper mixin to filter news articles which are published and
    whose date is less than the current date
    """

    def published(self, user=None):
        """
        Return the published queryset, or all if user is admin
        """
        if user and user.is_staff:
            return self.all()

        return self.filter(is_published=True, publish_at__lte=Now())


class PublishingMixin(TimestampMixin):
    """
    Helper mixin to add the following fields: is_published, publish_date,
    title, slug
    """

    is_published = models.BooleanField(
        default=False, help_text="Selecting this option will publish this item"
    )
    publish_at = models.DateTimeField(null=True, blank=True, default=timezone.now)

    class Meta:
        abstract = True


class Vacancy(PublishingMixin):
    """
    Stores information about a Vacancy object.
    """

    position = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    hours = models.CharField(
        max_length=12, choices=(("full_time", "Full-Time"), ("part_time", "Part-Time"))
    )
    description = models.TextField()
    category = models.CharField(max_length=30, blank=True)
    content = PlaceholderField("vacancy_content")

    objects = PublishingQuerySetMixin.as_manager()

    def __str__(self):
        return f"{self.hours} vacancy for {self.position}"

    class Meta:
        verbose_name_plural = "Vacancies"
        verbose_name = "Vacancy"

    def get_absolute_url(self):
        """
        Attempt to retrieve the URLMixin absolute url, if not found, return the detail view for the
        vacancy.
        """
        detail_url = reverse("vacancies:detail", kwargs={"slug": self.slug})
        return super().get_absolute_url() or detail_url


class VacancyCardsPlugin(CMSPlugin):
    """
    Model for the vacancy card plugin
    """
    title = models.CharField(max_length=255, blank=True)
    vacancy_count = models.IntegerField(default=3)
    category = models.CharField(max_length=30, blank=True)

    def __str__(self):
        return f"Vacancy cards: {self.title}"

    def copy_relations(self, oldinstance):
        """
        Copy the relations from oldinstance and update the plugin field
        """

        for item in oldinstance.plugin_cards.all():
            item.pk = None
            item.plugin = self
            item.save()

    @property
    def filter_query(self) -> Q:
        """
        Builds the Q query object to use for filtering vacancies.
        """
        query = Q()

        if self.category:
            query &= Q(category=self.category)

        return query

    def get_vacancies(self):
        """
        Return a queryset based on what the user chooses on the frontend
        """
        queryset = Vacancy.objects.published()

        if query := self.filter_query:
            queryset = queryset.filter(query)

        return queryset


class VacancyCard(SearchableMixin, models.Model):
    """
    A model for an individual vacancy card plugin
    """

    vacancy = models.ForeignKey(
        to=Vacancy,
        related_name="vacancy_cards",
        verbose_name="Vacancy",
        on_delete=models.CASCADE,
        limit_choices_to={"is_published": True},
        null=True,
        blank=True,
    )

    plugin = models.ForeignKey(
        to=VacancyCardsPlugin, on_delete=models.CASCADE, related_name="plugin_cards",
    )

    def __str__(self):
        return f"Vacancy card: {self.vacancy}"

    @staticmethod
    def get_search_fields() -> tuple:
        return ('vacancy__position', 'vacancy__slug', 'vacancy__description')

    def get_absolute_url(self) -> str:
        page = getattr(self.plugin, "page", None)
        if page:
            try:
                return page.get_public_url()
            except AttributeError:
                pass
        return ""

    def get_search_result_title(self) -> str:
        return self.vacancy and self.vacancy.position or ""

    def get_search_result_description(self) -> str:
        return self.vacancy.__str__()

    def get_search_result_category(self) -> str:
        return "Vacancy"
