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

# to change based on what years you want to analyze
selected_years = {"2022"}

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
