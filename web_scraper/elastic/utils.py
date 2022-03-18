import json
from .setup import elasticsearch_obj


def get_index_mapping(index_name):
    mapping = elasticsearch_obj.indices.get_mapping(index=index_name)
    return mapping


def documents_from_search_results(search_results, scrolling=False, scroll=None):
    results = []
    if scrolling:
        scroll_ids = []
        scroll_ids.append(search_results['_scroll_id'])
        results.extend([doc['_source'] for doc in search_results['hits']['hits']])
        while True:
            res = elasticsearch_obj.scroll(scroll_id=scroll_ids[-1], scroll=scroll)
            if res:
                scroll_ids.append(res['_scroll_id'])
                if res['hits']['hits']:
                    results.extend([doc['_source'] for doc in res['hits']['hits']])
                else:
                    break
    return results
