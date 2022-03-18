import json
from .setup import elasticsearch_obj

import math

ARTICLE_FIELDS = fields = [
    'type', 'publisher', 'url', 'title', 'article', 'bias', 'topic', 'tags', 'year', 'month', 'day',
    'creation_date', 'character_length', 'comments'
]


def analyze_query(index, text, analyzer: str):
    body = {
        "analyzer": analyzer,
        "text": text
    }
    data = elasticsearch_obj.indices.analyze(body=body, index=index)
    return data


def show_all(index, scroll=None):
    body = {
        "size": 10000,
        "query": {
            "bool": {
                "must": {
                    "match_all": {}
                }
            }
        }
    }
    if scroll:
        data = elasticsearch_obj.search(index=index, body=body, scroll=scroll)
    else:
        data = elasticsearch_obj.search(index=index, body=body)
    return data


def show_all_publisher(index, doc_type, publisher):
    body = {
        "query": {
            "bool": {
                "must": {
                    "match_all": {}
                },
                "filter": {
                    "term": {
                        "publisher": publisher.lower()
                    }
                }
            }
        }
    }
    data = elasticsearch_obj.search(index=index, doc_type=doc_type, body=body)
    return data


def search_match_query(index, field, text):
    body = {
        "query": {
            "match": {
                field: {
                    "query": text
                }
            }
        }
    }
    data = elasticsearch_obj.search(index=index, body=body)
    return data


def search_default_with_filter(index, search_string, filter_field, text):
    body = {
        "query": {
            "bool": {
                "must": {
                    "query_string": {
                        "query": search_string
                    }
                },
                "filter": {
                    "term": {
                        filter_field: text.lower()
                    }
                }
            }
        }
    }
    data = elasticsearch_obj.search(index=index, body=body)
    return data


def search_default_publisher(index, search_string, publisher):
    body = {
        "query": {
            "bool": {
                "must": {
                    "query_string": {
                        "query": search_string
                    }
                },
                "filter": {
                    "term": {
                        "publisher": publisher.lower()
                    }
                }
            }
        }
    }
    data = elasticsearch_obj.search(index=index, body=body)
    return data


def create_elastic_search_text_filter(field: str, value: str):
    if len(value.split()) > 1:
        # Match query is case insensitive. Match Phrase is used for matching exact phrases.
        return {"match_phrase": {field: value}}
    else:
        # Term query expects a lower cased term.
        return {"term": {field: value.lower()}}


def search_query_with_filters(index, search_string, filters, publisher=None):
    # Filters is a list of dictionaries which contain the filter values.
    filter_list = []
    if publisher:
        filter_list.append({"term": {'publisher': publisher.lower()}})
    term_filters = filters.get('filters')
    if term_filters:
        for fltr in term_filters:
            key = fltr.get('field')
            values = fltr.get('values')
            for value in values:
                filter_list.append({"term": {key: value}})
    range_filters = filters.get('rangeFilters')
    if range_filters:
        for fltr in range_filters:
            key = fltr.get('field')
            values = fltr.get('values')
            for value in values:
                # value_id = value.get('id')
                start = value.get('start')
                end = value.get('end')
                filter_list.append({'range': {key: {'gte': start, 'lte': end}}})
    print(filter_list)
    body = {
        "size": 10000,
        "query": {
            "bool": {
                "must": {
                    "query_string": {
                        "query": search_string
                    }
                },
                "filter": filter_list
            }
        }
    }
    data = elasticsearch_obj.search(index=index, body=body)
    return data
