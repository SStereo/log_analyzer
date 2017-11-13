#!/usr/bin/env python2.7

import psycopg2

OUTPUT_COL1 = 35   # width for output column 1
OUTPUT_COL2 = 15   # width for output column 2
OUTPUT_SEP = ': '  # column separator for output


def view_exists(view_name):
    # Establish db connection and create a cursor
    db = psycopg2.connect("dbname=news")
    c = db.cursor()

    # Validates if the view already exists and creates it if it is missing
    SQL = """SELECT EXISTS(SELECT 1 FROM information_schema.tables
             WHERE table_catalog='news' AND
                    table_schema='public' AND
                    table_name=%s);"""
    data = (view_name,)
    c.execute(SQL, data)
    results = c.fetchone()
    return results[0]


def show_popular_articles(max_articles):
    # Establish db connection and create a cursor
    db = psycopg2.connect("dbname=news")
    c = db.cursor()

    # Creates the view if it does not exist
    if not view_exists('toparticles'):
        # Creates a view that sorts all articles by number of page views
        print("Creating toparticles view ...")
        SQL = """CREATE VIEW toparticles AS
                 SELECT articles.title, count(log.path) AS visits
                 FROM articles
                 LEFT JOIN log ON log.path LIKE concat('%%',articles.slug)
                 GROUP BY articles.title
                 ORDER BY visits desc;"""
        c.execute(SQL)
        db.commit()

    # RESULT 1: Selects the top articles based on passed max_articles argument
    SQL = """SELECT * FROM toparticles LIMIT %s;"""
    data = (str(max_articles),)
    c.execute(SQL, data)
    results = c.fetchall()

    # Output of the results
    print ("""\n""")
    print ("Top "+str(max_articles)+" most popular articles")
    print ("-".ljust(OUTPUT_COL1 + OUTPUT_COL2 + 2, "-"))
    for r in results:
        value1 = str(r[0])
        value2 = "{:,}".format(r[1]) + " views"
        column1 = value1.ljust(OUTPUT_COL1)
        column2 = value2.rjust(OUTPUT_COL2)
        print (column1+OUTPUT_SEP+column2)

    # Closes the db connection
    db.close()


def show_popular_authors():
    # Establish db connection and create a cursor
    db = psycopg2.connect("dbname=news")
    c = db.cursor()

    # RESULT 2: Shows authors per total number of views
    SQL = """SELECT authors.name, sum(toparticles.visits) as totalviews
            FROM authors, articles, toparticles
            WHERE authors.id = articles.author
            AND articles.title = toparticles.title
            GROUP BY authors.name
            ORDER BY totalviews DESC;"""
    c.execute(SQL)
    results = c.fetchall()

    # Output of the results
    print ("""\n""")
    print ("Most popular authors")
    print ("-".ljust(OUTPUT_COL1 + OUTPUT_COL2 + 2, "-"))
    for r in results:
        value1 = str(r[0])
        value2 = "{:,}".format(r[1]) + " views"
        column1 = value1.ljust(OUTPUT_COL1)
        column2 = value2.rjust(OUTPUT_COL2)
        print (column1+OUTPUT_SEP+column2)

    # Closes the db connection
    db.close()


def show_bad_day():
    # Establish db connection and create a cursor
    db = psycopg2.connect("dbname=news")
    c = db.cursor()

    # Creates the view if it does not exist
    if not view_exists('totalvisits'):
        # Creates a view that counts all visits per day
        SQL = """CREATE VIEW totalvisits AS
                SELECT date_trunc('day', log.time) AS date, count(*)
                FROM log
                GROUP BY date;"""
        c.execute(SQL)
        db.commit()

    # Creates the view if it does not exist
    if not view_exists('errorvisits'):
        # Creates a VIEW that counts all visits with status code 4 or 5
        SQL = """CREATE VIEW errorvisits AS
                SELECT date_trunc('day', log.time) AS date, count(*)
                FROM log
                WHERE left(log.status,1) = '4' OR left(log.status,1) = '5'
                GROUP BY date;"""
        c.execute(SQL)
        db.commit()

    # RESULT 3: Day with more than 1 percent error views
    SQL = """SELECT to_char(totalvisits.date,'DDth FMMonth YYYY'),
            round((errorvisits.count::decimal * 100/totalvisits.count),2)
            FROM totalvisits
            LEFT JOIN errorvisits
            ON totalvisits.date = errorvisits.date
            WHERE round(
                  (errorvisits.count::decimal * 100/totalvisits.count),2
                       ) > 1;"""
    c.execute(SQL)
    results = c.fetchall()

    # Output of the results
    print ("""\n""")
    print ("""Days with more than 1% errors""")
    print ("-".ljust(OUTPUT_COL1 + OUTPUT_COL2 + 2, "-"))
    for r in results:
        value1 = str(r[0])
        value2 = str(r[1]) + "% errors"
        column1 = value1.ljust(OUTPUT_COL1)
        column2 = value2.rjust(OUTPUT_COL2)
        print (column1+OUTPUT_SEP+column2)

    # Closes the db connection
    db.close()


if __name__ == '__main__':
    print ("Analyzing log data ...\n")
    show_popular_articles(3)
    show_popular_authors()
    show_bad_day()
