# -*- coding: utf-8 -*-
# Copyright 2018, XOE Solutions
# Copyright 2018 Rafis Bikbov <https://it-projects.info/team/bikbov>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import base64
import json
import logging
from odoo import http
from . import pinguin

_logger = logging.getLogger(__name__)

#################################################################
# Odoo REST API                                                 #
#  Version 1                                                    #
# --------------------------------------------------------------#
# The current api version is considered stable, although        #
# the exposed models and methods change as they are configured  #
# on the database level. Only if significant changes in the api #
# generation logic should be implemented in the future          #
# a version bump should be considered.                          #
#################################################################

API_ENDPOINT = '/api'
API_ENDPOINT_V1 = '/v1'


API_ENDPOINT_V2 = '/v2'

class ApiV2Controller(http.Controller):
    _api_endpoint = API_ENDPOINT + API_ENDPOINT_V2
    _api_endpoint = _api_endpoint + '/<namespace>'
    _api_endpoint_model = _api_endpoint + '/<model>'
    _api_endpoint_model_id = _api_endpoint + '/<model>/<int:id>'

    _api_endpoint_image_file = _api_endpoint + '/image'

    @pinguin.route2(_api_endpoint_image_file, methods=['POST'], type='http', auth='none', csrf=False, website=True, cors="*")
    def v2_call_image_file(self, namespace, file, model_mame, res_id, field_name, method_name, method_params):
        _logger.info('=======v2_call_image_file========0 %s %s %s %s %s %s' % (method_name, method_params, file, model_mame, res_id, field_name))
        try:
            res_id = int(res_id)
            method_params = json.loads(method_params)
            method_params.update({field_name: base64.b64encode(file.read())})

            _logger.info('=======v2_call_image_file========1 %s %s' % (res_id, bool(res_id)))
            if res_id:
                _logger.info('=======v2_call_image_file========2 %s %s' % (model_mame, method_name) )
                res = pinguin.wrap__resource_v2_call_method(
                    modelname=model_mame,
                    ids=[int(res_id)],
                    method_name=method_name,
                    method_params=method_params,
                    success_code=pinguin.CODE__success)
            else:
                _logger.info('=======v2_call_image_file========3 %s %s' % (model_mame, method_name))
                res = pinguin.wrap__resource_v2_call_class_method(
                    modelname=model_mame,
                    method_name=method_name,
                    method_params=method_params,
                    success_code=pinguin.CODE__success,
                    context={},
                )

                _logger.info('=======v2_call_image_file========4 %s' % (res))

        except Exception as e:
            res = {'error_code': 999, 'error_message': str(e)}

        _logger.info('=======v2_call_image_file========99 %s' % (res))
        response = http.request.make_response(json.dumps(res, ensure_ascii=False))
        response.headers.set('Content-Type', 'application/json;charset=UTF-8')
        return response



    @pinguin.route2(_api_endpoint_model_id, methods=['POST'], type='json', auth='none', csrf=False,  cors="*")
    def v2_call_method_one__POST(self, namespace, model, id):
        _logger.info('=======v2_call_method_one__POST========0 %s %s %s' % (namespace, model, id))

        data_str = http.request.httprequest.data
        _logger.info('=======v2_call_method_one__POST========1 %s' % (data_str))
        if isinstance(data_str, bytes):
            data_str = str(data_str, encoding="utf-8")
            _logger.info('=======v2_call_method_one__POST========2 %s' % (data_str))

        data = json.loads(data_str)
        _logger.info('=======v2_call_method_one__POST========3 %s' % (data))
        if ('method_name' not in data) or ('method_params' not in data):
            raise Warning('method_name 和 method_params 是必须的参数')

        method_name, method_params = data.get('method_name'), data.get('method_params')

        _logger.info('=======v2_call_method_one__POST========4 %s %s %s %s' % (type(method_params), type(method_name), method_name, method_params))
        res = pinguin.wrap__resource_v2_call_method(
            modelname=model,
            ids=[id],
            method_name=method_name,
            method_params=method_params,
            success_code=pinguin.CODE__success)

        _logger.info('=======v2_call_method_one__POST========5 %s' % (res))

        return res
        # response = http.request.make_response(json.dumps(res, ensure_ascii=False))
        # response.headers.set('Content-Type', 'application/json;charset=UTF-8')
        # return response


# We patch the route decorator in pinguin.py
# with authentication and DB inference logic.
# We also check if the model is installed in the database.
# Furthermore we check if api version is supported.
# This keeps the code below minial and readable.


class ApiV1Controller(http.Controller):
    """ Implements the REST API V1 endpoint.
    .. methods:

        CRUD Methods:
        - `POST     .../<model>`               -> `CreateOne`
        - `PUT      .../<model>/<id>`          -> `UpdateOne`
        - `GET      .../<model>`               -> `ReadMulti`
        - `GET      .../<model>/<id>`          -> `ReadOne`
        - `DELETE   .../<model>/<id>`          -> `UnlinkOne`

        Auxiliary Methods:
        - `PATCH    .../<model>/<id>/<method>`               -> `Call Method on Singleton Record`
        - `PATCH    .../<model>/<method>`                    -> `Call Method on RecordSet`
        - `GET      .../report/pdf/<report_external_id>`     -> `Get Report as PDF`
        - `GET      .../report/html/<report_external_id>`    -> `Get Report as HTML`
    """

    _api_endpoint = API_ENDPOINT + API_ENDPOINT_V1
    _api_endpoint = _api_endpoint + '/<namespace>'
    # CreateOne # ReadMulti
    _api_endpoint_model = _api_endpoint + '/<model>'
    # ReadOne # UpdateOne # UnlinkOne
    _api_endpoint_model_id = _api_endpoint + '/<model>/<int:id>'
    # Get Reports
    _api_report_docids = _api_endpoint + '/report/<any(pdf, html):converter>/<report_external_id>/<docids>'

    # #################
    # # CRUD Methods ##
    # #################

    # CreateOne
    @pinguin.route(_api_endpoint_model, methods=['POST'], type='json', auth='none', csrf=False)
    def create_one__POST(self, namespace, model, **data):
        conf = pinguin.get_model_openapi_access(namespace, model)
        pinguin.method_is_allowed('api_create', conf['method'], main=True, raise_exception=True)
        # FIXME: What is contained in context and for what?
        # # If context is not a python dict
        # # TODO unwrap
        # if isinstance(kw.get('context'), basestring):
        #     context = get_create_context(namespace, model, kw.get('context'))
        # else:
        #     context = kw.get('context') or {}

        # jon 创建记录改为json格式，
        # TODO 如何直接得到data数据，可能需要改写route的处理？
        data_s = http.request.httprequest.data
        data = json.loads(data_s)
        return pinguin.wrap__resource__create_one(
            modelname=model,
            context=conf['context'],
            data=data,
            success_code=pinguin.CODE__created,
            out_fields=conf['out_fields_read_one'])

    # ReadMulti (optional: filters, offset, limit, order, include_fields, exclude_fields):
    @pinguin.route(_api_endpoint_model, methods=['GET'], type='http', auth='none', csrf=False)
    def read_multi__GET(self, namespace, model, **kw):
        conf = pinguin.get_model_openapi_access(namespace, model)
        pinguin.method_is_allowed('api_read', conf['method'], main=True, raise_exception=True)
        return pinguin.wrap__resource__read_all(
            modelname=model,
            success_code=pinguin.CODE__success,
            out_fields=conf['out_fields_read_multi'])

    # ReadOne (optional: include_fields, exclude_fields)
    @pinguin.route(
        _api_endpoint_model_id, methods=['GET'], type='http', auth='none', csrf=False)
    def read_one__GET(self, namespace, model, id, **kw):
        conf = pinguin.get_model_openapi_access(namespace, model)
        pinguin.method_is_allowed('api_read', conf['method'], main=True, raise_exception=True)
        return pinguin.wrap__resource__read_one(
            modelname=model,
            id=id,
            success_code=pinguin.CODE__success,
            out_fields=conf['out_fields_read_one'])

    # UpdateOne
    @pinguin.route(_api_endpoint_model_id, methods=['PUT'], type='http', auth='none', csrf=False)
    def update_one__PUT(self, namespace, model, id, **data):
        conf = pinguin.get_model_openapi_access(namespace, model)
        pinguin.method_is_allowed('api_update', conf['method'], main=True, raise_exception=True)
        return pinguin.wrap__resource__update_one(
            modelname=model, id=id, success_code=pinguin.CODE__ok_no_content, data=data)

    # UnlinkOne
    @pinguin.route(_api_endpoint_model_id, methods=['DELETE'], type='http', auth='none', csrf=False)
    def unlink_one__DELETE(self, namespace, model, id, **data):
        conf = pinguin.get_model_openapi_access(namespace, model)
        pinguin.method_is_allowed('api_delete', conf['method'], main=True, raise_exception=True)
        return pinguin.wrap__resource__unlink_one(
            modelname=model, id=id, success_code=pinguin.CODE__ok_no_content)

    # ######################
    # # Auxiliary Methods ##
    # ######################

    # Call Method on Singleton Record (optional: method parameters)
    @pinguin.route(_api_endpoint_model_id, methods=['POST', 'GET'], type='http', auth='none', csrf=False)
    def call_method_one__PATCH(self, namespace, model, id, method_name, method_params=None):
        conf = pinguin.get_model_openapi_access(namespace, model)
        pinguin.method_is_allowed(method_name, conf['method'])
        method_params = json.loads(method_params) if method_params else {}

        _logger.info('==call_method_one__PATCH== %s %s %s %s ' % (model, id, method_name, method_params))
        return pinguin.wrap__resource__call_method(
            modelname=model,
            ids=[id],
            method=method_name,
            method_params=method_params,
            success_code=pinguin.CODE__success)

    # Call Method on RecordSet (optional: method parameters)
    @pinguin.route(_api_endpoint_model, methods=['PATCH'], type='http', auth='none', csrf=False)
    def call_method_multi__PATCH(self, namespace, model, method_name, ids, method_params=None, **kw):
        conf = pinguin.get_model_openapi_access(namespace, model)
        pinguin.method_is_allowed(method_name, conf['method'])
        ids = json.loads(ids)
        method_params = json.loads(method_params) if method_params else {}
        return pinguin.wrap__resource__call_method(
            modelname=model,
            ids=ids,
            method=method_name,
            method_params=method_params,
            success_code=pinguin.CODE__success)

    # Get Report
    @pinguin.route(_api_report_docids, methods=['GET'], type='http', auth='none', csrf=False)
    def report__GET(self, converter, namespace, report_external_id, docids):
        return pinguin.wrap__resource__get_report(namespace=namespace, report_external_id=report_external_id, docids=docids, converter=converter,
                                                  success_code=pinguin.CODE__success)
