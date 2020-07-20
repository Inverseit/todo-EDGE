import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
test_command =  """INSERT INTO tasks (chat_id, task, status) VALUES ("123", "nts", 0);"""
cur.execute(test_command)
cur.close()

conn.commit()
conn.close()

# CREATE TABLE tasks (
#     task_id SERIAL PRIMARY KEY,
#     chat_id VARCHAR(255) NOT NULL,
#     task VARCHAR(255) NOT NULL,
#     status INTEGER  NOT NULL
# )