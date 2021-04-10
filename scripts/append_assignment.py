#!usr/bin/python3
import re
import mysql.connector
from datetime import datetime
import os

# week = open('input_task.txt', 'r').read().strip()



mydb = mysql.connector.connect(
  # host='172.24.96.1',
  host=os.environ['WSL_HOST_IP'],
  user='root',
  password='',
  database='college'
)

cursor = mydb.cursor(buffered=True)

def get_last_assignment_id():
    cursor.execute('SELECT assignment_id FROM assignment;')
    assignment_id = cursor.fetchall()
    assignment_ids = sorted([x[0] for x in assignment_id])
    return assignment_ids[-1]


# data = open('assignment_input.txt').read().split('\n')
data = open('assignment_input.txt').read().split('\n')

current_assignment_id = None
task_number = 1
for each in data:
    if each == "":
        # skip any empty line
        continue
    if each.startswith('#'):
        # skip any comment
        continue

    if ' ' * 2 not in each:
        class_name, week = each.split(', ')
    elif ' ' * 4 not in each:
        items = each.split(', ')

        # title
        # type
        # deadline
        if len(items) == 0 or len(items) > 3:
            print(f'skipped, insufficient or too much data {items}')
            continue
        value = f'"{class_name}", "{week}", '
        item_types = 'class, week, '
        for item_type, item in zip(['title', 'type', 'deadline'], items):
            item_types += item_type + ', '
            value += '"' + item.replace(' ' * 2, '') + '", '
        item_types = item_types[:-2]
        value = value[:-2]

        query = f'INSERT assignment ({item_types}) VALUES ({value});'
        cursor.execute(query)
        current_assignment_id = get_last_assignment_id()
        print(f"{current_assignment_id},", value)
        task_number = 1
    elif current_assignment_id is not None:
        each = each.replace(' ' * 4, '')
        print(f'    {current_assignment_id}, {task_number}, {each}')
        query = (f'INSERT tasks (assignment_id, task, task_number) VALUES ({current_assignment_id}, "{each}", {task_number});')
        # print('     ', query)
        cursor.execute(query)
        task_number += 1


confirm = input('Does it look good (type y)?: ')
if confirm == 'y':
    print('committed')
    mydb.commit()
else:
    mydb.rollback()
    print('canceled')
