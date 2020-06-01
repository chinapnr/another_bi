import json
import redis
from superset.datacube.redisClient import RedisClient
from superset.config import REDIS_CONFIG

def generator_password(plaintext):
    from fishbase.fish_crypt import FishSha256
    password = FishSha256.hashlib_sha256(plaintext)
    # print(f"当前用户密码为: {password}")
    return password


def get_sign(request_method: str, app_key: str, app_token: str, params: dict):
    from fishbase.fish_crypt import FishSha256
    params.pop("sign","true")
    sorted_params = sorted(params, key=lambda x: x[0])
    plaintext = request_method.upper() + \
                    app_token + \
                    '&'.join([x + '=' + str(params.get(x)) for x in sorted_params if x]).replace("'", '"')
    sign = FishSha256.hmac_sha256(app_key, plaintext)
    print(f"正确 sign, {sign}")
    return sign

def get_user_info_by_token( token):
    username = None
    password = None
    try:
        userinfo = json.loads(redis_get(token))
        username = userinfo["short_name"] + userinfo["username"]
        password = generator_password(username + userinfo["app_key"])
    except Exception:
        return username, password
    return username, password

def get_redis_conn():
    """
    获取 redis 链接
    :param :
    :return:
    """
    redis = RedisClient(**REDIS_CONFIG)
    return redis

def redis_put( token_uuid, values):
    redis_cli = get_redis_conn()
    redis_cli.set_data(token_uuid, values, ex=10 * 60 * 1000)

def redis_get( token_uuid):
    r = get_redis_conn()
    res = r.get_data(token_uuid)
    if res != None:
        redis_put(token_uuid, res)
        return res
    return None