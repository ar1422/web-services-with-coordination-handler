from db_helper import DatabaseWrapper
from fastapi import FastAPI, Request, Response
from models import RatingModel
import uvicorn
from models import ALL_APP_CALLS, validate_user, validate_conversation, update_user_conversation

app = FastAPI()


@app.get("/")
async def root():
    return {"MESSAGE": "Welcome to Movie Ratings"}


@app.middleware("http")
async def middleware_manager(request: Request, call_next):
    if request.url.path not in ALL_APP_CALLS:
        response = await call_next(request)
        return response

    username = request.headers.get("username", None)
    password = request.headers.get("password", None)

    if not validate_user(username, password):
        return Response(status_code=500, content="Please provide valid Username and Password")

    conversation_id = request.headers.get("conversation_id", None)
    conversation_validation = validate_conversation(username, conversation_id, request.url.path)
    if not conversation_validation:
        return Response(status_code=500, content="Please provide valid Conversation ID")

    response = await call_next(request)
    response.headers["conversation_id"] = update_user_conversation(username, conversation_id, request.url.path)
    return response


@app.get("/search/search_movies")
async def search_movies(request: Request):

    database_wrapper = DatabaseWrapper()
    search_string = request.query_params.get("search_string")
    all_filtered_movies = database_wrapper.search_movies_by_name(search_string)
    if len(all_filtered_movies) == 0:
        return {"MESSAGE": "FAIL", "CONTENT": None}
    else:
        return {"MESSAGE": "SUCCESS", "CONTENT": all_filtered_movies}


@app.get("/search/search_tv_series")
async def search_tv_series(request: Request):
    database_wrapper = DatabaseWrapper()
    search_string = request.query_params.get("search_string")
    all_filtered_tv_series = database_wrapper.search_tv_series_by_name(search_string)
    if len(all_filtered_tv_series) == 0:
        return {"MESSAGE": "FAIL", "CONTENT": None}
    else:
        return {"MESSAGE": "SUCCESS", "CONTENT": all_filtered_tv_series}


@app.post("/rank/rank_movies")
async def rank_movies(rating_obj: RatingModel):
    database_wrapper = DatabaseWrapper()
    movie_name = rating_obj.search_string
    rating = rating_obj.rating
    updated_movies = database_wrapper.update_movie_ratings(movie_name, rating)
    if len(updated_movies) == 0:
        return {"MESSAGE": "FAIL", "CONTENT": None}
    else:
        return {"MESSAGE": "SUCCESS", "CONTENT": updated_movies}


@app.post("/rank/rank_tv_series")
async def rank_tv_series(rating_obj: RatingModel):
    database_wrapper = DatabaseWrapper()
    tv_series_name = rating_obj.search_string
    rating = rating_obj.rating
    updated_tv_series = database_wrapper.update_tv_series_ratings(tv_series_name, rating)
    if len(updated_tv_series) == 0:
        return {"MESSAGE": "FAIL", "CONTENT": None}
    else:
        return {"MESSAGE": "SUCCESS", "CONTENT": updated_tv_series}


if __name__ == '__main__':
    uvicorn.run(app)
