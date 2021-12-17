from datetime import timedelta, datetime
import jwt
import json
from functools import wraps
import flask as flaskk
from flask import request, abort
from es_client import es_client
objects_priviledges = []


# defined in API specification structure
path_blacklist = {
    "/get-cards": {
        "GET": [],
        "POST": [],
        "PUT": [],
        "DELETE": [],
    },
    "/get-card": {
        "GET": [],
        "POST": [],
        "PUT": [],
        "DELETE": [],
    },
    "/create-card": {
        "GET": [],
        "POST": [],
        "PUT": [],
        "DELETE": [],
    },
    "/delete-card": {
        "GET": [],
        "POST": [],
        "PUT": [],
        "DELETE": [],
    },
}


def check_path_priviledge(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        header = request.headers["Authorization"]
        bearer = header.split(" ")[1]
        decoded = jwt.decode(bearer, "secret", algorithms=["HS256"])
        now = datetime.strptime(
            datetime.now().time().strftime("%H:%M:%S"), "%H:%M:%S")
        if datetime.strptime(decoded["time"], '%H:%M:%S') > now:
            if decoded["username"] not in path_blacklist[request.path][request.method]:
                return f(*args, **kwargs)
            else:
                es_client.addEntry(request, 401)
                abort(401)
        else:
            es_client.addEntry(request, 401)
            abort(401)

    return decorated_function


def check_obj_priviledge_to_alter(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if request.method == "GET":
            header = request.headers["Authorization"]
            bearer = header.split(" ")[1]
            decoded = jwt.decode(bearer, "secret", algorithms=["HS256"])
            for datum in objects_priviledges:
                if datum["category"] == str(request.args.get('category')):
                    if (decoded["username"] in datum["users_ro"]) or (decoded["username"] in datum["users_rw"]):
                        if str(datum["id"]) == str(request.args.get('id')):
                            return json.dumps(datum, indent=2)
            es_client.addEntry(request, 401)
            abort(401)

        elif request.method == "POST":
            header = request.headers["Authorization"]
            bearer = header.split(" ")[1]
            decoded = jwt.decode(bearer, "secret", algorithms=["HS256"])
            for index, datum in enumerate(objects_priviledges):
                if datum["category"] == str(request.args.get('category')):
                    if decoded["username"] in datum["users_rw"]:
                        if str(datum["id"]) == str(request.args.get('id')):
                            objects_priviledges[index] = dict(request.json)
                            status_code = flaskk.Response(status=201)
                            return status_code
            es_client.addEntry(request, 401)
            abort(401)
    return decorated_function


def check_obj_priviledge(category=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if request.method == "GET" or request.method == "HEAD":
                header = request.headers["Authorization"]
                bearer = header.split(" ")[1]
                decoded = jwt.decode(bearer, "secret", algorithms=["HS256"])
                for datum in objects_priviledges:
                    if datum["category"] == category:
                        if (decoded["username"] in datum["users_ro"]) or (decoded["username"] in datum["users_rw"]):
                            if str(datum["id"]) == str(request.args.get('id')):
                                return f(*args, **kwargs)
                es_client.addEntry(request, 401)
                abort(401)
            elif request.method == "DELETE":
                header = request.headers["Authorization"]
                bearer = header.split(" ")[1]
                decoded = jwt.decode(bearer, "secret", algorithms=["HS256"])
                for index, datum in enumerate(objects_priviledges):
                    if datum["category"] == category:
                        if (decoded["username"] in datum["users_ro"]) or (decoded["username"] in datum["users_rw"]):
                            if str(datum["id"]) == str(request.args.get('id')):
                                objects_priviledges.pop(index)
                                return f(*args, **kwargs)
                es_client.addEntry(request, 401)
                abort(401)

            else:
                header = request.headers["Authorization"]
                bearer = header.split(" ")[1]
                decoded = jwt.decode(bearer, "secret", algorithms=["HS256"])
                for datum in objects_priviledges:
                    if datum["category"] == category:
                        if decoded["username"] in datum["users_rw"]:
                            return f(*args, **kwargs)
                es_client.addEntry(request, 401)
                abort(401)

        return decorated_function
    return decorator


def generate_obj_priviledge(category=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            info = json.loads(f(*args, **kwargs))
            print("DIN DECORATOR "+category)
            object_info = {
                "id": info["id"],
                "category": category,
                "users_ro": [],
                "users_rw": [info["username"]]
            }
            global objects_priviledges
            objects_priviledges.append(object_info)
            print(objects_priviledges)
            return json.dumps(info)
        return decorated_function
    return decorator


def authenticate_user(creds):
    try:
        if creds["username"] == "cisco" and creds["password"] == "cisco":
            expiration = (datetime.now() + timedelta(minutes=5)
                          ).time().strftime("%H:%M:%S")
            print("The token will expire at: "+expiration)
            # send the user the token to do whaever he wants
            encoded = jwt.encode(
                {"username": "cisco", "time": expiration}, "secret", algorithm="HS256")
            es_client.addEntryAuth(request, "username="+creds["username"], str(encoded), 200)
            return {"token": str(encoded)}
        elif creds["username"] == "hacker" and creds["password"] == "cisco":
            expiration = (datetime.now() + timedelta(minutes=5)
                          ).time().strftime("%H:%M:%S")
            print("The token will expire at: "+expiration)
            # send the user the token to do whaever he wants
            encoded = jwt.encode(
                {"username": creds["username"], "time": expiration}, "secret", algorithm="HS256")
            es_client.addEntryAuth(request, "username="+creds["username"], str(encoded), 200)
            return {"token": str(encoded)}
        else:
            return "Bad creds"
    except Exception as e:
        es_client.addEntryAuth(request, "username="+creds.get("username", ""), str(encoded), 404)
        return "Something went wrong! With authenticate_user() function  "+str(e)
