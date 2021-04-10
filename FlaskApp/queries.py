import re
import mysql.connector
from datetime import datetime
import platform

mydb = mysql.connector.connect(
  host='172.24.96.1',
  user='root',
  # password='',
  database='college'
)

# convert google stopwatch into seconds
def convert_stopwatch_to_second(string):
  hour, minute, second = re.match(r'(?:(\d+)h)?(?:(\d+)?m)?(\d+)s.*', string).groups()
  hour = 0 if hour is None else int(hour)
  minute = 0 if minute is None else int(minute)
  second = int(second)
  return hour * 3600 + minute * 60 + second

def class_specific(week, a_class):
  query = ("""SELECT assignment_id, class, week, title, DATE_FORMAT(deadline, "%M %d, %Y")
              FROM assignment JOIN tasks USING (assignment_id)
              WHERE week = %s AND done = 0 AND class = %s GROUP BY class, title
              ORDER BY class, deadline;""")
  cursor.execute(query, (week, a_class))
  result = cursor.fetchall()
  return result
cursor = mydb.cursor()
