import psycopg2
import os
DATABASE_URL = os.environ['DATABASE_URL']

def get_all_tasks(chat_id):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    command = """SELECT task, status FROM tasks WHERE chat_id='{}';""".format(str(chat_id))
    cur.execute(command)
    records = cur.fetchall()
    cur.close()
    tasks = {}
    for s in records:
        task_name, status  = s
        tasks[task_name] = status
    conn.close()
    return tasks


def insert(chat_id, task, status):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    command_insert = """INSERT INTO tasks (chat_id, task, status) VALUES ('{0}', '{1}', {2});""".format(str(chat_id), task, status)
    cur.execute(command_insert)
    command = """SELECT task, status FROM tasks WHERE chat_id='{}';""".format(str(chat_id))
    cur.execute(command)
    records = cur.fetchall()
    cur.close()
    tasks = {}
    for s in records:
        task_name, status  = s
        tasks[task_name] = status
    conn.close()
    return tasks

def update(chat_id, task, status):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    command_update = """UPDATE tasks SET status={0} WHERE chat_id = '{1}' AND task = '{2}');""".format(status, str(chat_id), task)
    cur.execute(command_insert)
    command = """SELECT task, status FROM tasks WHERE chat_id='{}';""".format(str(chat_id))
    cur.execute(command)
    records = cur.fetchall()
    cur.close()
    tasks = {}
    for s in records:
        task_name, status  = s
        tasks[task_name] = status
    conn.close()
    return tasks

def delete(chat_id, task, status):
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    command_update = """UPDATE tasks SET status={0} WHERE chat_id = '{1}' AND task = '{2}');""".format(status, str(chat_id), task)
    cur.execute(command_insert)
    command = """SELECT task, status FROM tasks WHERE chat_id='{}';""".format(str(chat_id))
    cur.execute(command)
    records = cur.fetchall()
    cur.close()
    tasks = {}
    for s in records:
        task_name, status  = s
        tasks[task_name] = status
    conn.close()
    return tasks


# CREATE TABLE tasks (
#     task_id SERIAL PRIMARY KEY,
#     chat_id VARCHAR(255) NOT NULL,
#     task VARCHAR(255) NOT NULL,
#     status INTEGER  NOT NULL
# )