from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    @classmethod
    def create(cls, name):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO authors (name) VALUES (?)", (name,))
        author_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return cls(author_id, name)

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM authors")
        rows = cursor.fetchall()
        conn.close()
        return [cls(row["id"], row["name"]) for row in rows]

    def articles(self):
        from models.article import Article  # Delayed import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM articles WHERE author_id = ?', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(row["id"], row["title"], row["content"], row["author_id"], row["magazine_id"]) for row in rows]

    def magazines(self):
        from models.magazine import Magazine  # Delayed import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT magazines.* FROM magazines
            JOIN articles ON magazines.id = articles.magazine_id
            WHERE articles.author_id = ?
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Magazine(row["id"], row["name"], row["category"]) for row in rows]

    def __repr__(self):
        return f"<Author {self.name}>"
