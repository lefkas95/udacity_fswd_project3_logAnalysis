#!/usr/bin/env python3

import datetime
import psycopg2

DBNAME = "news"


def get_most_popular_articles(cursor):
    ''' Returns the three most visited articles and their total view count. '''
    
    cursor.execute("""
                    select a.title, count(*) as num from articles as a JOIN log
                    as l ON l.path = concat('/article/', a.slug) group by
                    a.id order by num DESC LIMIT 3;
    """)

    return cursor.fetchall()


def get_most_popular_authors(cursor):
    ''' Returns the authors and summed up article-views orderd by their view-counts '''
    cursor.execute("""
                    select au.name, sum(x.num) from authors as au JOIN
                    (select a.author, a.slug, count(*) as num from articles
                    as a JOIN log as l ON l.path =
                    concat('/article/', a.slug) group by a.id)
                    as x ON au.id = x.author group by au.id;
    """)

    return cursor.fetchall()


def get_request_errors(cursor):
    ''' As "select status, count(*) from log group by status;" showed there are
    only the status 200 and 404. So I don't include other 2xx or 3xx status '''

    # limit to 500 just in case - to not overload the client
    cursor.execute("""
                    select ok.date, ok.num, error.num
                    from (select count(*) as num, date(time) from log
                    where status = '200 OK' group by date(time)) as ok JOIN
                    (select count(*) as num, date(time) from log
                    where status = '404 NOT FOUND' group by date(time))
                    as error ON ok.date = error.date
                    where (100 * error.num > ok.num) limit 500;
    """)

    return cursor.fetchall()


print("Starting calculation. Please be patient...")

db = psycopg2.connect(database=DBNAME)
c = db.cursor()

articles = get_most_popular_articles(c)
authors = get_most_popular_authors(c)
errors = get_request_errors(c)

print("\n\nThe three most popular articles are\n")
for article in articles:
    print("\"" + article[0] + "\" - " + str(article[1]) + " views.")


print("\n\nThe most popular authors are\n")
for author in authors:
    print(author[0] + " - " + str(author[1]) + " views.")

print("\n\nOn these days more than 1% of all requests had an error\n")
for error in errors:
    print(error[0].strftime("%Y-%m-%d") + " - "
          + str(round(error[2] * 100.0 / (error[1] + error[2]), 2)) + "% errors.")
if(len(errors) == 500):
    print("(first 500 records)")

db.close()
