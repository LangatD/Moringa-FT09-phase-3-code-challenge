from database.connection import get_db_connection

class Magazine:
    def __init__(self, id=None, name=None, category="General"):
        self.id = id
        self.name = name
        self.category = category
        if not self.id:  # Create a new record only if `id` is not provided
            self._create_magazine()

    def _create_magazine(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (self.name, self.category))
        self.id = cursor.lastrowid  # Assign the generated ID
        conn.commit()
        conn.close()

    @classmethod
    def create(cls, name, category="General"):
        """
        Class method to create a new Magazine instance and save it to the database.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO magazines (name, category) VALUES (?, ?)", (name, category))
        magazine_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return cls(magazine_id, name, category)

    @classmethod
    def get_all(cls):
        """
        Retrieve all Magazine records from the database and return them as instances.
        """
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM magazines")
        rows = cursor.fetchall()
        conn.close()
        return [cls(row["id"], row["name"], row["category"]) for row in rows]

    def articles(self):
        """
        Retrieve all articles associated with this magazine.
        """
        from models.article import Article  # Delayed import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM articles WHERE magazine_id = ?", (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Article(row["id"], row["title"], row["content"], row["author_id"], row["magazine_id"]) for row in rows]

    def contributors(self):
        """
        Retrieve all authors who have written articles for this magazine.
        """
        from models.author import Author  # Delayed import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT authors.* FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row["id"], row["name"]) for row in rows]

    def article_titles(self):
        """
        Retrieve the titles of all articles for this magazine.
        """
        return [article.title for article in self.articles()]

    def contributing_authors(self):
        """
        Retrieve authors who have written more than 2 articles for this magazine.
        """
        from models.author import Author  # Delayed import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT authors.*, COUNT(*) as article_count FROM authors
            JOIN articles ON authors.id = articles.author_id
            WHERE articles.magazine_id = ?
            GROUP BY authors.id
            HAVING article_count > 2
        ''', (self.id,))
        rows = cursor.fetchall()
        conn.close()
        return [Author(row["id"], row["name"]) for row in rows]

    def __repr__(self):
        return f"<Magazine {self.name}, Category: {self.category}>"
