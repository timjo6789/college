var is_task_table_toggle_all = false;


function toggleAll(){
  is_task_table_toggle_all = is_task_table_toggle_all ? false : true;
  document.querySelectorAll('div.task_table').forEach(element => {
      is_task_table_toggle_all ? element.classList.add('hidden') : element.classList.remove('hidden');
  });
}


function collapseAll(){
    $('div.task_table').addClass('hidden');
}


function expandAll(){
    $('div.task_table').removeClass('hidden');
}

function today() {
  var dt = new Date();
  return dt.getFullYear() + "-" + ( (dt.getMonth() + 1) + '').padStart(2, '0') + "-" + (dt.getDate() + '').padStart(2, '0');
}



function print_commands(date){
  date = date === undefined ? ` -d ${today()}` : ` -d ${date}`;
  output = '';
  $('span.task_table_item.time').each((index, element) => {
    let time = $(element).text();
    if (time != '0s') {
      parts = $(element).attr('id').split('-');
      assignment_id = parts[1];
      task_number = parts[2];
      output += `em mark-done-duration ${assignment_id} ${task_number} ${time}${date}\n`;
    }
  });
  for (const item of stopwatches) {
    if (item.duration == '0s' && item.is_done) {
      parts = item.element_id.split('-');
      assignment_id = parts[1];
      task_number = parts[2];
      output += `em mark-done ${assignment_id} ${task_number}${date}\n`;
    }
  }
  // console.log(output);
  copyToClipboard(output);
  console.log('check your clipboard');
}


function to_seconds(string){
  regex = /(?:(\d+)h)?(?:(\d+)?m)?(\d+)s.*/gm;
  element = [...string.matchAll(regex)][0];
  hour = element[1] === undefined ? 0 : parseInt(element[1]);
  minute = element[2] === undefined ? 0 : parseInt(element[2]);;
  second = parseInt(element[3]);
  total = hour * 3600 + minute * 60 + second 
  return total;
}


function pretty_time(seconds){
  minute = Math.floor(seconds / 60);
  seconds = seconds % 60;
  hour = Math.floor(minute / 60);
  minute = minute % 60;

  minute = hour > 0 || minute > 0 ? `${minute}m` : '';
  hour = hour > 0 ? `${hour}h` : '';
  return `${hour}${minute}${seconds}s`;
}

function total_time(){
  total_seconds = 0;
  for (const time of stopwatches) {
    total_seconds += time.get_time();   
  }
  console.log(pretty_time(total_seconds));
}

function time_left(duration){
  if (typeof duration == 'undefined'){
    duration = '8h0m0s';
  }
  if (typeof duration == 'string') {
    duration = to_seconds(duration);
  }
  total_seconds = 0;
  for (const time of stopwatches) {
    total_seconds += time.get_time();   
  }
  console.log(pretty_time(duration) + ": "+ pretty_time(duration - total_seconds));
}

// https://stackoverflow.com/questions/43733099/javascript-difference-between-two-time-strings/43733867
// with some modification
function get_duration(d1, d2) {
  d3 = new Date(Date.parse(d2)).getTime() - new Date(Date.parse(d1)).getTime();

  seconds = Math.round(d3 / 1_000, 0);

  return pretty_time(seconds);
}

var total_intervals = 0;

class Stopwatch {
  constructor(element, duration) {
    this.element = element;
    this.interval = -1;
    this.duration = duration === undefined ? '0s' : duration;
    this.element_id = $(element).attr('id').split('stopwatch')[1];
    this.is_started = false;
    this.is_done = false;

    this.start_time = '';
    this.end_time = '';

    this.toggle_button = `button#toggle${this.element_id}`;
    this.restart_button = `button#restart${this.element_id}`;
    this.complete_button = `button#complete${this.element_id}`;

    $(this.toggle_button).click(() => this.toggle());
    $(this.restart_button).click(() => this.restart());
    $(this.complete_button).click(() => this.complete());
  }

  toggle(){
    if (!this.is_started){
      this.is_started = true;
      this.start();
      $(this.toggle_button).text("stop");
    } else {
      this.is_started = false;
      this.stop();
      $(this.toggle_button).text("start");
    }
  }

  debug(details) {
    let parts = this.element_id.substring(1).split('-');
    let assignment_id = parts[0];
    let assignment_task = parts[1];
    details += 'assignment id ' + assignment_id + ' and task number ' + assignment_task + '\n';
    details += new Date();
    console.log(details);
  }

  start(){
    if (this.interval >= 0){
      this.stop();
    }
    if (current_runner !== this){
      if (current_runner.is_started){
        current_runner.toggle();
      }
      current_runner = this
    }
    this.debug('start_time\n');
    this.start_time = new Date();
    this.interval = setInterval(() => this.update(), 1000);
    total_intervals++;
  }

  stop(){
    clearInterval(this.interval);
    if (this.end_time === ''){
      this.end_time = new Date();
    }
    this.debug('end_time\n')
    this.duration = pretty_time(to_seconds(this.duration) + to_seconds(get_duration(this.start_time, this.end_time)));
    $(this.element).text(this.duration);
    this.start_time = '';
    this.end_time = '';
    this.interval = -1;
    total_intervals--;
  }

  get_time(){
    return to_seconds(this.duration);
  }

  restart() {
    if (confirm('Are you sure?')) {
      if (this.interval >= 0){
        this.stop();
      }
      this.duration = '0s';
      this.start_time = '';
      $(this.element).text(this.duration);
      $(this.toggle_button).text("start");
    }
  }

  update(){
    this.end_time = new Date();
    $(this.element).text(pretty_time(to_seconds(this.duration) + to_seconds(get_duration(this.start_time, this.end_time))));
  }

  setBackgroundColor(background_color) {
    $(`#task${this.element_id}`).css('background-color', background_color);
    $(`#task-number${this.element_id}`).css('background-color', background_color);
    $(`#stopwatch${this.element_id}`).css('background-color', background_color);
    $(`#toggle${this.element_id}`).parent().css('background-color', background_color);
    $(`#restart${this.element_id}`).parent().css('background-color', background_color);
    $(`#complete${this.element_id}`).parent().css('background-color', background_color);
  }

  complete() {
    // uses xnor to toggle between true and false
    this.is_done = (this.is_done ^ true) ? true : false;
    if (this.is_done) {
      $(this.complete_button).text('completed');
      this.setBackgroundColor('lightgreen');
    } else {
      $(this.complete_button).text('complete');
      this.setBackgroundColor('');
    }
    /*
    let output = '';
    let time = $(this.element).text();

    let parts = $(this.element).attr('id').split('-');
    let assignment_id = parts[1];
    let task_number = parts[2];

    output = `em mark-done-duration ${assignment_id} ${task_number} ${time}\n`;
    
    $.ajax({
      type: "POST",
      data: {
        time: time,
        assignment_id: assignment_id,
        task_number: task_number,
        date: new Date().toISOString().slice(0, 10)
      },
      url: "http://127.0.0.1:5000/mark_done_duration",
      //dataType: 'json',
      success: function(data) {
          console.log("This is the returned data: " + data);
      },
      error: function(error){
          console.log("Here is the error res: " + error);
      }
    });
    */
  }
}

stopwatches = [];
var current_runner = undefined;

$(document).ready(() => {
  $('div.assignment_table').click((element) => $(element.target.parentElement).find('div.task_table').toggleClass('hidden'));
  let first_time = true;
  $('span.task_table_item.time').each((index, element) => {
    stopwatch = new Stopwatch($(element), $(element).text());
    if (first_time){
      current_runner = stopwatch;
      first_time = false;
    }
    stopwatches.push(stopwatch);
  });
  $('div.task_table').addClass('hidden');
});

window.addEventListener('beforeunload', function (e) {
  is_counting = total_intervals > 0;

  warn = false;
  $('span.task_table_item.time').each((index, element) => {
    let time = $(element).text();
    if (time != '0s') {
      warn = true;
    }
  });

  if (!warn){
    for (const each of stopwatches) {
      if (each.is_done) {
        warn = true;
        break;
      }
    }
  }

  if (is_counting || warn){
    e.preventDefault();
    e.returnValue = '';
  }
});

// https://stackoverflow.com/questions/33855641/copy-output-of-a-javascript-variable-to-the-clipboard
function copyToClipboard(text) {
  var dummy = document.createElement("textarea");
  // to avoid breaking orgain page when copying more words
  // cant copy when adding below this code
  // dummy.style.display = 'none'
  document.body.appendChild(dummy);
  //Be careful if you use texarea. setAttribute('value', value), which works with "input" does not work with "textarea". – Eduard
  dummy.value = text;
  dummy.select();
  document.execCommand("copy");
  document.body.removeChild(dummy);
}