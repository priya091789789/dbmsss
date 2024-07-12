import streamlit as st
import mysql.connector
from mysql.connector import Error

# Establishing the connection to the database
def create_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            database='dbmsproject',
            user='priyanka',
            password='priyanka'
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            st.write("Connected to MySQL Server version ", db_info)
            cursor = connection.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            st.write("Connected to database: ", record)
        return connection
    except Error as e:
        st.error(f"Error while connecting to MySQL: {e}")
        return None

# Run a query and return the result
def run_query(query):
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.close()
        return result
    else:
        st.error("Failed to connect to the database")
        return None
    

# Insert data function
def insert_movie(movie_id, name, release_date, genre, duration, collection):
    query = f"INSERT INTO Movies (movie_id, name, release_date, genre, duration, collection) VALUES ({movie_id}, '{name}', '{release_date}', '{genre}', {duration}, {collection})"
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            st.success('Movie inserted successfully')
        except Error as e:
            st.error(f"Error executing query: {e}")
        finally:
            connection.close()

# Update data function
def update_movie_collection(movie_id, new_collection):
    query = f"UPDATE Movies SET collection = {new_collection} WHERE movie_id = {movie_id}"
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            st.success('Movie collection updated successfully')
        except Error as e:
            st.error(f"Error executing query: {e}")
        finally:
            connection.close()

# Delete data function
def delete_movie(movie_id):
    query = f"DELETE FROM Movies WHERE movie_id = {movie_id}"
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            connection.commit()
            st.success('Movie deleted successfully')
        except Error as e:
            st.error(f"Error executing query: {e}")
        finally:
            connection.close()
        
# Select data function
def select_movies():
    query = "SELECT * FROM Movies"
    connection = create_connection()
    if connection is not None:
        cursor = connection.cursor()
        try:
            cursor.execute(query)
            result = cursor.fetchall()
            return result
        except Error as e:
            st.error(f"Error executing query: {e}")
            return None
        finally:
            connection.close()


# Streamlit app layout
st.title('Movies Database Interface')

# Create tabs for different operations
tabs = st.tabs(["Insert Data", "Update Data", "Delete Data", "Select Data", "Conditional Queries", "Aggregation Functions", "Join Operations", "Nested Queries", "Group By Queries"])


# Insert Data
with tabs[0]:
    st.header('Insert Data into the Database')
    
    # Form for inserting movie
    movie_id = st.number_input('Movie ID', min_value=1, step=1)
    name = st.text_input('Movie Name')
    release_date = st.date_input('Release Date')
    genre = st.text_input('Genre')
    duration = st.number_input('Duration (in minutes)', min_value=1, step=1)
    collection = st.number_input('Collection (in dollars)', min_value=0, step=1000000)
    
    if st.button('Insert Movie'):
        insert_movie(movie_id, name, release_date, genre, duration, collection)

# Update Data
with tabs[1]:
    st.header('Update Data in the Database')
    
    # Form for updating movie collection
    movie_id = st.number_input('Movie ID to Update', min_value=1, step=1)
    new_collection = st.number_input('New Collection (in dollars)', min_value=0, step=1000000)
    
    if st.button('Update Movie Collection'):
        update_movie_collection(movie_id, new_collection)

# Delete Data
with tabs[2]:
    st.header('Delete Data from the Database')
    
    # Form for deleting movie
    movie_id = st.number_input('Movie ID to Delete', min_value=1, step=1)
    
    if st.button('Delete Movie'):
        delete_movie(movie_id)

# Select Data
with tabs[3]:
    st.header('Select Data from the Database')
    
    # Button to retrieve and display movies
    if st.button('Show Movies'):
        movies = select_movies()
        if movies:
            for movie in movies:
                st.write(movie)

# Conditional Queries
with tabs[4]:
    st.header('Conditional Queries')
    queries = {
        'Movies released after 2010': "SELECT * FROM Movies WHERE release_date > '2010-01-01';",
        'Actors aged above 40': "SELECT p.person_id, p.name, p.date_of_birth, p.age, p.gender, a.actor_id, a.no_of_films FROM Persons p JOIN Actors a ON p.person_id = a.person_id WHERE p.age > 40;",
        'Movies with more than 4 songs': "SELECT m.name AS movie_name, COUNT(s.song_id) AS no_of_songs FROM Movies m JOIN Songs s ON m.movie_id = s.movie_id GROUP BY m.movie_id HAVING no_of_songs > 4;"
    }
    query_option = st.selectbox('Select a conditional query', list(queries.keys()))
    if st.button('Run Conditional Query'):
        query = queries[query_option]
        result = run_query(query)
        if result is not None:
            for row in result:
                st.write(row)

# Aggregation Functions
with tabs[5]:
    st.header('Aggregation Functions')
    queries = {
        'Count number of movies': "SELECT COUNT(*) FROM Movies;",
        'Average rating of a specific movie': "SELECT AVG(rating) FROM Reviews WHERE movie_id = 1;",
        'Total collection of all movies': "SELECT SUM(collection) FROM Movies;"
    }
    query_option = st.selectbox('Select an aggregation query', list(queries.keys()))
    if st.button('Run Aggregation Query'):
        query = queries[query_option]
        result = run_query(query)
        if result is not None:
            for row in result:
                st.write(row)

# Join Operations
with tabs[6]:
    st.header('Join Operations')
    queries = {
        'Movies and their directors': "SELECT m.name AS movie_name, p.name AS director_name FROM Movies m JOIN Directors d ON m.movie_id = d.director_id JOIN Persons p ON d.person_id = p.person_id;",
        'Movies and their reviews': "SELECT m.name AS movie_name, r.rating, r.review_text FROM Movies m JOIN Reviews r ON m.movie_id = r.movie_id;",
        'Movies available on streaming platforms': "SELECT m.name AS movie_name, sp.platform_name FROM Movies m JOIN StreamingPlatform sp ON m.movie_id = sp.movie_id;"
    }
    query_option = st.selectbox('Select a join query', list(queries.keys()))
    if st.button('Run Join Query'):
        query = queries[query_option]
        result = run_query(query)
        if result is not None:
            for row in result:
                st.write(row)

# Nested Queries
with tabs[7]:
    st.header('Nested Queries')
    queries = {
        'Movie with the highest collection': "SELECT * FROM Movies WHERE collection = (SELECT MAX(collection) FROM Movies);",
        'Movies with above average ratings': "SELECT m.name, AVG(r.rating) AS avg_rating FROM Movies m JOIN Reviews r ON m.movie_id = r.movie_id GROUP BY m.name HAVING avg_rating > (SELECT AVG(rating) FROM Reviews);"
    }
    query_option = st.selectbox('Select a nested query', list(queries.keys()))
    if st.button('Run Nested Query'):
        query = queries[query_option]
        result = run_query(query)
        if result is not None:
            for row in result:
                st.write(row)

# Group By Queries
with tabs[8]:
    st.header('Group By Queries')
    queries = {
        'Number of movies by each genre': "SELECT genre, COUNT(*) AS num_movies FROM Movies GROUP BY genre;",
        'Average duration of movies by language': "SELECT language, AVG(duration) AS avg_duration FROM Movies GROUP BY language;",
        'List of movies and their awards': "SELECT m.name AS movie_name, a.award_name, a.award_category, a.year FROM Movies m LEFT JOIN Awards a ON m.movie_id = a.movie_id;",
        'Movies with 0 awards': "SELECT m.name AS movie_name FROM Movies m LEFT JOIN Awards a ON m.movie_id = a.movie_id WHERE a.award_id IS NULL;",
        'Rank movies by their collection in descending order': "SELECT m.name, m.collection, RANK() OVER (ORDER BY m.collection DESC) AS collection_rank FROM Movies m;",
        'Movies and their reviews (including movies without reviews and reviews without movies)': "SELECT m.name AS movie_name, r.rating, r.review_text FROM Movies m LEFT JOIN Reviews r ON m.movie_id = r.movie_id UNION ALL SELECT m.name AS movie_name, r.rating, r.review_text FROM Reviews r RIGHT JOIN Movies m ON r.movie_id = m.movie_id WHERE m.movie_id IS NULL OR r.review_id IS NULL;",
        'Movies and their awards (including movies without awards and awards not linked to any movie)': "SELECT m.name AS movie_name, a.award_name, a.award_category, a.year FROM Movies m LEFT JOIN Awards a ON m.movie_id = a.movie_id UNION ALL SELECT m.name AS movie_name, a.award_name, a.award_category, a.year FROM Awards a RIGHT JOIN Movies m ON a.movie_id = m.movie_id WHERE m.movie_id IS NULL OR a.award_id IS NULL;",
        'Streaming platforms and the movies in them': "SELECT sp.platform_name, m.name AS movie_name FROM StreamingPlatform sp RIGHT JOIN Movies m ON sp.movie_id = m.movie_id;"
    }
    query_option = st.selectbox('Select a group by query', list(queries.keys()))
    if st.button('Run Group By Query'):
        query = queries[query_option]
        result = run_query(query)
        if result is not None:
            for row in result:
                st.write(row)