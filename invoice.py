import jinja2
import os
from jinja2 import Template
import re
import settings
import worked
import datetime

def multiline(linelist):
    x = linelist[0]
    for l in linelist[1:]:
        x = '{0} \\\\ {1}'.format(x, l)
    return x


def tex_escape(text):
    """
        :param text: a plain text message
        :return: the message escaped to appear correctly in LaTeX
    """
    conv = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless ',
        '>': r'\textgreater ',
    }
    regex = re.compile('|'.join(re.escape(key) for key in sorted(conv.keys(), key = lambda item: - len(item))))
    return regex.sub(lambda match: conv[match.group()], text)


latex_jinja_env = jinja2.Environment(
    block_start_string = '\BLOCK{',
    block_end_string = '}',
    variable_start_string = '\VAR{',
    variable_end_string = '}',
    comment_start_string = '\#{',
    comment_end_string = '}',
    line_statement_prefix = '%%',
    line_comment_prefix = '%#',
    trim_blocks = True,
    autoescape = False,
    loader = jinja2.FileSystemLoader(os.path.abspath('.'))
)
project = worked.check_project_file('project.json')

project['work_log'] = sorted(project['work_log'], key=lambda k: k['date'])

# Fix bug with unescaped special characters in latex output.
for i, v in enumerate(project['work_log']):
    project['work_log'][i]['comment'] = tex_escape(project['work_log'][i]['comment'])

gst = project['total'] * 0.05
project['gst'] = format(float(gst), '.2f')
project['finaltotal'] = format(float(gst + project['total']), '.2f')
project['rate'] = format(float(project['rate']), '.2f')
project['total'] = format(float(project['total']), '.2f')
for l in project['work_log']:
    l['subtotal'] = format(float(l['subtotal']), '.2f')
    project['end_date'] = l['date']
project['client_address'] = multiline(settings.client_address)
project['home_address'] = multiline(settings.home_address)
project['position'] = settings.position
project['bank'] = settings.bank
project['transit'] = settings.transit
project['institution'] = settings.institution
project['account'] = settings.account
project['invoice_date'] = datetime.date.today()
# project['invoice_date'] = datetime.date(2020, 12, 31)
project['payment_date'] = project['invoice_date'] + datetime.timedelta(days=30)


template = latex_jinja_env.get_template('jinja-invoice.tex')
print(template.render(**project))
