import mysql.connector as mysql
import utils.config as config
import traceback
import pandas as pd


def connect():
    try:
        connection = mysql.connect(
            user=config.user,
            password=config.password,
            database=config.database,
            host=config.host,
            port=config.port
        )
        return connection
    except Exception as err:
        print("Error occurred in making connection …")
        traceback.print_exc()


def create(connection, table_name, columns):
    cursor = connection.cursor()
    query = """
    create table {table_name}(ID int AUTO_INCREMENT primary key""".format(table_name=table_name)
    for column in columns:
        query += ", {key} {value}".format(key=column, value=columns[column])
    query += ");"
    try:
        cursor.execute(query)
        connection.commit()
        print("table created successfully!")
    except Exception as err:
        print(err)
    cursor.close()
    connection.close()


def insert(connection, table_name, values):
    cursor = connection.cursor()
    query = """
    INSERT INTO {table_name}  VALUES {values}""".format(table_name=table_name, values=values)
    try:
        cursor.execute(query)
        connection.commit()
        print("Records inserted successfully!")
    except Exception as err:
        print(err)
    cursor.close()
    connection.close()


def read(connection, table_name):
    cursor = connection.cursor()
    try:
        query = "SELECT * FROM {table_name};".format(table_name=table_name)
        cursor.execute(query)
        record = cursor.fetchall()
        connection.commit()
        print("Read successful")
    except Exception as err:
        print(err)
    cursor.close()
    connection.close()
    return record

def read_top_ranks(connection, where):
    cursor = connection.cursor()
    record = ""
    try:
        query = """select Name, Rating from cafe_df
        join location_df on cafe_df.ID=location_df.ID
        WHERE {key}=N'{value}' COLLATE utf8_persian_ci
        order by  Rating desc, Number_of_Ratings desc
        limit 10;
        """.format(key=list(where.keys())[0], value=list(where.values())[0])
        cursor.execute(query)
        record = cursor.fetchall()
        connection.commit()
        print("Read successful")
    except Exception as err:
        print(err)
    cursor.close()
    connection.close()
    if record:
        return record

def update(connection, table_name, column_name, data, where):
    cursor = connection.cursor()
    query = """
    UPDATE {table_name} SET {column_name}={data} WHERE {key}=N'{value}';
    """.format(table_name=table_name, column_name=column_name, data=data, key=list(where.keys())[0], value=list(where.values())[0])
    try:
        cursor.execute(query)
        connection.commit()
        print("Update successful")
    except Exception as err:
        print(err)
    cursor.close()
    connection.close()


def delete(connection, table_name, where):
    cursor = connection.cursor()
    query = """
    DELETE FROM {table_name} WHERE {key}={value};
    """.format(table_name=table_name, key=list(where.keys())[0], value=list(where.values())[0])
    try:
        cursor.execute(query)
        connection.commit()
        print("Delete successful")
    except Exception as err:
        print(err)
    cursor.close()
    connection.close()

def get_cities(connection):
    cursor = connection.cursor()
    query = """
    SELECT distinct City FROM location_df;
    """
    try:
        cursor.execute(query)
        record = cursor.fetchall()
        connection.commit()
    except Exception as err:
        print(err)
    cursor.close()
    connection.close()
    return  record

def top_restaaturants(connection, tables, city):
    cursor = connection.cursor()
    query = """
        SELECT Name, Rating from cafe_df
        join facilities_df
        on cafe_df.ID=facilities_df.ID
        join location_df
         on cafe_df.ID = location_df.ID
         where City =  city and facilities_df.قلیان = 1
         order by Rating desc, Number_of_Ratings desc
        LIMIT 10
    """

def csv_to_value(df):
    values = ""
    for i in range(len(df)):
        if i > 0:
            values += ","
        values += "({i},".format(i=i+1)
        for j in range(len(df.columns)):
            if j > 0:
                values += ","
            temp = df.iloc[i, j]
            if isinstance(temp, str):
                values += '"' + temp + '"'
            else:
                values += str(temp)
        values += ")"
    values += ";"
    return values


if __name__ == '__main__':
    cafe_df = pd.read_csv('../../Downloads/Telegram Desktop/cafe_df.csv')
    location_df = pd.read_csv('../../Downloads/Telegram Desktop/location_df.csv')
    time_df = pd.read_csv('../../Downloads/Telegram Desktop/time_df.csv')
    facilities_df = pd.read_csv('../../Downloads/Telegram Desktop/facilities_df.csv')
    food_type_df = pd.read_csv('../../Downloads/Telegram Desktop/food_type_df.csv')

    cafe_df_columns = {"Name": "text", "Rating": "float", "Number_of_Ratings": "int"}
    location_df_columns = {"Latitude": "float", "Longitude": "float", "City": "text", "Address": "text"}
    time_df_columns = {"Work_period": "text", "Work_time": "text"}
    facilities_df_columns = {}
    for col in facilities_df.columns:
        facilities_df_columns[col] = "bool"
    food_type_df_columns = {}
    for col in food_type_df.columns:
        food_type_df_columns[col] = "bool"

    cafe_df_values = csv_to_value(cafe_df)
    location_df_values = csv_to_value(location_df)
    time_df_values = csv_to_value(time_df)
    facilities_df_values = csv_to_value(facilities_df)
    food_type_df_values = csv_to_value(food_type_df)

    connection = connect()
    create(connection, "cafe_df", cafe_df_columns)
    connection = connect()
    create(connection, "location_df", location_df_columns)
    connection = connect()
    create(connection, "time_df", time_df_columns)
    connection = connect()
    create(connection, "facilities_df", facilities_df_columns)
    connection = connect()
    create(connection, "food_type_df", food_type_df_columns)

    connection = connect()
    insert(connection, "cafe_df", cafe_df_values)
    connection = connect()
    insert(connection, "location_df", location_df_values)
    connection = connect()
    insert(connection, "time_df", time_df_values)
    connection = connect()
    insert(connection, "facilities_df", facilities_df_values)
    connection = connect()
    insert(connection, "food_type_df", food_type_df_values)
