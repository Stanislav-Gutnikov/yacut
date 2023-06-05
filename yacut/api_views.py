from flask import jsonify, request
from re import match
from http import HTTPStatus

from . import app, db
from .models import URLMap
from .utils import get_unique_short_id
from .error_handlers import InvalidAPIUsage


@app.route('/api/id/', methods=['POST', ])
def add_url():
    if request.get_json() is None:
        raise InvalidAPIUsage('Отсутствует тело запроса')
    data = request.get_json()
    if 'url' not in data:
        raise InvalidAPIUsage('"url" является обязательным полем!')
    if 'custom_id' in data and data['custom_id'] != '' and data['custom_id'] is not None:
        if not match(r'^[A-Za-z0-9]{1,16}$', data['custom_id']):
            raise InvalidAPIUsage('Указано недопустимое имя для короткой ссылки')
        if URLMap.query.filter_by(short=data['custom_id']).first():
            raise InvalidAPIUsage(f'Имя "{data["custom_id"]}" уже занято.')
    else:
        data['custom_id'] = get_unique_short_id()
    if URLMap.query.filter_by(original=data['url']).first():
        raise InvalidAPIUsage('Такая оригинальная ссылка уже есть в БД')
    url = URLMap(
        original=data['url'],
        short=data['custom_id']
    )
    response = {
        'short_link': 'http://localhost/' + data['custom_id'],
        'url': data['url']
    }
    db.session.add(url)
    db.session.commit()
    return jsonify(response), HTTPStatus.CREATED


@app.route('/api/id/<string:short_id>/')
def get_original_url(short_id):
    if not URLMap.query.filter_by(short=short_id).first():
        raise InvalidAPIUsage('Указанный id не найден', 404)
    original = URLMap.query.filter_by(short=short_id).first().original
    return jsonify({'url': original}), HTTPStatus.OK
