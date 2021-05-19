import os
import psycopg2
import uuid

con = psycopg2.connect(database=os.environ['POSTGRES_USER'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'], host=os.environ['POSTGRES_HOST'], port=os.environ['POSTGRES_PORT'])


def get_uuid(keys, graph):
    key = '/'.join(keys)

    sherlock_uuid = None

    with con:
        try:
            cur = con.cursor()
            cur.execute(f"SELECT uuid FROM cache WHERE key='{key}'")
            row = cur.fetchone()
            if not row:
                sherlock_uuid = str(uuid.uuid4())
                cur.execute("INSERT INTO cache (graph, key, uuid) VALUES(%s, %s, %s)", (graph, key, sherlock_uuid))
            else:
                sherlock_uuid = row[0]
        except psycopg2.DatabaseError as e:
            print(e)
        # finally:
        #     cur.close()

    return sherlock_uuid


def make_mei_element_sherlock_id(sha1, xmlid):
    return sha1 + '_' + xmlid


def make_tweet_sherlock_id(tweet_id):
    return tweet_id
