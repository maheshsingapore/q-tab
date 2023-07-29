#!/usr/bin/env python

from flask import Flask, request, jsonify, render_template,send_from_directory,redirect
from DB import *
import re

app = Flask("qtab.py")
db = DB("qtab.db")
entries = db.getEntries()
entry_patterns = db.getEntryPatterns()
all_patterns = entry_patterns.readAll()

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/')
def index_page():
    return render_template("index.html")


@app.route('/pattern/update_form/update=<term>')
def pattern_update_form(term):
    to_update = entry_patterns.readWithId(term)
    return render_template("pattern_update.html", pe=to_update, term=term)

@app.route('/pattern/update', methods=['POST'])
def pattern_update():
    uid = request.form["uid"]
    sys_id = request.form["sys_id"]
    sys_name = request.form["sys_name"]
    pattern = request.form["pattern"]
    owner = request.form["owner"]
    redirect_url = request.form["redirect_url"]

    entry_patterns.update(EntryPattern(sys_id, sys_name, pattern, owner, redirect_url, None, uid))
    all_patterns = entry_patterns.readAll()

    return redirect('/pattern/create_form')

@app.route('/pattern/create_form')
def pattern_create_form():
    return render_template("pattern_create.html")

@app.route('/pattern/create', methods=['POST'])
def pattern_create():
    sys_id = request.form["sys_id"]
    sys_name = request.form["sys_name"]
    pattern = request.form["pattern"]
    owner = request.form["owner"]
    redirect_url = request.form["redirect_url"]

    created = entry_patterns.create(EntryPattern(sys_id, sys_name, pattern, owner, redirect_url))
    all_patterns.append(created)

    return redirect('/pattern/create_form')

@app.route('/pattern/search=<term>')
def pattern_search(term):
    if term == "all":
        all_patterns = entry_patterns.readAll()   
        return jsonify(data=[e.as_dict() for e in all_patterns])
    else:
        all_matched = []
        owner = request.args.get('owner')

        if owner is None:
            owner = "zsystem"
            print "No owner supplied, showing only default entries"

        owner_patterns = entry_patterns.readAll(owner)
        for p in owner_patterns:
            if p.matches(term):
                all_matched.append(p)

        number_of_results = len(all_matched)
        print "{0} pattern(s) matched for {1}".format(number_of_results, term)

        if (number_of_results == 1):
            return redirect(all_matched[0].get_redirect_url(term))
        else:
            return render_template('pattern_list.html', pattern_entries = all_matched, term = term)


@app.route('/pattern/validate/pattern=<term>')
def pattern_validate(term):
    message = jsonify(msg="Pattern parsed successfully", response_code=1)
    try:
        re.compile(term)
    except re.error:
        message = jsonify(msg="Bad pattern", response_code=0)

    return message

if __name__ == "__main__":
    app.run()
