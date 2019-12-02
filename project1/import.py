import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("postgres://kjkmtwcexbgcrx:522c649866896ff5bddbbbb0c53f2dec216fb496e6590bdce81f42e5aba9f313@ec2-174-129-253-47.compute-1.amazonaws.com:5432/d98hjgkripkjc5")
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    books = csv.reader(f)
    for isbn, title, author, year in books:
        db.execute("INSERT INTO books(isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
                    {"isbn": isbn, "title": title, "author": author, "year": year})
        print(f"Added book  {title}.")
    db.commit()

if __name__ == "__main__":
    main()

