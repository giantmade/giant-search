from cms.api import create_page
from cms.models.placeholdermodel import Placeholder
from django.test import TestCase
from django.utils.translation import get_language
from watson.search import SearchEngine

from giant_search.utils import SearchResultProcessor

from .models import Vacancy, VacancyCard, VacancyCardsPlugin


class TestSearchPublished(TestCase):

    def _test_get_queryset(self, publish=0):
        # scan placeholders
        page = create_page('Test Page', 'template.html', get_language())
        v1 = Vacancy.objects.create(
            position='Senior Python Developer',
            slug='senior-python-developer',
            hours=36,
            description='Django, DevOps',
            category='python',
        )
        vcp = VacancyCardsPlugin.objects.create(
            title='Backend Developers', vacancy_count=10, category='backend', placeholder=Placeholder.objects.first()
        )
        vc1 = VacancyCard.objects.create(vacancy=v1, plugin=vcp)
        if publish:
            published = page.publish(get_language())
            assert published

        search_engine = SearchEngine.get_created_engines()[0][1]
        results = search_engine.search('python')
        assert len(results) == 1
        assert results[0].title == 'Senior Python Developer'

        queryset = SearchResultProcessor(results).exclude_unpublished_items()
        # conflating bool and int
        assert len(queryset) == publish

    def test_published(self):
        self._test_get_queryset(1)

    def test_unpublished(self):
        self._test_get_queryset()
