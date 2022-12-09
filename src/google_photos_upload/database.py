import sqlite3

class Database:
    def __init__(self, path):
        self.database_location = "{}/gphotos.sqlite".format(path)
        self.db = sqlite3.connect(self.database_location)
        self.create_tables()

    def create_tables(self):
        self.db.execute('CREATE TABLE IF NOT EXISTS files (name text, path text, album text, external_id text, external_url text)')
        self.db.execute('CREATE TABLE IF NOT EXISTS albums (name text, path text, external_id text, external_url text)')

    def add_file(self, name, path, album, id, url):
        self.db.execute('INSERT INTO files (name, path, album, external_id, external_url) VALUES (?, ?, ?, ?, ?)', (name, path, album, id, url))
        self.db.commit()

    def add_album(self, name, path, id, url):
        self.db.execute('INSERT INTO albums (name, path, external_id, external_url) VALUES (?, ?, ?, ?)', (name, path, id, url))
        self.db.commit()

    def get_file(self, path):
        rows = self.db.execute('SELECT * FROM files WHERE path = ?', (path, )).fetchall()
        return rows if len(rows) > 0 else None

    def get_album(self, path):
        rows = self.db.execute('SELECT * FROM albums files WHERE path = ?', (path, )).fetchall()
        return rows if len(rows) > 0 else None
