#!/usr/bin/python

import sys, json, urllib2

host = 'localhost:50111'
user = 'dev'
database = 'default'
schema = None

# Example reply: {"columns":[{"name":"a","type":"int"},{"name":"b","type":"int"},{"name":"c","type":"int"}],"database":"default","table":"input"}
def get_schema(table): return json.loads(urllib2.urlopen('http://'+host+'/templeton/v1/ddl/database/'+database+'/table/'+table+'?user.name='+user).read())

def check_type(val, type):
  if type in ['tinyint', 'smallint', 'int']:
    try: return int(val)
    except ValueError: return False
  elif type == 'bigint':
    try: return long(val)
    except ValueError: return False
  elif type in ['float', 'double', 'decimal']:
    try: return float(val)
    except ValueError: return False
  elif type == 'string': return True

for record in sys.stdin:
  table = record.strip().split('\t')[0]
  columns = record.strip().split('\t')[1:]
  if schema is None: schema = get_schema(table)

  valid = True
  for col_num, val in enumerate(columns):
    valid = check_type(val, schema['columns'][col_num]['type'])
    if not valid: break
  
  if valid: print '\t'.join(['1'] + columns)
  else: print '\t'.join(['-1'] + columns)
