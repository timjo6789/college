#!/usr/bin/python3
import sys
arguments = sys.argv[1:]
file_name = arguments[0]
output_file = arguments[1]
Title = ''
Subtitle = ''
content = ''
tab = 0
SPACE = '  '

def count_space_left(line):
    total = 0
    for i in line:
        if i.isspace():
            total += 1
        else:
            break
    return total


def set_tab(word):
    global SPACE
    total = count_space_left(word)
    tab = total // len(SPACE)
    return tab

def format_keyword(each):
    # handle image keyword
    if each.startswith('Image: '):
        each = each.split('Image: ')[1]
        each = f'<img src="{each}">'
    elif each.startswith('Image figure: '):
        each = each.split('Image figure: ')[1]
        each = f'<img src="figures/figure_{each}.png">'

    # handle video keyword
    if each.startswith('Video: '):
        each = each.split('Video: ')[1]
        each = f'<video controls><source src="{each}.mp4" type="video/mp4">Your browser does not support the video tag.</video>'
    elif each.startswith('Video figure: '):
        each = each.split('Video figure: ')[1]
        each = f'<video controls><source src="figures/{each}.mp4" type="video/mp4">Your browser does not support the video tag.</video>'
    elif each.startswith('Video resource: '):
        each = each.split('Video resource: ')[1]
        each = f'<video controls><source src="resources/{each}.mp4" type="video/mp4">Your browser does not support the video tag.</video>'
    # replace &nbps with span class="tab"
    if '&nbsp;' in each:
       each = each.replace('&nbsp;', '<span class="tab"></span>')
    elif '&nbsp' in each:
        # breakpoint()
        each = each.replace('&nbsp', '<span class="tab"></span>')
    return each


# look ahead
stop = False
first_time = True
with open(f'{file_name}.txt') as file:
    details = file.readlines()
    content = {'Reduce':'', 'Record':''}
    key = 'Reduce'
    last_item = ''
    for each, each_next in zip(details, details[1:]):
        # if 'Can be mobile devices (laptops, tablets, smartphones, etc.)' in each:
        #     stop = True
        tab = set_tab(each)
        future_tab = set_tab(each_next)
        spacing = tab * SPACE
        future_spacing = future_tab * SPACE

        if tab == 0 and 'Title: ' in each:
            each = each.strip()
            each = each.replace('Title: ', '')
            Title = each
        elif tab == 0 and 'Subtitle: ' in each:
            each = each.strip()
            each = each.replace('Subtitle: ', '')
            Subtitle = each
        elif tab == 0 and 'Description: ' in each:
            each = each.strip()
            each = each.replace('Description: ', '')
            content[key] += f'\n<h2>{each}</h2>\n<ul>'
        elif tab == 0 and 'Reduce' == each.strip():
            key = 'Reduce'
        elif tab == 0 and 'Record' == each.strip():
            key = 'Record'
        else:
            if each.strip() != '':
                each = each.strip()
                each = format_keyword(each)
                if tab != future_tab:
                    if future_tab > tab:
                        # indented (open indent, has 1+ children)
                        content[key] += f'{spacing}<li>\n{future_spacing}<div class="head">{each}</div>\n{future_spacing}<ul class="content">\n'
                    elif future_tab < tab:
                        content[key] += f'{spacing}<li>{each}</li>\n'
                        # dedented 1+ (close indent)
                        shorter_spacing = ''
                        for shorter_tab in range(tab-1, future_tab-1, -1):
                            shorter_spacing = shorter_tab * SPACE
                            shorter_spacing = ""
                            content[key] += f'{shorter_spacing}</ul></li>\n'
                else:
                    # next line indent is same as this line indent (no children)
                    content[key] += f'{spacing}<li>{each}</li>\n'

    if each_next.strip() != '':
        each_next = format_keyword(each_next.strip())
        content[key] += f'{future_spacing}<li>{each_next}</li>\n'

output = fr"""<link href='cornell_note_html\style.css' rel='stylesheet'>
<script src="cornell_note_html\jquery.js"></script>
<script src="cornell_note_html\script.js"></script>
<h1>{Title}</h1>
<h2>{Subtitle}</h2>
<div id='reduce'>
    <h1>Reduce</h1>
    {content['Reduce']}
</div>

<div id='record'>
    <h1>Record</h1>
    {content['Record']}
</div>

<div id='summary'>
    <h1>Summary</h1>
</div>

<div id='recite'>
    <h1>Recite</h1>
</div>

<div id='reflect'>
    <h1>Reflect</h1>
</div>

<div id='review'>
    <h1>Review</h1>
</div>"""
with open(f'{output_file}.html', 'w') as file:
    file.write(output)
