#!/usr/bin/env python

from DB import *

e = DB("qtab.db")

patterns = e.getEntryPatterns()
#EntryPattern(uid, entry_uid, pattern, owner, redirect_url, lastmodified)

added = patterns.create(EntryPattern("SN", "ServiceNow", "INC[0-9]{10}","mahesh","http://127.0.0.1:5000/servicenow_inc.html?number={0}"))
print added.uid

read = patterns.read("CHG")
print read

updated = read

for row in updated:
    row.owner = "mahesh"
    ##patterns.update(row)
    print row.pattern + ":" + row.redirect_url
