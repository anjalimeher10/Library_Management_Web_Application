from flask import Flask, request
import mysql.connector


app = Flask(__name__)

#connection to mysql
mysqlHost = "localhost"
mysqlDB = "amx"
username = "amx"
pw = "amx@1234"
connection = mysql.connector.connect(host=mysqlHost, database=mysqlDB, user=username, password=pw)
cursor = connection.cursor(dictionary=True)

# login
@app.route('/login', methods =['GET','POST'])
def login():
    session ={
        "email" : getParam("email"),
        "password" : getParam("password")
    }
    email = session['email']
    password = session['password']
        #connection = mysql.connector.connect(host=mysqlHost, database=mysqlDB, user=username, password=pw)
        #cursor = connection.cursor(buffered=True)
    cursor.execute('SELECT * From user WHERE email = %s AND password =%s', (email, password,))
    user = cursor.fetchone()
    connection.commit()
    if user != None:
        message = "Logged in successfully"
    else : 
        message = "Please enter correct email / password "
        print("please enter correct email or password")
    return message

#serach books from the Application 
@app.route('/serachBook', methods =['GET'])
def serachBook():
    session = {
        "BOOK_NAME" : getParam("book_name"),
        "BOOK_AUTHOR" : getParam("book_author")
    }
    book_name = session['BOOK_NAME']
    book_author = session["BOOK_AUTHOR"]
    print(book_name)
    book = cursor.execute('SELECT * From books WHERE book_name = %s AND book_author =%s', (book_name, book_author,) )
    book = cursor.fetchone()
    #bookJson = json.dumps(book)
    if book == None:
        return ("This book is not available")
    connection.commit()
    return book

#insert new books to the system
@app.route('/insertBook', methods =['POST','GET'])
def insertBook():
    session = {
        "BOOK_ID" : getParam("book_id"),
        "BOOK_NAME" : getParam("book_name"),
        "BOOK_AUTHOR" : getParam("book_author"),
        "BOOK_RENT" : getParam("book_rent")
    }
    cursor.execute ('INSERT INTO Books (book_id , book_name ,book_author , book_rent) VALUES ("'+session['BOOK_ID']+'","'+session['BOOK_NAME']+'" ,"'+session['BOOK_AUTHOR']+'" ,"'+session['BOOK_RENT']+'")')
    connection.commit()
    return "New Book Inserted successfully"

#given book to the member                
@app.route('/givenBook', methods =['POST','GET'])
def givenBook():
    session = {
        "BOOK_ID" : getParam("book_id"),
        "BOOK_NAME" : getParam("book_name"),
        "MEMBER_NAME" : getParam("member_name"),
        "BOOK_RENT" : getParam("book_rent")
    }
    cursor.execute ('INSERT INTO givenBook (book_id , book_name ,member_name , book_rent) VALUES ("'+session['BOOK_ID']+'","'+session['BOOK_NAME']+'" ,"'+session['MEMBER_NAME']+'" ,"'+session['BOOK_RENT']+'")')
    book_id = session['BOOK_ID']
    cursor.execute ("DELETE FROM books WHERE book_id = %s", (book_id,))
    connection.commit()
    return 'Given book successfully remove from the system and add to the givenbook table'

#return book from the member
@app.route('/returnBook', methods =['POST','GET'])
def returnBook():
    session = {
        "BOOK_ID" : getParam("book_id")
    }
    book_id = session["BOOK_ID"]
    cursor.execute("SELECT * FROM givenbook WHERE book_id = %s", (book_id,))
    givenBook = cursor.fetchone()
    print(str(givenBook['book_id']))
    cursor.execute('INSERT INTO books (book_id, book_name, book_author, book_rent) VALUES ("'+str(givenBook['book_id'])+'","'+str(givenBook['book_name'])+'" ,"'+str(givenBook['book_author'])+'" ,"'+str(givenBook['book_rent'])+'")')
    cursor.execute('DELETE FROM givenbook WHERE book_id = %s',(book_id,))
    connection.commit()
    return "Member return book inserted into system"



def getParam(param):
    if param in request.args:
        return str(request.args.get(param))
    elif param in request.form:
        return str(request.form[param])
    else:
        return ''             

if __name__=='__main__':
    app.run(debug=True)
