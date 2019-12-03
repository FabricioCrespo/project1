# Project 1

This porject is about the creation of a web application to search books inside a database. You cand search a book by its isbn, title or author. Either users or books should be on the database server.

Flask is provided for this project. It let us load different pages to access to information.

My project1 has two python files. The first one has the application. Here are declared the different routes for the web application and the instruccions to access to the database too. The second one is the file import.py which let us import all the books to the databse.

There is a folder called templates. It has the different HTML files that I have used to render the app.routes.They are:
---author.html: display all the books matches with the authors of the data base. The same funcionality for title.html and isbn.html

---index.html let to users login or signup.

---error.html It is a template for display error with a particular message.

--success.html. Let users go to a page to login after theur signup.

--personal_account.html. It displays a welcome message to users and has a button to begin to search books.

--layout: it is the principal format to display the others html files. It has the import statement such as style.css, the bootstraps, etc.

--book.html It is used to display the information after the users search by isbn, title or author. Also, it let to users see and make reviews for a particular books.

Finally, there is the folder called static. It has the stylesheet.css and images that I has used for the design of the web application.

Thank you for readme. I hope that you enjoy the web application.
