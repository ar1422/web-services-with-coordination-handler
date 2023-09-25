import uuid
from pydantic import BaseModel
from db_helper import DatabaseWrapper


SEARCH_TO_RANK_MAP = {'/rank/rank_movies': "/search/search_movies", '/rank/rank_tv_series': "/search/search_tv_series"}
CONVERSATION_ID_MAP = {}

RANK_CALLS = ['/rank/rank_movies', '/rank/rank_tv_series']
ALL_APP_CALLS = ['/rank/rank_movies', '/rank/rank_tv_series', "/search/search_movies", "/search/search_tv_series"]


class RatingModel(BaseModel):

    search_string: str
    rating: float


def generate_conversation_id():
    return str(uuid.uuid4())


def validate_user(username, password):
    if username is None or password is None:
        return False

    database_wrapper = DatabaseWrapper()
    return database_wrapper.validate_user(username, password)


def add_new_conversation(username):
    conversation_id = generate_conversation_id()
    default_dictionary = {"/search/search_movies": False, "/search/search_tv_series": False}
    if username not in CONVERSATION_ID_MAP:

        CONVERSATION_ID_MAP[username] = {conversation_id: default_dictionary}
        return conversation_id

    CONVERSATION_ID_MAP[username][conversation_id] = default_dictionary
    return conversation_id


def update_user_conversation(username, conversation_id, operation):
    if conversation_id is None:
        conversation_id = add_new_conversation(username)

    CONVERSATION_ID_MAP[username][conversation_id][operation] = True
    return conversation_id


def check_user_conversation_history(username, conversation_id):
    conversation_map = CONVERSATION_ID_MAP.get(username, None)
    if conversation_map is None:
        return False
    return conversation_id in conversation_map


def validate_conversation(username, conversation_id, operation):
    if operation in RANK_CALLS:
        if conversation_id is None or not check_user_conversation_history(username, conversation_id):
            return False
        else:
            conversation_id_map = CONVERSATION_ID_MAP.get(username).get(conversation_id)
            return conversation_id_map[SEARCH_TO_RANK_MAP[operation]]
    else:
        return conversation_id is None or check_user_conversation_history(username, conversation_id)
