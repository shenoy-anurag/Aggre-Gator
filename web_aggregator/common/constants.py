# API:
API_STATUS_SUCCESS = 'Success'
API_STATUS_PARTIAL = 'Partial'
API_STATUS_FAILURE = 'Failure'
API_STATUS_WARNING = 'Warning'
API_STATUS_ERROR = 'Error'

# Publishers
PUBLISHER_CNN = "CNN"
PUBLISHER_FOX = "FOX_NEWS"
# main site map of all CNN years
site_map_url_cnn = "https://us.cnn.com/sitemap.html"
site_map_url_fox = "https://www.foxnews.com/sitemap.xml"

# CNN standard starting url
cnn_url = "https://us.cnn.com"
fox_news_url = "https://www.foxnews.com"

# hardcoded bias [-1, +1] -1 indicates extreme left leaning, +1 indicates extreme right leaning
CNN_bias = -0.5
FOX_bias = +0.5

# FOX News
FOX_NEWS_start_unix_timestamp = 1640796958000  # Timestamp which is 2021-12-29 11:58:36
FOX_NEWS_next_unix_timestamp = 1645752463000
FOX_NEWS_QUERY_ARGS = {'type': 'articles', 'from': FOX_NEWS_start_unix_timestamp}

SOURCES = [PUBLISHER_CNN, PUBLISHER_FOX]

CATEGORY_MAPPINGS = {
    'Health': {PUBLISHER_CNN: 'Health', PUBLISHER_FOX: 'health'},
    'Politics': {PUBLISHER_CNN: 'Politics', PUBLISHER_FOX: 'politics'},
    'Technology': {PUBLISHER_CNN: 'Tech', PUBLISHER_FOX: 'tech'},
    'Sports': {PUBLISHER_CNN: 'Sports', PUBLISHER_FOX: 'sports'},
    'US': {PUBLISHER_CNN: 'US', PUBLISHER_FOX: 'us'},
    'World': {PUBLISHER_CNN: 'World', PUBLISHER_FOX: 'world'},
    'Business': {PUBLISHER_CNN: 'Business', PUBLISHER_FOX: 'world'},
    'Entertainment': {PUBLISHER_CNN: 'Entertainment', PUBLISHER_FOX: 'entertainment'},
    'Travel': {PUBLISHER_CNN: 'Travel', PUBLISHER_FOX: 'travel'},
    'Opinion': {PUBLISHER_CNN: 'Opinion', PUBLISHER_FOX: 'special'},
    'Person': {PUBLISHER_CNN: '', PUBLISHER_FOX: 'person'},
    'Food': {PUBLISHER_CNN: '', PUBLISHER_FOX: 'food-drink'},
    'Lifestyle': {PUBLISHER_CNN: '', PUBLISHER_FOX: 'lifestyle'},
    'Media': {PUBLISHER_CNN: '', PUBLISHER_FOX: 'media'},
    'Shows': {PUBLISHER_CNN: '', PUBLISHER_FOX: 'shows'},
}

CATEGORIES = [
    'US', 'World', 'Politics', 'Technology', 'Business', 'Health', 'Entertainment', 'Travel', 'Science', 'Sports'
]

# to change based on what years you want to analyze
selected_years = {"2022"}

ES_INDEX_NAME = 'articles'

# topics from https://cnn.com/article/sitemap-2022.html
# topics = {
#     "Politics", "Opinion", "US", "Asia", "Middle East", "Election Center 2016", "China", "Economy", "Business", "Tech",
#     "Health", "World", "Africa"
# }
# topics = [
#     "Health", "US", "Opinion", "Arts", "Politics", "China", "Asia", "Travel", "World", "Business", "Economy",
#     "Entertainment", "Africa", "Tech", "Weather", "Investing", "Media", "CNN Underscored", "Perspectives", "India",
#     "Americas", "Design", "Travel-stay", "Travel - News", "Architecture", "Fashion", "Energy", "Cars", "Success",
#     "Beauty", "App News Section", "Movies", "CNN 10", "Luxury", "Business - Food", "Food and Drink", "Travel-play",
#     "Middle East", "Homes", "Celebrities"
# ]
topics = {
    'Opinion', 'Perspectives', 'Travel-play', 'Fashion', 'Cars', 'Economy', 'CNN 10', 'Africa', 'China', 'Asia',
    'Business', 'Tech', 'Movies', 'World', 'Success', 'App News Section', 'Food and Drink', 'Business - Food', 'India',
    'Design', 'Weather', 'Travel-stay', 'Luxury', 'Investing', 'Arts', 'Celebrities', 'Homes', 'US', 'Travel',
    'Entertainment', 'Energy', 'Media', 'Travel - News', 'Architecture', 'Middle East', 'Health', 'Beauty', 'Americas',
    'CNN Underscored', 'Politics'
}

# Frontend
DEFAULT_PAGE = 1
DEFAULT_PER_PAGE = 100
DEFAULT_DESCRIPTION_LENGTH = 250  # number of characters.
