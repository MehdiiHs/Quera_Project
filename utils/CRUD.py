import mysql.connector as mysql
from utils import config
import traceback


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
        return record
        connection.commit()
        print("Read successful")
    except Exception as err:
        print(err)
    cursor.close()
    connection.close()


def update(connection, table_name, column_name, data, where):
    cursor = connection.cursor()
    query = """
    UPDATE {table_name} SET {column_name}={data} WHERE {key}={value};
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



