#!/usr/bin/env python3
# cli - command line interface to ntz json file.

"""
### Showing notes.
Typing `ntz` will display your notes.
So will `ntz -l Shopping`

### Saving notes
Use [-r] for remember. Using [-r] on its own will save to the default ToDo category, like so:

`$ ntz -r "my first note"`

Using `-r` is the same as `ntz -c ToDo "my first note"

Use the -c flag to create a new category or direct a note to an existing category, like this:

`$ ntz -c Shopping "while out, get eggs"`

### Removing notes
Use [-f] for forget. [-f] requires a category and note number.

To delete the note we made in the Shopping category (and also the category, because it will be empty) we can do:

`$ ntz -f Shopping 1`

### Editing notes
Use [-e] for edit. This is more of a replacement then an edit.

To replace our first note, we can do

`$ ntz -e General 1 'my first note, edited'`

### Clearing all notes

`$ ntz clear`

You will be prompted with a Y/N and given a chance to review your notes before they are deleted.
"""

import json
from sys import argv 

class Ntz:
  def __init__(self):
    self.fn = 'db.json'
    self.swb = {
          '-l': self.do_list,
          '-r': self.do_store,
          '-c': self.do_store,
          '-f': self.do_erase,
          '-e': self.do_replace,
      }

  def opendb(self):
      try:
        with open(self.fn) as file:
          content = file.read()
          #print("before db", content)
          data = json.loads(content)
          if data == None:
            data = {}
          #print(data)
          return data
      except FileNotFoundError:
          file = open(fn, 'w')
      return {}

  def save(self, db):
      with open(self.fn, 'w') as file:
          documents = json.dumps(db)
          #print("documents", documents)
          file.write(documents)
          file.close()

  def scan_args(self):
      # print("debug:", argv)
      # "ntz"
      if len(argv) == 1:
          return '-l', 'all', '0', ''
      # ntz -r "note"
      if len(argv) == 3:
          return argv[1], "ToDo", '0', argv[2]
      # 'ntz' '-c' 'cat' 'note/num'
      if len(argv) == 4:
          return argv[1], argv[2], '0', argv[3]
      # 'ntz' '-e' 'cat' 'num' 'new note'
      if len(argv) == 5:
          return argv[1], argv[2], argv[3], argv[4]



  def perform_cmd(self, db, cmd, cat, n, note):
      do_work = self.swb.get(cmd)

      if do_work is None:
          return -1, "invalid command"

      return do_work(db, cat, n, note)

  # funcs that do commands
  def do_list(self, db, cat, n, note):
      # `ntz -l Shopping`
      if cat != 'all':
          self.print_cat(db, cat)
      else:
          cats = db.keys() # get(cat)
          if cats != None:
              for cat in cats:
                  self.print_cat(db, cat)
      return 0, ''

  def print_cat(self, db, cat):
      notes = db.get(cat)
      #print("debug: db", db)
      #print("debug: notes", notes)
      if notes is not None:
          i = 0
          print(cat, ":")
          for n in notes:
              print('\t', i, '-', n)
              i = i + 1

  def do_store(self, db, cat, n, note):
      #print('store:', cat, n, note)
      # ntz -c Shopping "while out, get eggs"
      if db.get(cat) is None:
          db[cat] = []
      db[cat].append(note)
      #print('db', db)
      return 0, ''

  def do_erase(self, db, cat, n, note):
      # -f Shopping 1
      return 0, ''

  def do_replace(self, db, cat, n, note):
      # -e General 1 'my first note, edited'
      return 0, ''

  ## main command line interface (cli)
  def cli(self):
      db = self.opendb()

      cmd, cat, n, note = self.scan_args()
      print(">>", cmd, cat, n, note)
      result, reason = self.perform_cmd(db, cmd, cat, n, note)
      self.save(db)
      if result != 0: # some error
          print(result, reason)

if __name__ == "__main__":
  obj = Ntz()
  obj.cli()
