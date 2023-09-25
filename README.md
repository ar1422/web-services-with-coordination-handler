# Move and TV Series Ratings 

This application is a web-service to search IMDB movies and TV series data and rank them by the users. 

## Features of the Application – 
   * User can search Movies and TV series.
   * User can provide their rating for any Movies/TV Series present in the collection.
   * The rating is updated with the average of existing values and new values.

   
## Technical details of the application - 
   * The application contains 3 data sets. All the dataset is present in input_data folder -
        * Top movies data (TOP_MOVIES_PROCESSED.csv)
        * Top TV Series data (TOP_TV_SERIES_PROCESSED.csv)
        * Top TV Series data (TOP_TV_SERIES_PROCESSED.csv)
   * MongoDB is used as backend database. The application provides a script (db_helper.py) provide option to load the data sets into local DB connection.
   * Python and FastAPI is used to develop the web service and client module to demonstrate web service invocation. All the source code is present in src folder and client modules are present in src/testing folder. 

        
      
 ## Structure and design of the code - 
 
   * The designed web-service includes a middleware (endpoint:  middleware_manager) which acts as an intermediary between the client and services. The middleware receives all the input requests, validates the requests by processing only the header and then forwards the request to required service end-points. It receives the response from the end-point and sends it to the client. 
   * There are four services – search movies, rank movies, search tv series, and rank tv series.
   * The co-ordination policy of the web service – search operation needs to be performed before rank operation. Also search and rank should be for the same type of the data (movies/tv series) – i.e. searching movies and trying to rank tv series is an invalid sequence.
   * A user can have more than 1 conversation with the service. Each service keeps track of all the search operations performed in that conversation so validation can be done.
   * Whenever a search request is received, the middleware checks the header and validates the username and password. If the validation fails, it returns a Response of 500. If the validation passes, it moves to validating the conversation ID. If the client has not provided the ID, it’ll assign a new one otherwise it validates whether the conversation ID matches to the username. If validation is passed, the search operation is marked complete and now user can make a post request.
   * Whenever a post request is received, the middleware the checks the header and validates username, password, and conversation ID. Then it checks if the conversation ID is marked complete. If the search operation is completed, it allows the update of the rating else the client is informed to perform the search first and then send a post request.


## Installation

#### Requirements
 * fastapi==0.95.0
 * pandas==1.3.5
 * pydantic==1.10.6
 * pymongo==4.3.3
 * requests==2.28.2
 * uvicorn==0.21.1

     
## Usage

The input data for the project is provided in the input_data folder.

There are three main data sets - Movie data set, TV series data set, and dummy users data.

To load the data into the MongoDB, please run the command - 
```python
    python db_helper.py
```

To start the web-services, please run the command - 
```python
    python movie_ratings.py
```
    
To run the valid client test simulation code, please run the command - 
```python
    python valid_requests_from_client.py
```
    
To run the Invalid client test simulation code, please run the command - 
```python
    python invalid_requests_from_client.py
```
    
