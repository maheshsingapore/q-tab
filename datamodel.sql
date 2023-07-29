create table entry(uid integer primary key, acronym character, desc text, wiki text, website varchar, owner varchar, lastmodified datetime, tags text);
create table entry_pattern(uid integer primary key, sys_id varchar, sys_name, pattern varchar, owner varchar, redirect_url text, lastmodified datetime);
