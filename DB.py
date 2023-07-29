#!/usr/bin/env python
import sqlite3 as lite
from singleton import Singleton
import logging
import re

log = logging.getLogger(__name__)

class DB(Singleton):

    def __init__(self, dbname):
        self.dbname = dbname
        log.info("Accessing DB : " + self.dbname)
        self.conn = lite.connect(dbname)
        self.entries = Entries(self.conn)
        self.entryPatterns = EntryPatterns(self.conn)

    def getEntries(self):
        return self.entries

    def getEntryPatterns(self):
        return self.entryPatterns

class Entry:

    def __init__(self, acronym, desc, wiki, website, owner, lastmodified=None, uid=0, tags=None):
        self.acronym = acronym
        self.desc = desc
        self.wiki = wiki
        self.website = website
        self.owner = owner
        self.lastmodified = lastmodified
        self.uid = None
        if tags is not None:
            self.tags = tags
        else:
            self.tags = []
            self.tags.append(self.acronym)

    def as_dict(self):
        return {"uid": self.uid, "acronym" : self.acronym, "desc" : self.desc, "wiki" : self.wiki, "website" : self.website, "owner" : self.owner, "lastmodified" : self.lastmodified}

class Entries:

    def __init__(self, conn):
        self.conn = conn

    def create(self, entry):
        args = (entry.acronym, entry.desc, entry.wiki, entry.website, entry.owner, " ".join(entry.tags));
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO entry VALUES (null, ?, ?, ?, ?, ?, datetime('now'), ?)", args)
            entry.uid = cur.lastrowid
            self.conn.commit()
            return entry

    def read(self, search_term):
        args = (('%' + search_term + '%'),)
        entries = []

        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT uid, acronym, desc, wiki, website, owner, lastmodified FROM entry where tags like ? ", args)
            all = cur.fetchall()
            for row in all:
                entries.append(self.mapEntry(row))

            return entries

    def update(self, entry):
        args = (entry.acronym, entry.desc, entry.wiki, entry.website, entry.owner, entry.uid);
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("UPDATE entry SET acronym = ?, desc = ?, wiki = ?, website = ?, owner = ?, lastmodified = datetime('now') where uid = ?", args)
            self.conn.commit()

    def delete(self, entry):
        pass


    def mapEntry(self, row):
        if row is not None:
            uid = row[0]
            acronym = row[1]
            desc = row[2]
            wiki = row[3]
            website = row[4]
            owner = row[5]
            lastmodified = row[6]

            return Entry(acronym, desc, wiki, website, owner, lastmodified, uid)


class EntryPattern:

    def __init__(self, sys_id, sys_name, pattern, owner, redirect_url, lastmodified=None, uid=None):
        self.sys_id = sys_id
        self.sys_name = sys_name
        self.pattern = pattern
        self.owner = owner
        self.redirect_url = redirect_url
        self.lastmodified = lastmodified
        self.uid = 0 if uid is None else uid

        self.regex = re.compile(pattern)

    def matches(self, input):
        return self.regex.match(input)

    def get_redirect_url(self, input):
        return self.redirect_url.format(input)

    def as_dict(self):
        return {"sys_id" : self.sys_id, "sys_name" : self.sys_name, "owner" : self.owner, "pattern" : self.pattern, "redirect_url" : self.redirect_url, "lastmodified" : self.lastmodified, "uid": self.uid}

class EntryPatterns:

    def __init__(self, conn):
        self.conn = conn

    def create(self, pattern):
        args = (pattern.sys_id, pattern.sys_name, pattern.pattern, pattern.owner, pattern.redirect_url)
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("INSERT INTO entry_pattern VALUES (null, ?, ?, ?, ?, ?, datetime('now'))", args)
            pattern.uid = cur.lastrowid
            self.conn.commit()
            return pattern

    def readAll(self, owner='zsystem'):
        args = ((owner),)
        entries = []

        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT uid, sys_id, sys_name, pattern, owner, redirect_url, lastmodified FROM entry_pattern where owner in (?, 'zsystem') order by owner asc", args)
            all = cur.fetchall()
            for row in all:
                entries.append(self.mapEntryPattern(row))

            return entries

    def read(self, search_pattern):
        args = (('%' + search_pattern + '%'),)
        entries = []

        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT uid, sys_id, sys_name, pattern, owner, redirect_url, lastmodified FROM entry_pattern where pattern like ? ", args)
            all = cur.fetchall()
            for row in all:
                entries.append(self.mapEntryPattern(row))

            return entries

    def readWithId(self, uid):
        args = ((uid),)
        entries = []

        with self.conn:
            cur = self.conn.cursor()
            cur.execute("SELECT uid, sys_id, sys_name, pattern, owner, redirect_url, lastmodified FROM entry_pattern where uid = ? ", args)
            one = cur.fetchone()

            return self.mapEntryPattern(one)

    def update(self, pattern):
        args = (pattern.sys_id, pattern.sys_name, pattern.pattern, pattern.owner, pattern.redirect_url, pattern.uid)

        print args
        with self.conn:
            cur = self.conn.cursor()
            cur.execute("UPDATE entry_pattern SET sys_id = ?, sys_name = ?, pattern = ?, owner = ?, redirect_url = ?, lastmodified = datetime('now') where uid = ?", args)
            self.conn.commit()

    def delete(self, pattern):
        pass

    def mapEntryPattern(self, row):
        if row is not None:
            uid = row[0]
            sys_id = row[1]
            sys_name = row[2]
            pattern = row[3]
            owner = row[4]
            redirect_url = row[5]
            lastmodified = row[6]

            return EntryPattern(sys_id, sys_name, pattern, owner, redirect_url, lastmodified, uid)
