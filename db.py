import os
import psycopg2

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')
cur = conn.cursor()
# test_command =  """INSERT INTO tasks (chat_id, task, status) VALUES ('12345', 'nts11', 1);"""
test_command1 = """SELECT task, status FROM tasks WHERE chat_id='123';"""
cur.execute(test_command1)
records = cur.fetchall()
cur.close()
tasks = {}
for s in records:
    task_name, status  = s
    tasks[task_name] = status
for key, value in tasks.items():
    print("{0} has status {1}".format(key, value))
conn.commit()
conn.close()

# CREATE TABLE tasks (
#     task_id SERIAL PRIMARY KEY,
#     chat_id VARCHAR(255) NOT NULL,
#     task VARCHAR(255) NOT NULL,
#     status INTEGER  NOT NULL
# )