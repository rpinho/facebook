#!/usr/bin/env python
#!/usr/bin/python

import sys, os
from json import load
from collections import Counter
from datetime import datetime
import facebook

oauth_access_token = os.environ['oauth_access_token']

fields = ['gender', 'hometown', 'location', 'first_name', 'last_name',
          'birthday', 'political']#, 'education', 'work']

N = [2,5,7,7,7,7,7]

utf = {u'\xe9':'e', u'\xed':'i', u'\xe3':'a', u'\xfa':'u', u'\xf3':'o',
       u'\xe3':'a', u'\xe7':'c', u'\xe1':'a', u'\xf5':'o', u'\xea':'e',
       u'\xea':'e', u'\xe2':'a', u'\u014d':'o', u'\u01dd':'a', u'\xfc':'u',
       u'\xf4':'o'}

locations = {u'Gaia, Porto, Portugal': u'Vila Nova de Gaia, Portugal'}

nested = ['hometown', 'location']

def translate_names(names, table):
    for key, value in table.iteritems():
        names = [name.replace(key, value) for name in names]
    return names

def get_friends(data):
    return data['friends']['data']

def get_friends_field(friends, field):
    return [friend[field] for friend in friends
            if field in friend.keys()]

def get_nested_field(friends, field):
    return [friend[field]['name'] for friend in friends
            if field in friend.keys()]

def parse_first_last_names(names):
    all_names = [name.split() for name in names]
    first_name = [name[0] for name in all_names]

    last_name = []
    for i in range(1,4):
        next_name = [name[i] for name in all_names if len(name) > i]
        last_name.extend(next_name)

    return first_name, last_name

def parse_birthday(birthday):
    try:
        birthday = datetime.strptime(birthday,"%m/%d/%Y")
    except:
        birthday = datetime.strptime(birthday,"%m/%d")
        return birthday.strftime('%b'), birthday.day
    else:
        return birthday.strftime('%b'), birthday.day, birthday.year

def parse_birthdays(birthdays):
    birthdays = [parse_birthday(birthday) for birthday in birthdays]
    month = [birthday[0] for birthday in birthdays]
    day = [birthday[1] for birthday in birthdays]
    year = [birthday[2] for birthday in birthdays if len(birthday) == 3]
    return month, day, year

def print_most_common(data, n):
    c = Counter(data)
    print c.most_common(n), sum(c.values())

def get_and_print_most_common(friends, field, n):
    print field

    # get data
    try:
        if field in nested:
            data = get_nested_field(friends, field)
        else:
            data = get_friends_field(friends, field)

    except:
        pass

    else:

        # correct utf characters
        if 'name' in field:
            data = translate_names(data, utf)

        # location synonyms
        if field == 'location' or field == 'hometown':
            data = translate_names(data, locations)

        # parse full names into first and last
        if field == 'name':
            names = parse_first_last_names(data)
            for x in names:
                print_most_common(x, n)

        elif field == 'birthday':
            birthdays = parse_birthdays(data)
            for x in birthdays:
                print_most_common(x, n)

        # get and print most common
        else:
            print_most_common(data, n)

######################
## facebook.GraphAPI #
######################

def get_graph():
    return facebook.GraphAPI(oauth_access_token)

def get_profile(graph=None):
    if not graph:
        graph = get_graph()
    return graph.get_object("me")

def get_friendsAPI(fields, graph=None):
    if not graph:
        graph = get_graph()
    return graph.get_connections("me", "friends", fields=fields)['data']


def main():

    try:
        fname = sys.argv[1]
    except IndexError:
        # connect to facebook API and download data in real-time
        friends = get_friendsAPI(fields)
    else:
        # load pre-downloaded json file
        fp = open(fname)
        data = load(fp)
        friends = get_friends(data)

    for field, n in zip(fields,N):
        get_and_print_most_common(friends, field, n)

if __name__ == '__main__':
    main()
