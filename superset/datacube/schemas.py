# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
import re

from flask_babel import lazy_gettext as _
from marshmallow import fields, Schema, ValidationError
from marshmallow.validate import Length

get_export_ids_schema = {"type": "array", "items": {"type": "integer"}}


def validate_python_date_format(value: str) -> None:
    regex = re.compile(
        r"""
        ^(
            epoch_s|epoch_ms|
            (?P<date>%Y(-%m(-%d)?)?)([\sT](?P<time>%H(:%M(:%S(\.%f)?)?)?))?
        )$
        """,
        re.VERBOSE,
    )
    match = regex.match(value or "")
    if not match:
        raise ValidationError(_("Invalid date/timestamp format"))


class BasicSchema(Schema):
    session_token = fields.String(validate=Length(0, 250), required=True)


class DatacubeUserSchema(Schema):
    cp_name = fields.String(validate=Length(0, 250), required=True)
    dashboard_id = fields.String(validate=Length(0, 250), required=True)
    users_name = fields.List(fields.String(validate=Length(0, 250), required=True))

class DatacubeTokenSchema(Schema):
    user_name = fields.String(validate=Length(0, 250), required=True)

class DatacubePostUserSchema(BasicSchema):
    dashboard_id = fields.String(validate=Length(0, 250), required=True)
    users_name = fields.List(fields.String(validate=Length(0, 250), required=True))

class DatacubePostTokenSchema(BasicSchema, DatacubeTokenSchema):
    pass
class DatacubePostSignSchema(Schema):
    app_token = fields.String(validate=Length(0, 250), required=True)
    app_key = fields.String(validate=Length(0, 250), required=True)