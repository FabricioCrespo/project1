
--CREANDO TABLA PARA LOS USUARIOS

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL, --NO SE PUEDE REPETIR LOS USUARIOS
    password VARCHAR NOT NULL,
    name VARCHAR NOT NULL,
    last_name VARCHAR NOT NULL,
    count_state boolean DEFAULT FALSE, --PARA VER SI LA CUENTA ESTA ACTIVA O NO, CUANDO CREA ESTA CERRADA
    UNIQUE(username)
);

INSERT INTO users (username, password, name, last_name) VALUES ('FabricioCrespo', '1234', 'Fabricio', 'Crespo');
select * from users where (username='FabricioCrespo') and (password='1234');

--Each one has an ISBN number, a title, an author, and a publication year
--crear tabla para mis libros de books.csv

CREATE TABLE books (
    isbn VARCHAR NOT NULL, --Todos los libros tienen ISBN
    title VARCHAR NOT NULL,
    author VARCHAR NOT NULL,
    year VARCHAR NOT NULL,
    UNIQUE(isbn),
    PRIMARY KEY(isbn)
);


--Reviews table

CREATE TABLE reviews (
    id SERIAL PRIMARY KEY, --Each review has a id
    isbn_review varchar NOT NULL, --review with its ISBN book
    review varchar NOT NULL, --reviews
    username_review varchar NOT NULL, --nombre del usuario quien hace el review
    FOREIGN KEY (isbn_review) REFERENCES books(isbn), --idbn_review debe constar en el isbn de la tabla libros
    FOREIGN KEY (username_review) REFERENCES users(username) --usuario debe existir en la tabla usuarios
);

select avg(review::integer) from reviews where isbn_review= :isbn_book;

1
2
ALTER TABLE reviews ADD COLUMN review_opinion varchar;

SELECT round(avg(review::integer),1) as average, count(*) as count from reviews;

DELETE FROM reviews WHERE username_review= 'FabricioCrespo' or username_review= 'BelenArias' or username_review= 'BrianCrespo';