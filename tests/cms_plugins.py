from django.contrib import admin

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .models import VacancyCard, VacancyCardsPlugin


class VacancyInline(admin.TabularInline):
    model = VacancyCard
    autocomplete_fields = ["vacancy"]
    max_num = 5
    extra = 1
    fk_name = "plugin"


@plugin_pool.register_plugin
class VacancyCardsContainerPlugin(CMSPluginBase):
    model = VacancyCardsPlugin
    name = "Vacancy Cards"
    render_template = "plugins/vacancy_cards.html"
    inlines = [VacancyInline]
    filter_horizontal = ["tags"]

    def render(self, context, instance, placeholder):
        """
        Override the default render to allow the user to set a custom number of
        vacancies to be shown
        """
        context = super().render(context, instance, placeholder)
        vacancies = instance.get_vacancies()
        current_vacancy = context.get("vacancy")

        if current_vacancy:
            vacancies.exclude(pk=current_vacancy.pk)

        if selected_vacancy_cards := instance.plugin_cards.all():
            vacancies = [card.vacancy for card in selected_vacancy_cards]

        context.update({"vacancies": vacancies[: instance.vacancy_count]})
        return context
