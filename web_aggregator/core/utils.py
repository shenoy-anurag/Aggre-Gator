from web_aggregator.common.constants import PUBLISHER_FOX, PUBLISHER_CNN, SOURCES, DEFAULT_DESCRIPTION_LENGTH


def convert_categories(categories, mappings, sources):
    converted_categories = dict([(source, []) for source in sources])
    for cat in categories:
        if cat in mappings:
            for source in SOURCES:
                converted_categories[source].append(mappings[cat][source])
    return converted_categories


def convert_sources(sources):
    converted_sources = []
    if 'CNN' in sources:
        converted_sources.append(PUBLISHER_CNN)
    if 'FOX' in sources:
        converted_sources.append(PUBLISHER_FOX)
    return converted_sources


def truncate_descriptions(articles):
    for i in range(len(articles)):
        if len(articles[i]["article"]) > DEFAULT_DESCRIPTION_LENGTH + 1:
            articles[i]["description"] = articles[i]["article"][:DEFAULT_DESCRIPTION_LENGTH] + "..."
        else:
            articles[i]["description"] = articles[i]["article"] + "..."
        articles[i].pop("article")
    return articles
