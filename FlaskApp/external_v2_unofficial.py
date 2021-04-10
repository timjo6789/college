#!usr/bin/python3
import re
import mysql.connector
from datetime import datetime
from prettytable import PrettyTable
from mergedeep import merge
import collections

import os


mydb = mysql.connector.connect(
  # host='172.24.96.1',
  host=os.environ['WSL_HOST_IP'],
  user='root',
  password='',
  database='college'
)

cursor = mydb.cursor()

def ensure_connection():
  raise NameError('ensure_connection function is not built')
  pass


def query(query, variables):
  pass