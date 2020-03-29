import sqlite3
import time

# connexion to the database

conn = sqlite3.connect('images_classification.db')
conn.execute('''CREATE TABLE IF NOT EXISTS document
         (id INTEGER  PRIMARY KEY   AUTOINCREMENT,
         filename           TEXT    NOT NULL,
         realfilname            TEXT     NOT NULL,
         filetype        TEXT NOT NULL,
         siren INTEGER NOT NULL,
         tva INTEGER NOT NULL,
         address INTEGER NOT NULL,
         companyname INTEGER NOT NULL,
         score REAl NOT NULL,
         date TEXT NOT NULL) ;''')


def insert_invoice_file(filename, realfilname, filetype, siren, tva, address, companyname, score):
    conn = sqlite3.connect('images_classification.db')
    # transform boolean to integer for sqlite (boolean not supported)
    siren = 0 if not siren else 1
    tva = 0 if not tva else 1
    address = 0 if not address else 1
    companyname = 0 if not companyname else 1
    # end
    date = str(time.time())  # timestamp
    filetype = str.upper(filetype)
    conn.execute("INSERT INTO document (id,filename,realfilname,filetype, siren, tva, address, companyname, score, date) \
            VALUES (NULL,%s, %s, %s, %d, %d, %d, %d, %d, %s)" % (filename, realfilname, filetype, siren, tva, address, companyname, score, date))
    conn.commit()


def get_files(filetype=None):
    conn = sqlite3.connect('images_classification.db')
    if filetype is None:
        cursor = conn.execute("SELECT filename,realfilname,filetype, siren, tva, address, companyname, score, date from document")
    else:
        filetype = str.upper(filetype)
        cursor = conn.execute("SELECT filename,realfilname,filetype, siren, tva, address, companyname, score, date from document WHERE filetype=%s" % (filetype))

    result = []

    for row in cursor:
        files = files.append({
            'filename': row['filename'],
            'url': row['realfilename'],
            'filetype': row['filetype'],
            'siren': True if row['siren'] == 1 else False,
            'tva': True if row['tva'] == 1 else False,
            'address': True if row['address'] == 1 else False,
            'companyname': True if row['companyname'] == 1 else False,
            'score': True if row['score'] == 1 else False,
            'date': row['date']

        })
    return result


def test():
    insert_invoice_file('erere', 'dede', 'invoice', False, True, False, False, 85.5)
