#!usr/bin/python3
import click
import external
from datetime import datetime, timedelta


@click.group()
def main():
  pass


@main.command()
@click.argument('assignment_id')
@click.argument('task_number')
@click.argument('duration')
def add_time(assignment_id, task_number, duration):
  external.add_time(assignment_id, task_number, duration)


@main.command()
@click.argument('title')
@click.option('--week', '-w')
@click.option('--a_class', '-c')
def get_id(title, week, a_class):
  external.general_get_assignment_id(title, week, a_class)


@main.command()
@click.argument('assignment_id')
@click.argument('task_number')
@click.option('--date_completed', '-d')
def mark_done(assignment_id, task_number, date_completed):
  """if date_completed is not used then it automatically sets to today date."""
  if date_completed is None:
    date_completed = datetime.now().strftime('%Y-%m-%d')
  external.mark_done_without_duration(assignment_id, task_number, date_completed)


@main.command()
@click.argument('assignment_id')
@click.argument('task_number')
@click.argument('duration')
@click.option('--date_completed', '-d')
def mark_done_duration(assignment_id, task_number, duration, date_completed):
  """if date_completed is not used then it automatically sets to today date."""
  if date_completed is None:
    date_completed = datetime.now().strftime('%Y-%m-%d')
  external.mark_done(assignment_id, task_number, duration, date_completed)


@main.command()
@click.argument('assignment_id')
@click.argument('task_number')
def mark_undone(assignment_id, task_number):
  external.mark_undone(assignment_id, task_number, False)


@main.command()
@click.argument('assignment_id')
@click.argument('task_number')
def mark_undone_fully(assignment_id, task_number):
  external.mark_undone(assignment_id, task_number)


@main.command()
@click.argument('assignment_id')
def task_list(assignment_id):
  external.get_task_list(assignment_id)


@main.command()
@click.option('--week', '-w')
@click.option('--a_class', '-c')
def tasks(week, a_class):
  external.left_to_do(week, a_class)


@main.command()
@click.argument('week')
def assignment_tasks(week):
  print('Saved at /home/tgj2u2/notes/Fall 2020/weekly_focus/output.txt')
  print('quick access')
  print(r"\\wsl$\Ubuntu\home\tgj2u2\notes\Fall 2020\weekly_focus" + '\\')
  print(r'\\wsl$\Ubuntu\home\tgj2u2\notes\Fall 2020\weekly_focus\output.txt')
  open('/home/tgj2u2/notes/Fall 2020/weekly_focus/output.txt', 'w').write(external.get_assignment_tasks(week))

  
@main.command()
@click.argument('start_week')
@click.argument('end_week')
def time_table(start_week, end_week):
  external.get_table(start_week, end_week)


@main.command()
def time_table_auto():
  now = datetime.now().date()
  start_week = now - timedelta(days=now.weekday()+1) # start on Sunday
  end_week = start_week + timedelta(days=6) # end on Saturday
  external.get_table(start_week, end_week)


@main.command()
@click.argument('week')
def missing_tasks(week):
  """Pass in a week number (W01, W02, etc.)"""
  external.missing_tasks(week)


@main.command()
@click.argument('class_name')
@click.argument('week')
@click.argument('assignment_title')
@click.argument('a_type')
def create_assignment(class_name, week, assignment_title, a_type):
  external.create_assignment_with_type(assignment_title, class_name, week, a_type, None)

@main.command()
@click.argument('assignment_id')
def delete_assignment(assignment_id):
  external.delete_assignment(assignment_id)

@main.command()
@click.argument('assignment_id')
@click.argument('task_number')
def delete_task(assignment_id, task_number):
  external.delete_task(assignment_id, task_number)


@main.command()
@click.argument('class_name')
@click.argument('week')
@click.argument('deadline')
@click.argument('assignment_title')
@click.argument('a_type')
def create_assignment_due(class_name, week, assignment_title, a_type, deadline):
  external.create_assignment_with_type(assignment_title, class_name, week, a_type, deadline)


@main.command()
@click.argument('assignment_id')
@click.argument('task_number')
@click.argument('task_title')
def create_task(assignment_id, task_number, task_title):
  external.create_task(assignment_id, task_number, task_title)


@main.command()
@click.argument('file')
@click.option('--date_completed', '-d')
def mark_done_duration_file(file, date_completed):
  if date_completed is None:
    external.write_complete_to_mysql(file)
  else:
    external.write_complete_to_mysql(file, date_completed)

main()
