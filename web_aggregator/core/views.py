import datetime
import logging
import os
import traceback

from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity, create_refresh_token
)
from flask_restful import Resource

from web_aggregator import app, api, JWT_ACCESS_TOKEN_TIMEDELTA, JWT_REFRESH_TOKEN_TIMEDELTA
# from web_aggregator.common import mem_cache
from web_aggregator.common.constants import (
    API_STATUS_SUCCESS, API_STATUS_FAILURE, API_STATUS_ERROR, DEFAULT_PAGE, DEFAULT_PER_PAGE
)
from web_aggregator.core.controller import fetch_categories
from web_aggregator.core.models import fetch_mongo_articles

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


class Categories(Resource):
    def get(self):
        try:
            categories = fetch_categories()
            if categories:
                return make_response(jsonify({'status': API_STATUS_SUCCESS, 'data': categories}))
            else:
                return make_response(jsonify({'status': API_STATUS_FAILURE, 'data': None}))
        except Exception as e:
            logger.error(e)
            logger.debug(traceback.format_exc())
            return make_response(jsonify({'status': API_STATUS_ERROR}))


class Articles(Resource):
    def post(self):
        try:
            categories = request.json.get('categories', [])
            sources = request.json.get('sources', [])
            per_page = request.json.get('per_page', DEFAULT_PER_PAGE)
            page = request.json.get('page', DEFAULT_PAGE)
            years = request.json.get('years', [str(datetime.datetime.now().year)])
            articles = fetch_mongo_articles(
                categories=categories, sources=sources, years=years, page=page, per_page=per_page
            )
            if articles:
                return make_response(jsonify({'status': API_STATUS_SUCCESS, 'articles': articles}))
            else:
                return make_response(jsonify({'status': API_STATUS_FAILURE, 'articles': None}))
        except Exception as e:
            app.logger.error(e)
            app.logger.debug(traceback.format_exc())
            return make_response(jsonify({'status': API_STATUS_ERROR}))


api.add_resource(Ping, '/ping')
api.add_resource(Login, '/login')
api.add_resource(TokenRefresh, '/refresh')
api.add_resource(Protected, '/protected')
api.add_resource(Categories, '/categories')
api.add_resource(Articles, '/articles')
