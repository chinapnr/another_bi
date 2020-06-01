import logging

from flask_appbuilder.api import expose
from flask import request, Response
from flask_appbuilder.models.sqla.interface import SQLAInterface

from superset.connectors.sqla.models import SqlaTable
from superset.const import CREATE_USER_EMAIL_SUFFIX
from superset.constants import RouteMethod
from superset.datacube.schemas import DatacubePostUserSchema,DatacubePostTokenSchema,DatacubePostSignSchema
from superset.models.user_dashboard_rel import UserDashboardRel
from superset.views.base_api import (
    BaseSupersetModelRestApi
)
import uuid
import flask_login.utils as flask_lg
from superset.models.cp_info import CpInfo
from superset.views.base import BaseSupersetView
logger = logging.getLogger(__name__)


import json
from superset.datacube import utils

class DatacubeRestApi(BaseSupersetModelRestApi):
    datamodel = SQLAInterface(SqlaTable)
    resource_name = "datacude"
    include_route_methods = {RouteMethod.POST}|{"token"}|{"sign"}
    add_model_schema = DatacubePostUserSchema()
    token_schema = DatacubePostTokenSchema()
    session_schema =DatacubePostSignSchema()
    openapi_spec_tag = "Datacube"

    @expose("/add_users", methods=["POST"])
    def post(self) -> Response:
        """Create Datacube users
        ---
        post:
          description: >-
            Create Datacube users
          requestBody:
            description: Datacube users schema
            required: true
            content:
              application/json:
                schema:
                  $ref: '#/components/schemas/{{self.__class__.__name__}}.post'
          responses:
            201:
              description: Datacube users added
              content:
                application/json:
                  schema:
                    type: object
                    properties:
                      id:
                        type: number
                      result:
                        $ref: '#/components/schemas/{{self.__class__.__name__}}.post'
            400:
              $ref: '#/components/responses/400'
            401:
              $ref: '#/components/responses/401'
            422:
              $ref: '#/components/responses/422'
            500:
              $ref: '#/components/responses/500'
        """
        # 获取请求参数
        from superset import security_manager
        if not request.is_json:
            return self.response_400(message="Request is not JSON")
        item = self.add_model_schema.load(request.json)
        if item.errors:
            return self.response_400(message=item.errors)
        session_token=item.data.get("session_token")
        if session_token is None :
            return self.response_400(message="session_token error")
        cp_info=json.loads(utils.redis_get(session_token))
        print(cp_info)
        if cp_info is None :
            return self.response_400(message="session_token error")
        dashboard_id, users_name, last_name= item.data.get("dashboard_id"), item.data.get("users_name"), "datacube"
        app_token=cp_info["app_token"]
        first_name =cp_info["short_name"]
        success_create_user_list = []

        app_key = cp_info.get("app_key")
        role_name = cp_info.get("role_name")
        short_name = cp_info.get("short_name")
        role = security_manager.find_role(role_name)
        try:
            # 批量创建用户
            for user in users_name:
                # 查询用户是否存在
                user_info = security_manager.find_user(username=short_name+user)
                if not user_info:
                    # 用户不存在则新增存在则不创建
                    email = user + CREATE_USER_EMAIL_SUFFIX
                    password = utils.generator_password(short_name + user + app_key)
                    user_info = security_manager.add_user(short_name+user, first_name, last_name, email, role, password=password)
                    success_create_user_list.append(user)

                # 关联 dashboard
                UserDashboardRel.add_data({"user_id": user_info.id, "dashboard_id":dashboard_id})

            return self.response(201, return_data=success_create_user_list)
        except Exception as ex:
            return self.response(422,message=str(ex),  return_data=success_create_user_list)



    @expose("/iframe/sign", methods=["POST"])
    def sign(self) -> Response:
        """Create Datacube users
                ---
                post:
                  description: >-
                    Create Datacube users
                  requestBody:
                    description: Datacube users schema
                    required: true
                    content:
                      application/json:
                        schema:
                          $ref: '#/components/schemas/{{self.__class__.__name__}}.post'
                  responses:
                    201:
                      description: Datacube users added
                      content:
                        application/json:
                          schema:
                            type: object
                            properties:
                              id:
                                type: number
                              result:
                                $ref: '#/components/schemas/{{self.__class__.__name__}}.post'
                    400:
                      $ref: '#/components/responses/400'
                    401:
                      $ref: '#/components/responses/401'
                    422:
                      $ref: '#/components/responses/422'
                    500:
                      $ref: '#/components/responses/500'
                """
        if not request.is_json:
            return self.response_400(message="Request is not JSON")
        item = self.session_schema.load(request.json)
        app_token=item.data.get("app_token")
        app_key=item.data.get("app_key")
        cp_info = CpInfo.get_data_by_field("app_token", app_token)
        if app_key != cp_info[0].get("app_key") :
            return self.response_400(message="Request is not JSON")
        session_uuid = str(uuid.uuid1()).replace("-", "")
        utils.redis_put(session_uuid, json.dumps(cp_info[0]))
        return self.response(200,return_data=session_uuid)


    @expose("/iframe/token", methods=["POST"])
    def token(self) -> Response:
        """Create Datacube users
                ---
                post:
                  description: >-
                    Create Datacube users
                  requestBody:
                    description: Datacube users schema
                    required: true
                    content:
                      application/json:
                        schema:
                          $ref: '#/components/schemas/{{self.__class__.__name__}}.post'
                  responses:
                    201:
                      description: Datacube users added
                      content:
                        application/json:
                          schema:
                            type: object
                            properties:
                              id:
                                type: number
                              result:
                                $ref: '#/components/schemas/{{self.__class__.__name__}}.post'
                    400:
                      $ref: '#/components/responses/400'
                    401:
                      $ref: '#/components/responses/401'
                    422:
                      $ref: '#/components/responses/422'
                    500:
                      $ref: '#/components/responses/500'
                """
        from superset import security_manager

        if not request.is_json:
            return self.response_400(message="Request is not JSON")
        item = self.token_schema.load(request.json)
        if item.errors:
            return self.response_400(message=item.errors)
        session_token=item.data.get("session_token")
        cp_info=json.loads(utils.redis_get(session_token))
        if cp_info is None :
            return self.response_400(message="cp_info is None")
        username = item.data.get('user_name')
        if username == None:
            return self.response_400(message="username is None")

        app_key = cp_info.get("app_key")
        short_name = cp_info.get("short_name")
        password = utils.generator_password(short_name + username + app_key)
        user = security_manager.auth_user_db(short_name + username, password)
        if user == None:
            return self.response_400(message="user is not exits")
        token_uuid = str(uuid.uuid1()).replace("-", "")
        userinfo = {}
        userinfo["username"] = username
        userinfo["app_key"] = app_key
        userinfo["short_name"] = short_name
        utils.redis_put(token_uuid, json.dumps(userinfo))
        return self.response(200,return_data=token_uuid)
