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


def read_top_ranks_facilities(connection, where):
    cursor = connection.cursor()
    record = ""
    try:
        query = """select cafe_df.Name , Rating, total.total_sum from cafe_df join
    (select facilities_df.ID, sum(قلیان+سفارش_تلفنی
                   +اینترنت_رایگان+
               DJ+بازی_و_سرگرمی+سیگار_آزاد+فضای_باز+شبانه_روزی
                   +چشم_انداز+بوفه+دسترسی_ویلچر+
               فضای_بازی_کودک+موسیقی_زنده+پارکینگ
               ) as total_sum from
                    facilities_df
    group by facilities_df.ID) total on cafe_df.ID = total.ID
         JOIN location_df on cafe_df.ID = location_df.ID
             where  {key}=N'{value}' COLLATE utf8_persian_ci
    group by cafe_df.ID
    order by cafe_df.Rating desc, cafe_df.Number_of_Ratings desc
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


def read_best_facilities(connection, where):
    cursor = connection.cursor()
    record = ""
    try:
        query = """select  sum(سفارش_تلفنی) 'سفارش تلفنی',
                           sum(بازی_و_سرگرمی) 'بازی و سرگرمی',
                           sum(موسیقی_زنده) 'موسیقی زنده',
                           sum(قلیان) 'قلیان',
                           sum(اینترنت_رایگان) 'اینترنت رایگان',
                           sum(سیگار_آزاد) 'سیگار آزاد',
                           sum(فضای_باز) 'فضای باز',
                           sum(شبانه_روزی) 'شبانه روزی',
                           sum(چشم_انداز) 'چشم انداز',
                           sum(پارکینگ) 'پارکینگ',
                           sum(بوفه) 'بوفه',
                           sum(دسترسی_ویلچر) 'دسترسی ویلچر',
                           sum(DJ) 'DJ',
                           sum(فضای_بازی_کودک)  'فضای بازی کودک' from (select facilities_df.* from cafe_df
                    join facilities_df on cafe_df.ID= facilities_df.ID
                    join location_df on cafe_df.ID = location_df.ID
                    where  {key}=N'{value}' COLLATE utf8_persian_ci
                    order by cafe_df.Rating desc , cafe_df.Number_of_Ratings desc
                    limit 50) t;
        """.format(key=list(where.keys())[0], value=list(where.values())[0])
        cursor.execute(query)
        field_names = [i[0] for i in cursor.description]
        record = cursor.fetchall()
        connection.commit()
        print("Read successful")
    except Exception as err:
        print(err)
    cursor.close()
    connection.close()
    if record:
        return record,field_names


def read_time_average(connection, where):
    cursor = connection.cursor()
    record = ""
    try:
        query = """select sec_to_time(avg(TIME_TO_SEC(t.working_hours))) time,
                    case
                        when Rating between 0 and 2.5 then '0 - 2.5'
                        when Rating between 2.5 and 5 then '2.5 - 5'
                        when Rating between 5 and 7.5 then '5 - 7.5'
                        when Rating between 7.5 and 10 then '7.5 - 10'
                    end as rate_range
                from(select Name, Rating, Number_of_Ratings, timediff(Close_time,Open_time) 'working_hours' from cafe_df
                join time_df on cafe_df.ID=time_df.ID
                join location_df on cafe_df.ID = location_df.ID
                where  {key}=N'{value}' COLLATE utf8_persian_ci
                order by working_hours desc
                limit 50) t
                group by rate_range
                order by time;
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


def read_rating_variant_foodtype(connection, where):
    cursor = connection.cursor()
    record = ""
    try:
        query = """select cd.Name, cd.Rating, sum(فرنگی+فرانسوی+ایتالیایی+ایرانی+چینی+کره_ای+گیاهی+ژاپنی+عربی+افغانی+ترکیه_ای+کیک_و_شیرینی+سالاد+پیتزا
                        +استیک+پاستا+کباب+ساندویچ+املت_و_نیمرو+محلی+دیزی+سوخاری+برگر+مدیترانه_ای+هندی+سوشی+گیلکی+ماهی
                        +فرنگی+فرانسوی+ایتالیایی+ایرانی+چینی+کره_ای+گیاهی+ژاپنی+عربی+افغانی+ترکیه_ای+کیک_و_شیرینی+سالاد
                        +پیتزا+استیک+پاستا+کباب+ساندویچ+املت_و_نیمرو+محلی+دیزی+سوخاری+برگر+مدیترانه_ای+هندی+سوشی+گیلکی
                    +ماهی+آش+لازانیا+سوپ+غذای_دریایی+میگو+حلیم+کله_پاچه) as food_type from food_type_df
                    join cafe_df cd on food_type_df.ID = cd.ID
                    join location_df on cd.ID = location_df.ID
                    where  {key}=N'{value}' COLLATE utf8_persian_ci
                    group by cd.ID
                    order by food_type desc
                    limit 10
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

def read_cities_with_most_top_restaurants(connection):
    cursor = connection.cursor()
    record = ""
    try:
        query = """select City, count(Name) from(select Name, Rating, Number_of_Ratings, City from cafe_df
                    join location_df on cafe_df.ID = location_df.ID
                    order by Rating desc , Number_of_Ratings desc
                    limit 100) t
                    group by City
                    order by count(Name) desc;
                    """
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
