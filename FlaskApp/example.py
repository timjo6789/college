import re
import mysql.connector
from datetime import datetime
import platform

mydb = mysql.connector.connect(
  host='localhost',
  user='root',
  password='simple and fun',
  database='college'
)

# convert google stopwatch into seconds
def convert_stopwatch_to_second(string):
  hour, minute, second = re.match(r'(?:(\d+)h)?(?:(\d+)?m)?(\d+)s.*', string).groups()
  hour = 0 if hour is None else int(hour)
  minute = 0 if minute is None else int(minute)
  second = int(second)
  return hour * 3600 + minute * 60 + second


cursor = mydb.cursor()


def general_get_assignment_id(title, week=None, a_class=None):
  query = 'SELECT assignment_id, class, week, title\nFROM assignment\nWHERE title = %s'
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
  return result

def get_assignment_id(a_class, week, title):
  query = ("""SELECT assignment_id
           FROM assignment
           WHERE class = %s AND week = %s AND title = %s;""")
  cursor.execute(query, (a_class, week, title))
  result = cursor.fetchone()
  if result is not None:
    return result[0]

def mark_done(assignment_id, task_number, duration, date_completed):
  query = ("""UPDATE assignment JOIN tasks USING (assignment_id)
              SET Duration = %s, Done = 1, date_completed = %s
              WHERE assignment_id = %s AND task_number = %s;""")
  cursor.execute(query, (duration, date_completed, assignment_id, task_number))
  mydb.commit()

def mark_done_without_duration(assignment_id, task_number, date_completed):
  query = ("""UPDATE assignment JOIN tasks USING (assignment_id)
              SET Done = 1, date_completed = %s
              WHERE assignment_id = %s AND task_number = %s;""")
  cursor.execute(query, (date_completed, assignment_id, task_number))
  mydb.commit()

def mark_undone(assignment_id, task_number):
  query = ("""UPDATE assignment JOIN tasks USING (assignment_id)
              SET Duration = 0, Done = 0, date_completed = NULL
              WHERE assignment_id = %s AND task_number = %s;""")
  cursor.execute(query, (assignment_id, task_number))
  mydb.commit()

def add_time(assignment_id, task_number, duration):
  query = ("""UPDATE assignment JOIN tasks USING (assignment_id)
              SET Duration = Duration + %s
              WHERE assignment_id = %s AND task_number = %s;""")
  cursor.execute(query, (duration, assignment_id, task_number))
  mydb.commit()

def get_task_list(assignment_id):
  details = ''
  query = ("SELECT task_number, PRETTY_TIME(duration), task, done, date_completed FROM tasks WHERE assignment_id = %s;")
  cursor.execute(query, (assignment_id,));
  result = cursor.fetchall()
  a_list = ['task: ', 'duration: ', 'Description: ', 'status: ', 'date completed: ']
  for each in result:
    for item, pair in zip(each, a_list):
      if pair == 'status: ':
        details += pair + ('Finished' if item == 1 else 'in progress') + '<br>'
      else:
        details += pair + str(item) + '<br>'
    details += '<br>'
  return details

# usages
# general_get_assignment_id(title, week, a_class)
# get_task_list(assignment_id)
# mark_done(assignment_id, task_number, duration, date_completed)
# mark_done_without_duration(assignment_id, task_number, date_completed)
# add_time(assignment_id, task_number)


# gather details to add to the web
details = ''

# day can be automatically set to today
date_completed = datetime.now().strftime('%Y-%m-%d')

# set the day that it is completed as YYYY-MM-DD format
# date_completed = '2020-09-15'


# get id from assignment name
an_id = general_get_assignment_id('Team Activity', 'W01')
details += str(an_id) + '<br>'
details +=  ', '.join([str(each[0]) for each in an_id]) + '<br>' # ids
# decide which one then assign it here
assignment_id = 179
details += '<br><br>'

query = ("SELECT assignment_id, title, class, week FROM assignment WHERE assignment_id = %s;")
cursor.execute(query, (assignment_id,));
result = cursor.fetchone()
details += 'current ' + str(result) + '<br><br>'


# then decide which task to work on then assign it here
task_number = 2

# use either google or manual seconds here
# add_time(assignment_id, task_number, convert_stopwatch_to_second('4m27s49'))
# add_time(assignment_id, task_number, 0)

# when done, run this
# mark_done_without_duration(assignment_id, task_number, date_completed)

# only run this if duration was never added or set
# mark_done(assignment_id, task_number, 0, date_completed)
# mark_done(assignment_id, task_number, convert_stopwatch_to_second('24s86'), date_completed)

# show task list
details += get_task_list(assignment_id)


def close():
  cursor.close()
  mydb.close()


if __name__ == '__main__':
  if platform.system() == 'Windows':
    open(r'\\wsl$\Ubuntu\var\www\html\index.html', 'w').write(details)
  elif platform.system() == 'Linux':
    open('/var/www/html/index.html', 'w').write(details)