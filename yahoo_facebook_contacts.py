#!/usr/bin/env python
#!/usr/bin/python

import sys, json

def get_name_email(contact):
    fields = contact['fields']

    try:
        given_name  = fields[1]['value']['givenName']
        family_name = fields[1]['value']['familyName']
    except:
        given_name  = fields[2]['value']['givenName']
        family_name = fields[2]['value']['familyName']

    name = ' '.join((given_name, family_name))

    email = fields[0]['value']

    return ','.join((name, email))

def main():

    # load json file
    fname = sys.argv[1]
    fp = open(fname)
    file = json.load(fp)

    # get name, email
    names_emails = [get_name_email(contact).encode('utf-8')
                    for contact in file['contacts']['contact']]

    # save if numpy
    try:
        import numpy
        numpy.savetxt(fname.split('.')[0] + '.csv', names_emails, '%s')

    # print to output
    except:
        for name_email in names_emails:
            print name_email

if __name__ == '__main__':
    main()
