#!usr/bin/python3
import re
import mysql.connector
from datetime import datetime
from prettytable import PrettyTable
from mergedeep import merge
import collections

import os

def create_connection(host='10.0.0.244', user='root', password='42', database='college'):
  mydb = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
  )
  return mydb, mydb.cursor()

# convert google stopwatch into seconds
def convert_stopwatch_to_second(string):
  hour, minute, second = re.match(r'(?:(\d+)h)?(?:(\d+)?m)?(\d+)s.*', string).groups()
  hour = 0 if hour is None else int(hour)
  minute = 0 if minute is None else int(minute)
  second = int(second)
  return hour * 3600 + minute * 60 + second




def add_time(assignment_id, task_number, duration):
    mydb, cursor = create_connection()
    print(duration)
    if type(duration) is str:
      try:
        duration = int(duration)
      except:
        duration = convert_stopwatch_to_second(duration)
    query = ("""UPDATE assignment JOIN tasks USING (assignment_id)
              SET Duration = Duration + %s
              WHERE assignment_id = %s AND task_number = %s;""")
    cursor.execute(query, (duration, assignment_id, task_number))
    mydb.commit()


def general_get_assignment_id(title, week=None, a_class=None):
    mydb, cursor = create_connection()
    query = 'SELECT class, assignment_id, week, title\nFROM assignment\nWHERE title = %s'
    if a_class is not None:
        query += ' AND class = %s'
    if week is not None:
        query += ' AND week = %s'
    query += ';'
    query = (query)

    if a_class is not None and week is not None:
        cursor.execute(query, (title, a_class, week))
    elif a_class is not None:
        cursor.execute(query, (title, a_class))
    elif week is not None:
        cursor.execute(query, (title, week))
    else:
        cursor.execute(query, (title,))

    result = cursor.fetchall()

    for each in result:
      print(each)


def mark_done(assignment_id, task_number, duration, date_completed):
  mydb, cursor = create_connection()
  if type(duration) is str:
      duration = convert_stopwatch_to_second(duration)
  query = ("""UPDATE assignment JOIN tasks USING (assignment_id)
              SET Duration = %s, Done = 1, date_completed = %s
              WHERE assignment_id = %s AND task_number = %s;""")
  cursor.execute(query, (duration, date_completed, assignment_id, task_number))
  mydb.commit()


def mark_done_without_duration(assignment_id, task_number, date_completed):
  mydb, cursor = create_connection()
  query = ("""UPDATE assignment JOIN tasks USING (assignment_id)
              SET Done = 1, date_completed = %s
              WHERE assignment_id = %s AND task_number = %s;""")
  cursor.execute(query, (date_completed, assignment_id, task_number))
  mydb.commit()


def mark_undone(assignment_id, task_number, reset_seconds=True):
  mydb, cursor = create_connection()
  if reset_seconds:
    query = ("""UPDATE assignment JOIN tasks USING (assignment_id)
                SET Duration = 0, Done = 0, date_completed = NULL
                WHERE assignment_id = %s AND task_number = %s;""")
    cursor.execute(query, (assignment_id, task_number))
    mydb.commit()
  else:
    query = ("""UPDATE assignment JOIN tasks USING (assignment_id)
                SET Done = 0, date_completed = NULL
                WHERE assignment_id = %s AND task_number = %s;""")
    cursor.execute(query, (assignment_id, task_number))
    mydb.commit()


def get_task_list(assignment_id):
  mydb, cursor = create_connection()
  details = ''
  query = ("SELECT task_number, PRETTY_TIME(duration), task, done, date_completed FROM tasks WHERE assignment_id = %s;")
  cursor.execute(query, (assignment_id,));
  result = cursor.fetchall()
  a_list = ['task: ', 'duration: ', 'Description: ', 'status: ', 'date completed: ']
  for each in result:
    for item, pair in zip(each, a_list):
      if pair == 'status: ':
        details += pair + ('Finished' if item == 1 else 'in progress') + '\n'
      else:
        details += pair + str(item) + '\n'
    details += '\n'
  print(details)

def left_to_do(week=None, a_class=None):
  mydb, cursor = create_connection()
  query = "SELECT assignment_id, class, week, title, DATE_FORMAT(deadline, '%m-%d-%Y') FROM assignment JOIN tasks USING (assignment_id)"
  if week is not None and a_class is not None:
    query += f' WHERE done = 0 AND week = "{week}" AND class = "{a_class}" '
  elif week is not None or a_class is not None:
    query += ' WHERE done = 0 AND '
    if week is not None:
      query += f'week = "{week}" '
    elif a_class is not None:
      query += f'class = "{a_class}" '
  else:
    query += ' WHERE done = 0 '
  query += 'GROUP BY class, title ORDER BY class, deadline;'
  query = (query)
  cursor.execute(query)
  result = cursor.fetchall()
  for each in result:
    print(each)

def get_assignment_tasks(week, done=0):
  mydb, cursor = create_connection()

  query = ("SELECT class, assignment_id, title, DAYNAME(deadline) FROM assignment JOIN tasks USING (assignment_id) WHERE week = %s AND done = %s GROUP BY assignment_id ORDER BY class, assignment_id;")
  # query = ("SELECT class, assignment_id, title, DAYNAME(deadline) FROM assignment JOIN tasks USING (assignment_id) WHERE week = %s GROUP BY assignment_id ORDER BY class, assignment_id;")
  cursor.execute(query, (week, done))
  assignments = cursor.fetchall()

  query = ("SELECT class, assignment_id, task_number, task, duration FROM assignment JOIN tasks USING (assignment_id) WHERE week = %s AND done = %s ORDER BY class, assignment_id, task_number;")
  # query = ("SELECT class, assignment_id, task_number, task, duration FROM assignment JOIN tasks USING (assignment_id) WHERE week = %s ORDER BY class, assignment_id, task_number;")
  cursor.execute(query, (week, done))
  tasks = cursor.fetchall()
  mydb.commit()

  a_dict = {}

  for each in assignments:
      each_class, each_assignment_id, each_title, deadline = each
      a_dict.setdefault(each_class, {})
      a_dict[each_class].setdefault(each_assignment_id, {'title':each_title, 'due': 'No due date' if deadline is None else deadline})

  for each in tasks:
      each_class, each_assignment_id, each_task, each_description, each_duration = each
      a_dict[each_class][each_assignment_id].setdefault('task', [])
      a_dict[each_class][each_assignment_id]['task'].append(each_description)

      a_dict[each_class][each_assignment_id].setdefault('task_number', [])
      a_dict[each_class][each_assignment_id]['task_number'].append(each_task)

      a_dict[each_class][each_assignment_id].setdefault('duration', [])
      a_dict[each_class][each_assignment_id]['duration'].append(each_duration)

  output = ''
  for class_key, class_value in a_dict.items():
      output += class_key + '\n'
      i = 1
      for assignment_id_key, assignment_id_value in class_value.items():
          if len(assignment_id_value['task']) > 1:
              output += f" {assignment_id_key}, {assignment_id_value['title']}, {assignment_id_value['due']}" + '\n'
              for task, task_number in zip(assignment_id_value['task'], assignment_id_value['task_number']):
                  output += f'  {task_number} - {task}' + '\n'
          else:
              output += f" {assignment_id_key}, {assignment_id_value['title']}, {assignment_id_value['due']} - {assignment_id_value['task_number'][0]} - {assignment_id_value['task'][0]}" + '\n'
          i += 1
      output += '\n'
  return a_dict


def order_dict(dictionary):
    mydb, cursor = create_connection()
    return {k: order_dict(v) if isinstance(v, dict) else v
            for k, v in sorted(dictionary.items())}


def get_multiple_assignment_tasks(weeks, done=0):
  mydb, cursor = create_connection()
  a_dict = {}
  weeks = [int(x.replace('W', '')) for x in weeks]
  weeks = [f'W{x:02}' for x in range(weeks[0], weeks[1]+1)]
  for each in weeks:
    merge(a_dict, get_assignment_tasks(each, done))
    print(each)
  # return a_dict
  # return dict(sorted(a_dict.items()))
  # sorted(a_dict.items(), key = lambda x: x[1])
  # a_dict.sort(key=lambda x: x[1])
  # order_dict(a_dict)
  return a_dict

def load_mysql_script(relative_path):
  mydb, cursor = create_connection()
  return open(os.path.join(os.path.dirname(__file__), f'mysql_script_files/{relative_path}')).read()



def get_table(start_date, end_date):
  mydb, cursor = create_connection()
  date_range = f'{start_date} - {end_date}'
  fields = ['class', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', date_range]

  query = load_mysql_script('time_table.txt')
  cursor.execute(query, (date_range, start_date, end_date))

  time_table = list(cursor.fetchall())
  time_table = [list(x) for x in time_table]

  pretty = PrettyTable(fields)

  pretty.align['class'] = 'l'
  pretty.align['Sunday'] = 'r'
  pretty.align['Monday'] = 'r'
  pretty.align['Tuesday'] = 'r'
  pretty.align['Wednesday'] = 'r'
  pretty.align['Thursday'] = 'r'
  pretty.align['Friday'] = 'r'
  pretty.align['Saturday'] = 'r'
  pretty.align[date_range] = 'r'

  time_table[-1][0] = 'total' # renaming None to total in class column
  [pretty.add_row(x) for x in time_table]

  print(pretty)


def missing_tasks(week):
  mydb, cursor = create_connection()
  query = ("SELECT CONCAT(ASSIGNMENT_ID, ', 1, ""') AS ID FROM ASSIGNMENT WHERE ASSIGNMENT_ID NOT IN (SELECT ASSIGNMENT_ID FROM TASKS) AND WEEK = %s ORDER BY CLASS;")
  cursor.execute(query, (week,))
  construct_task_fill = cursor.fetchall()
  for each in construct_task_fill:
    print(''.join(each))

  query = ("SELECT ASSIGNMENT_ID as ID, CLASS, TITLE FROM ASSIGNMENT WHERE ASSIGNMENT_ID NOT IN (SELECT ASSIGNMENT_ID FROM TASKS) AND WEEK = %s ORDER BY CLASS;")
  cursor.execute(query, (week,))
  construct_assignment_reference = cursor.fetchall()
  current_class = '-42'
  for ID, Class, title in construct_assignment_reference:
    if current_class != Class:
      current_class = Class
      print()
      print(Class)
    print(ID, title, sep=', ')


def create_assignment(assignment_name, class_name, week, deadline):
  mydb, cursor = create_connection()
  query = ("SELECT * FROM ASSIGNMENT WHERE title = %s AND class = %s AND week = %s AND IF(deadline is not null, deadline = %s, deadline is null)")
  cursor.execute(query, (assignment_name, class_name, week, deadline))
  information = cursor.fetchall()
  if len(information) > 0:
    print('looks like assignment exists, check below')
    print(information)
  else:
    query = ("INSERT ASSIGNMENT (TITLE, CLASS, WEEK, DEADLINE) VALUES (%s, %s, %s, %s);")
    cursor.execute(query, (assignment_name, class_name, week, deadline))
    if input('seems good? (y/n) ') in ['yes', 'y']:
      mydb.commit()
      query = ("SELECT * FROM ASSIGNMENT WHERE title = %s AND class = %s AND week = %s AND IF(deadline is not null, deadline = %s, deadline is null)")
      cursor.execute(query, (assignment_name, class_name, week, deadline))
      print(cursor.fetchall())
    else:
      print('canceled')


def delete_assignment(assignment_id):
  mydb, cursor = create_connection()
  query = ("SELECT * FROM assignment JOIN tasks USING (assignment_id) WHERE assignment_id = %s")
  cursor.execute(query, (assignment_id,))
  information = cursor.fetchall()

  print('these information will be deleted')
  print(information)

  if input('are you sure? (y/n)') in ['yes', 'y']:
    query = ("DELETE tasks WHERE assignment_id = %s")
    cursor.execute(query, (assignment_id))

    query = ("DELETE assignment WHERE assignment_id = %s")
    cursor.execute(query, (assignment_id))
    if input('They have been prepared to be deleted, permenantly delete? (y/n)') in ['yes', 'y']:
      mydb.commit()
      print('Deleted')
    else:
      print('They are not deleted.')
  else:
    print('canceled')


def delete_task(assignment_id, task_number):
  mydb, cursor = create_connection()
  query = ("SELECT * FROM tasks USING (assignment_id) WHERE assignment_id = %s AND task_number = %s")
  cursor.execute(query, (assignment_id, task_number))
  information = cursor.fetchall()

  print('This task will be deleted')
  print(information)

  if input('are you sure? (y/n)') in ['yes', 'y']:
    query = ("DELETE tasks WHERE assignment_id = %s AND task_number = %s")
    cursor.execute(query, (assignment_id))

    if input('They have been prepared to be deleted, permenantly delete? (y/n)') in ['yes', 'y']:
      mydb.commit()
      print('Deleted')
    else:
      print('They are not deleted.')
  else:
    print('canceled')


def create_task(assignment_id, task_number, task_title): # , duration, done, date_completed):
  mydb, cursor = create_connection()
  query = ("SELECT * FROM TASKS WHERE assignment_id = %s AND task_number = %s")
  # AND task = %s AND duration = %s AND IF(done is not null, done = %s, done is null) AND IF(date_completed is not null, date_completed = %s, date_completed is null)
  cursor.execute(query, (assignment_id, task_number))
  information = cursor.fetchall()
  if len(information) > 0:
    print('looks like task exists, check below')
    print(information)
  else:
    query = ("INSERT TASKS (assignment_id, task_number, task) VALUES (%s, %s, %s);")
    cursor.execute(query, (assignment_id, task_number, task_title))
    if input('seems good? (y/n) ') in ['yes', 'y']:
      mydb.commit()
      query = ("SELECT * FROM TASKS WHERE assignment_id = %s AND task_number = %s")
      cursor.execute(query, (assignment_id, task_number))
      information = cursor.fetchall()
    else:
      print('canceled')


def update_task(assignment_id, task_number, task_title, duration, done, date_completed):
  pass


def write_complete_to_mysql(file_path, date_tag="", command="em mark-done-duration"):
  mydb, cursor = create_connection()
  if date_tag != '':
    date_tag = f' -d {date_tag}'

  sample_input = open(file_path).read()

  single_task_regex = r"^ (\d+).*(?: - (\d) - .*)- (.*s)$" # captures assignment number with single task and time stamp
  results = re.findall(single_task_regex, sample_input, re.MULTILINE)
  command = "em mark-done-duration"

  for assignment_id, task, time_stamp in results:
    each = f'{command} {assignment_id} {task} {time_stamp}'
    each += date_tag if date_tag != '' else ''
    print(each)
    # print(command, assignment_id, task, time_stamp, date_tag)



  # captures the multiple lines to be regex into small pieces
  results_multi_line = re.findall(r"\d*.*(?:\n  .*)+", sample_input, re.MULTILINE)

  # captures the assignment id per task_group
  results_assignment_ids = [re.findall(r"^ \d+", x, re.MULTILINE) for x in results_multi_line]
  # captures the task number with time stamp
  results_tasks = [re.findall(r"^  (\d+).*- (.*s)$", x, re.MULTILINE) for x in results_multi_line]

  if len(results_assignment_ids) != len(results_tasks):
    raise re.error("multiline mismatch error")

  for assignment_id_list, tasks in zip(results_assignment_ids, results_tasks):
    assignment_id = int(assignment_id_list[0])
    for task, time_stamp in tasks:
      each = f'{command} {assignment_id} {task} {time_stamp}'
      each += date_tag if date_tag != '' else ''
      print(each)
