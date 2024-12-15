from database.connection import get_db_connection

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

    @classmethod
    def create(cls, title, content, author_id, magazine_id):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO articles (title, content, author_id, magazine_id)
            VALUES (?, ?, ?, ?)
        ''', (title, content, author_id, magazine_id))
        article_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return cls(article_id, title, content, author_id, magazine_id)

    @classmethod
    def get_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles")
        rows = cursor.fetchall()
        conn.close()
        return [cls(row["id"], row["title"], row["content"], row["author_id"], row["magazine_id"]) for row in rows]

    def __repr__(self):
        return f"<Article {self.title}>"
