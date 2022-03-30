import logging

from web_aggregator.core.models import fetch_settings
from web_aggregator.elastic.search import search_query_with_or_filters
from web_aggregator.common.constants import ES_INDEX_NAME, CATEGORIES, CATEGORY_MAPPINGS
from web_aggregator.core.utils import convert_categories, convert_sources

logger = logging.getLogger(__name__)


def fetch_categories():
    try:
        settings = fetch_settings()
        if settings:
            return {'categories': settings['categories']}
        else:
            return {
                'categories': CATEGORIES}
    except Exception as e:
        logger.error(e)
        return None


def fetch_es_articles(categories, sources, years):
    filters = {'filters': [], 'rangeFilters': []}
    # publishers = convert_sources(sources)
    publishers = sources
    converted_categories = convert_categories(categories, CATEGORY_MAPPINGS, publishers)
    converted_categories = [c for cat in list(converted_categories.values()) for c in cat]
    category_filters = {'field': 'topic', 'values': converted_categories}
    filters['filters'].append(category_filters)
    results = search_query_with_or_filters(index=ES_INDEX_NAME, filters=filters, publishers=publishers)
    return results
