#!/usr/bin/env python

from DB import *

e = DB("qtab.db")

entries = e.getEntries()
tags = ['abc','ABC','mon']
added = entries.create(Entry("ABC","ABC","wiki","website","owner", None, 0, tags))
print added.uid

read = entries.read("ABC")
print read

updated = read

for row in updated:
    row.wiki = "wiki2"
    ##entries.update(row)
    print row.wiki
