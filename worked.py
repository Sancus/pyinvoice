#!/usr/bin/env python

import argparse
import calendar
import collections
import datetime
import jsondate as json
import os
import sys

def main():
    pfile = 'project.json'
    parser = argparse.ArgumentParser(
    description="""
    worked start -s Feb 24 2017
    worked 8 -s Feb 24 2017 comment
    worked 8 comment (default today)
    worked summary (lists days and hours worked as well as total)
    """, formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('-s', '--start-date',
                        dest='start_date',
                        type=valid_date_type,
                        default=datetime.date.today(),
                        help='start datetime in format "YYYY-MM-DD"')
    parser.add_argument('first', nargs='?')
    parser.add_argument('other', nargs='*')

    args = parser.parse_args()
    # set the date that work happened
    work_date = args.start_date
    # set first args and the rest of 'em
    first = args.first
    other = args.other

    # assume we're adding work log
    work = True
    # assume we're not creating a new project file
    create = False

    if first =='summary':
        # Build a list of days and how many hours were worked
        project = check_project_file(pfile)
        days = {}
        for entry in project['work_log']:
            base = days.get(entry['date'], 0)
            days[entry['date']] = base + entry['hours']
        days = collections.OrderedDict(sorted(days.items()))
        for k, v in days.iteritems():
            print '{0} {1} - {2} hours.'.format(calendar.day_name[k.weekday()], k, v)
        print "You've worked {0} hours on project {1} since {2}.".format(project['total']/project['rate'], project['name'], project['start_date'])
        sys.exit()
    elif first == 'start':
        create = True
        work = False
    else:
        try:
            first = int(first)
        except (ValueError, TypeError):
            parser.print_help()
            sys.exit(1)

    project = check_project_file(pfile, create, work_date)

    if work:
        comment = ' '.join(other)
        log_entry = {'comment': comment,
                     'date': work_date,
                     'hours': first,
                     'subtotal': project['rate'] * first}
        project['work_log'].append(log_entry)
        project['total'] = total_cost(project['work_log'])
        project['totalhours'] = project['total']/project['rate']

    write_project_data(project, pfile)

def total_cost(work_logs):
    total = 0
    for log in work_logs:
        total = total + log['subtotal']
    return total

def write_project_data(project, pfile):
    with open(pfile, 'w') as f:
        res = json.dump(project, f, indent=4, sort_keys=True)
    return res

def check_project_file(pfile, create=False, date=False):
    if os.path.isfile(pfile):
        with open(pfile, 'r') as f:
            project = json.load(f)
    else:
        if create:
            project = { 'name': '',
                        'invoice': '001',
                        'rate': 0,
                        'start_date': date or datetime.date.today(),
                        'work_log': []}
        else:
            sys.exit('No {0} found, '.format(pfile))
    return project

def valid_date_type(arg_date_str):
    """custom argparse *date* type for user dates values given from the command line"""
    try:
        return datetime.datetime.strptime(arg_date_str, "%Y-%m-%d").date()
    except ValueError:
        msg = "Given Date ({0}) not valid! Expected format, YYYY-MM-DD!".format(arg_date_str)
    raise argparse.ArgumentTypeError(msg)

if __name__ == '__main__':
    main()