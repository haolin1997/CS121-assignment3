from django.conf import settings

SEARCH_RESULTS_PER_PAGE = getattr(
    settings, 'SEARCH_RESULTS_PER_PAGE', 10)

SEARCH_MAX_PAGES = getattr(settings, 'SEARCH_MAX_PAGES', 10)
