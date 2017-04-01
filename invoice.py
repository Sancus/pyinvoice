import jinja2
import os
from jinja2 import Template
import settings
import worked
import datetime

def multiline(linelist):
    x = linelist[0]
    for l in linelist[1:]:
        x = '{0} \\\\ {1}'.format(x, l)
    return x


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
project['rate'] = format(float(project['rate']), '.2f')
project['total'] = format(float(project['total']), '.2f')
for l in project['work_log']:
    l['subtotal'] = format(float(l['subtotal']), '.2f')
project['client_address'] = multiline(settings.client_address)
project['home_address'] = multiline(settings.home_address)
project['position'] = settings.position
project['bank'] = settings.bank
project['routing'] = settings.routing
project['account'] = settings.account
project['invoice_date'] = datetime.date.today()
project['payment_date'] = project['invoice_date'] + datetime.timedelta(days=30)

template = latex_jinja_env.get_template('jinja-invoice.tex')
print(template.render(**project))
