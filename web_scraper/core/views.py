import datetime
import logging
import os
import traceback

from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity, create_refresh_token, get_jwt, get_jti
)
from flask_restful import Resource

from web_scraper import api, JWT_ACCESS_TOKEN_TIMEDELTA, JWT_REFRESH_TOKEN_TIMEDELTA
from web_scraper.celery_config.celery_tasks import scrape_cnn_articles, scrape_fox_articles
from web_scraper.common import mem_cache
from web_scraper.common.constants import API_STATUS_SUCCESS, API_STATUS_FAILURE, API_STATUS_ERROR

core_blueprint = Blueprint('core', __name__)

logger = logging.getLogger(__name__)


class Ping(Resource):
    def get(self):
        return jsonify({"message": "pong"})


class Login(Resource):
    def post(self):
        if not request.is_json:
            return jsonify({'status': API_STATUS_FAILURE, "msg": "Missing JSON in request"})

        username = request.json.get('username', None)
        password = request.json.get('password', None)
        try:
            if not username:
                return jsonify({'status': API_STATUS_FAILURE, "msg": "Missing username parameter"})
            if not password:
                return jsonify({'status': API_STATUS_FAILURE, "msg": "Missing password parameter"})

            if username != os.environ['JWT_USERNAME'] or password != os.environ['JWT_PASSWORD']:
                return jsonify({'status': API_STATUS_FAILURE, "msg": "Bad username or password"})

            # Identity can be any data that is json serializable
            access_token = create_access_token(identity=username, expires_delta=JWT_ACCESS_TOKEN_TIMEDELTA)
            refresh_token = create_refresh_token(identity=username, expires_delta=JWT_REFRESH_TOKEN_TIMEDELTA)
            return make_response(
                jsonify({'status': API_STATUS_SUCCESS, 'access_token': access_token, 'refresh_token': refresh_token}))
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            return make_response(jsonify({'status': API_STATUS_ERROR}))


class TokenRefresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        try:
            current_user = get_jwt_identity()
            access_token = create_access_token(identity=current_user, expires_delta=JWT_ACCESS_TOKEN_TIMEDELTA)
            return make_response(jsonify({'status': API_STATUS_SUCCESS, 'message': 'Access Token Generated',
                                          'access_token': access_token}), 200)
        except Exception as e:
            logger.error(e)
            return make_response(jsonify({'status': API_STATUS_ERROR, 'message': 'Something went wrong'}), 500)


# @app_jwt.token_in_blocklist_loader
# def check_if_token_in_blacklist(decrypted_token):
#     jti = decrypted_token['jti']
#     return jti in mem_cache.get_blacklisted_tokens()


class LogoutAccess(Resource):
    @jwt_required
    def post(self):
        try:
            jti = get_jti(get_jwt())
            logger.debug(jti)
            blacklisted_tokens = mem_cache.get_blacklisted_tokens()
            blacklisted_tokens.add(jti)
            mem_cache.set_blacklisted_tokens(blacklisted_tokens)
            return make_response(
                jsonify({'status': API_STATUS_SUCCESS, 'message': 'Access token has been revoked'}), 200)
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            return make_response(
                jsonify({'status': API_STATUS_ERROR, 'message': 'Something went wrong'}), 500)


class Protected(Resource):
    @jwt_required
    def post(self):
        try:
            current_user = get_jwt_identity()
            return jsonify({'logged_in_as': current_user})
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            return make_response(jsonify({'status': API_STATUS_ERROR}))


class ScrapeCNNArticles(Resource):
    def post(self):
        selected_years = request.json.get('years', None)
        added_by = request.json.get('user', None)
        added_on = datetime.datetime.now()
        metadata = {'added_by': added_by, 'added_on': added_on}
        try:
            scrape_cnn_articles.delay(selected_years=selected_years, metadata=metadata)
            return make_response(
                jsonify({
                    'status': API_STATUS_SUCCESS,
                    'message': "scraping articles from CNN for given years: {}".format(",".join(selected_years))
                })
            )
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            return make_response(jsonify({'status': API_STATUS_ERROR}))


class ScrapeFOXArticles(Resource):
    def post(self):
        added_by = request.json.get('user', None)
        added_on = datetime.datetime.now()
        metadata = {'added_by': added_by, 'added_on': added_on}
        try:
            scrape_fox_articles.delay(metadata=metadata)
            return make_response(
                jsonify({
                    'status': API_STATUS_SUCCESS,
                    'message': "scraping articles from FOX"
                })
            )
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            return make_response(jsonify({'status': API_STATUS_ERROR}))


api.add_resource(Ping, '/ping')
api.add_resource(Login, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(LogoutAccess, '/logout-access')
api.add_resource(Protected, '/protected')
api.add_resource(ScrapeCNNArticles, '/scrape-cnn-articles')
api.add_resource(ScrapeFOXArticles, '/scrape-fox-articles')
