import os

from web_aggregator import app
from web_aggregator.core.views import core_blueprint

app.register_blueprint(core_blueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5005, debug=True if os.environ.get('FLASK_DEBUG') == 1 else False)
