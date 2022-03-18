import datetime

from .setup import elasticsearch_obj, logger, get_or_create_es_client


def create_index(index_name, settings: dict = None, mappings=None):
    elasticsearch_obj = get_or_create_es_client()
    logger.debug("Index Name: {index}".format(index=index_name))
    created = False
    # index settings
    body = {}
    if settings:
        body['settings'] = settings
    if mappings:
        body['mappings'] = mappings

    print(body)

    try:
        if not elasticsearch_obj.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            elasticsearch_obj.indices.create(index=index_name, ignore=400, body=body)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_single_document(index, document_data, doc_id=None, metadata=None):
    elasticsearch_obj = get_or_create_es_client()
    logger.debug("Index: {index}, Document ID: {doc_id}, \nDocument: {doc}, \nMetadata: {metadata}".format(
        index=index,
        doc_id=doc_id,
        doc=document_data,
        metadata=metadata)
    )
    body = {}
    if document_data:
        body.update(document_data)
    if metadata:
        body.update(metadata)

    doc_created = False
    try:
        if doc_id:
            elasticsearch_obj.index(index=index, id=doc_id, body=body)
            response = None
        else:
            response = elasticsearch_obj.index(index=index, body=body)
        doc_created = True
        return doc_created, response
    except Exception as e:
        logger.error(e)
    finally:
        return doc_created, None


# TODO: Edit document function needs to be written.

def delete_single_document_by_id(index, doc_id):
    elasticsearch_obj = get_or_create_es_client()
    doc_updated = False
    try:
        response = elasticsearch_obj.delete(index=index, id=doc_id)
        doc_updated = True
        return doc_updated, response
    except Exception as e:
        print(e)
        return doc_updated, None


def update_documents_by_query(index, body, params=None):
    elasticsearch_obj = get_or_create_es_client()
    docs_updated = False
    try:
        response = elasticsearch_obj.update_by_query(index=index, body=body, params=params)
        docs_updated = True
        return docs_updated, response
    except Exception as e:
        print(e)
        return docs_updated, None


def delete_documents_by_query(index, body, params=None):
    docs_deleted = False
    try:
        response = elasticsearch_obj.delete_by_query(index=index, body=body, params=params)
        docs_deleted = True
        return docs_deleted, response
    except Exception as e:
        print(e)
        return docs_deleted, None


# Articles Index:
def create_articles_index(es_object, index_name='articles'):
    elasticsearch_obj = get_or_create_es_client()
    logger.debug("Index Name: {index}".format(index=index_name))
    created = False
    fields = [
        'type', 'publisher', 'url', 'title', 'article', 'bias', 'topic', 'tags', 'year', 'month', 'day',
        'creation_date', 'character_length', 'comments'
    ]
    # index settings
    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0
        },
        "mappings": {
            "properties": {
                "type": {
                    "type": "text"
                },
                "publisher": {
                    "type": "text"
                },
                "url": {
                    "type": "text"
                },
                "title": {
                    "type": "search_as_you_type"
                },
                "article": {
                    "type": "text"
                },
                "bias": {
                    "type": "text"
                },
                "topic": {
                    "type": "text"
                },
                "tags": {
                    "type": "text"
                },
                "year": {
                    "type": "integer"
                },
                "month": {
                    "type": "integer"
                },
                "day": {
                    "type": "integer"
                },
                "creation_date": {
                    "type": "date"
                },
                "character_length": {
                    "type": "integer"
                },
                "comments": {
                    "type": "text"
                },
                # Metadata fields:
                "added_by": {
                    "type": "text"
                },
                "added_on": {
                    "type": "date"
                },
            }
        }
    }
    print(settings)

    try:
        if not es_object.indices.exists(index_name):
            # Ignore 400 means to ignore "Index Already Exist" error.
            es_object.indices.create(index=index_name, ignore=400, body=settings)
            print('Created Index')
        created = True
    except Exception as ex:
        print(str(ex))
    finally:
        return created


def store_single_article_document_with_set_id(index, document_index, document_data, metadata):
    elasticsearch_obj = get_or_create_es_client()
    logger.debug("Index: {index}, Document: {doc}, Metadata: {metadata}".format(
        index=index, doc=document_data, metadata=metadata)
    )
    article_doc = {}

    fields = [
        'type', 'publisher', 'url', 'title', 'article', 'bias', 'topic', 'tags', 'year', 'month', 'day',
        'creation_date', 'character_length', 'comments'
    ]

    article_doc.update(document_data)
    article_doc["added_by"] = metadata.get('added_by', '')
    article_doc["added_on"] = metadata.get('added_on', datetime.datetime.now())
    logger.debug("The document being written: {}".format(article_doc["url"]))

    doc_created = False
    if article_doc.get('title') is not None:
        try:
            elasticsearch_obj.index(index=index, id=document_index, body=article_doc)
            doc_created = True
        except Exception as e:
            logger.error(e)
        finally:
            return doc_created
    return "Article Is Null"


def store_single_article_document_with_auto_id(index, document_data, metadata):
    elasticsearch_obj = get_or_create_es_client()
    logger.debug("Index: {index}, Document: {doc}, Metadata: {metadata}".format(
        index=index, doc=document_data, metadata=metadata)
    )
    article_doc = {}

    fields = [
        'type', 'publisher', 'url', 'title', 'article', 'bias', 'topic', 'tags', 'year', 'month', 'day',
        'creation_date', 'character_length', 'comments'
    ]

    article_doc.update(document_data)
    article_doc["added_by"] = metadata.get('added_by', '')
    article_doc["added_on"] = metadata.get('added_on', datetime.datetime.now())
    logger.debug("The document being written: {}".format(article_doc["url"]))

    doc_created = False
    try:
        response = elasticsearch_obj.index(index=index, body=article_doc)
        doc_created = True
        return doc_created, response
    except Exception as e:
        logger.error(e)
        return doc_created, None


def edit_single_document_using_id(index, doc_id, document_data: dict, metadata: dict):
    elasticsearch_obj = get_or_create_es_client()
    # logger.debug("Index: {index}, Document: {doc}, Metadata: {metadata}".format(
    #     index=index, doc=document_data, metadata=metadata)
    # )
    document_data.update(metadata)
    doc_updated = False
    try:
        response = elasticsearch_obj.update(index=index, id=doc_id, body={"doc": document_data})
        doc_updated = True
        return doc_updated, response
    except Exception as e:
        logger.error(e)
        return doc_updated, None


def save_articles_es(article_objs, metadata):
    for i in range(len(article_objs)):
        try:
            article = article_objs[i]
            article_doc = article.create_mongo_document()
            store_single_article_document_with_auto_id(index='articles', document_data=article_doc, metadata=metadata)
        except Exception as e:
            logger.error(e)