import os
from dotenv import load_dotenv
import sqlalchemy as sa

load_dotenv()

class Database:
    def __init__(self):
        dbUrl = os.getenv("DB_CONNECTION_STRING")

        if not dbUrl:
            raise ValueError("DB_CONNECTION_STRING is not set in the environment variables.")

        self._engine = sa.create_engine(dbUrl, echo=True, future=True)

    def connect(self):
        return self._engine.connect()

    def close(self, connection):
        connection.close()

    def executeQuery(self, query: str):
        query = sa.text(query)
        with self.connect() as connection:
            try:
                result = connection.execute(query)
                connection.commit()
            except Exception as e:
                print(f"An error occurred: {e}")
                return None
            try:
                return result.fetchall()
            except Exception as e:
                return None


if __name__ == "__main__":
    #connection to db and creating simples table and deleting it
    #just for testing
    db = Database()
    with db.connect() as connection:
        db.executeQuery("CREATE TABLE IF NOT EXISTS test (id SERIAL PRIMARY KEY, name VARCHAR(50))")
        db.executeQuery("INSERT INTO test (name) VALUES ('Alice')")
        db.executeQuery("INSERT INTO test (name) VALUES ('Bob')")
        db.executeQuery("INSERT INTO test (name) VALUES ('Charlie')")
        result = db.executeQuery("SELECT * FROM test")
        for row in result:
            print(row)
        db.executeQuery("DROP TABLE test")
        db.close(connection)