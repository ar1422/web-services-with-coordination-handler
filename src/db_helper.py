import pandas as pd
from pymongo import MongoClient


class DatabaseWrapper(object):
    connection = None
    hostname = "localhost"
    port_number = 27017
    database_name = "MOVIES_TV_SERIES_COLLECTION"
    list_of_connections = ["TOP_MOVIES", "TOP_TV_SERIES", "USERS"]
    connection_to_data_map = {"TOP_MOVIES": "input_data/TOP_MOVIES_PROCESSED.csv",
                              "TOP_TV_SERIES": "input_data/TOP_TV_SERIES_PROCESSED.csv",
                              "USERS": "input_data/USER_DATA.csv"}

    def __init__(self):
        if DatabaseWrapper.connection is None:
            DatabaseWrapper.connection = MongoClient(DatabaseWrapper.hostname, DatabaseWrapper.port_number)

        self.connection = DatabaseWrapper.connection

        list_of_databases = self.connection.list_database_names()
        if DatabaseWrapper.database_name not in list_of_databases:
            self.db = self.connection[DatabaseWrapper.database_name]
        else:
            self.db = self.connection.get_database(DatabaseWrapper.database_name)

    def add_user(self, user_name, password):
        user_collection = self.db.get_collection("USERS")
        user_collection.insert_one({"USERNAME": user_name, "PASSWORD": password})
        return

    def validate_user(self, username, password):
        user_collection = self.db.get_collection("USERS")
        find_criteria = {"USERNAME": username}
        filtered_dict = self.find_one_from_collection(user_collection, find_criteria)
        return len(filtered_dict) > 0 and filtered_dict["PASSWORD"] == password

    def add_collection_to_db(self):
        all_existing_collection = self.db.list_collections()
        for collection in DatabaseWrapper.list_of_connections:
            if collection not in all_existing_collection:
                self.db.create_collection(collection)
                collection_obj = self.db.get_collection(collection)
                input_df = pd.read_csv(self.connection_to_data_map.get(collection))
                input_records = input_df.to_dict('records')
                collection_obj.insert_many(input_records)

    @staticmethod
    def find_one_from_collection(collection, find_criteria):
        filtered_collection = collection.find_one(find_criteria)
        if filtered_collection is None:
            return {}
        else:
            filtered_collection = dict(filtered_collection)
            filtered_collection.pop('_id')
            return filtered_collection

    def search_movies_by_name(self, search_string):
        movie_collection = self.db.get_collection("TOP_MOVIES")
        find_criteria = {"MOVIE_NAME": search_string}
        output_dict = self.find_one_from_collection(movie_collection, find_criteria)
        return output_dict

    def search_tv_series_by_name(self, search_string):
        tv_series_collection = self.db.get_collection("TOP_TV_SERIES")
        find_criteria = {"TV_SERIES_NAME": search_string}
        output_dict = self.find_one_from_collection(tv_series_collection, find_criteria)
        return output_dict

    def update_movie_ratings(self, movie_name, rating):
        movie_collection = self.db.get_collection("TOP_MOVIES")
        filtered_movies = movie_collection.find({"MOVIE_NAME": movie_name})
        output_dict = {}

        for movie in filtered_movies:
            current_votes = movie["VOTES"]
            current_rating = movie["RATING"]
            updated_votes = current_votes + 1
            updated_rating = float((current_rating * current_votes) + rating) / updated_votes
            movie_collection.update_one({"_id": movie["_id"]},
                                        {"$set": {'VOTES': updated_votes, "RATING": updated_rating}})
            output_dict[movie["MOVIE_NAME"]] = updated_rating

        return output_dict

    def update_tv_series_ratings(self, tv_series_name, rating):
        tv_series_collection = self.db.get_collection("TOP_TV_SERIES")
        filtered_tv_series = tv_series_collection.find({"TV_SERIES_NAME": tv_series_name})
        output_dict = {}

        for tv_series in filtered_tv_series:
            current_votes = tv_series["VOTES"]
            current_rating = tv_series["RATING"]
            updated_votes = current_votes + 1
            updated_rating = float((current_rating * current_votes) + rating) / updated_votes
            tv_series_collection.update_one({"_id": tv_series["_id"]},
                                            {"$set": {'VOTES': updated_votes, "RATING": updated_rating}})
            output_dict[tv_series["TV_SERIES_NAME"]] = updated_rating

        return output_dict


if __name__ == '__main__':
    database_wrapper = DatabaseWrapper()
    database_wrapper.add_collection_to_db()
