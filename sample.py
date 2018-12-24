from flask import Flask, render_template,request,url_for,redirect, abort
import sqlite3

app = Flask(__name__)

table_name = ""
operation = ""

@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return render_template('homepage.html')
    return render_template('login.html', error=error)

@app.route('/get_op_table',methods=['GET','POST'])
def table():
        if request.method == 'POST':
                global table_name
                global operation
                table_name = request.form["table"]
                operation = request.form["operation"]
                if table_name == "students" and operation == "insert":
                        return render_template("insert_student.html")
                elif operation == "read":
                        return read()
                elif operation == "update":
                        return render_template("update.html")
                elif operation == "search":
                        return render_template("search.html")
                elif operation == "delete":
                        return render_template("delete.html")
        else:
                return abort(405)

@app.route('/insert',methods = ['GET','POST'])
def insert():
	if request.method == 'POST':
            global table_name
            global operation
            if table_name == "students" and operation == "insert":
                    studid = request.form["studentid"]
                    studname = request.form["studentname"]
                    depid = request.form["departmentid"]
                    age = request.form["age"]
                    conn=sqlite3.connect('C:\sqlite\school.db')
                    c=conn.cursor()
                    with conn:
                            c.execute("insert into students values(:StudentId,:StudentName,:Department,:Age)",{'StudentId':studid,'StudentName':studname,'Department':depid,'Age':age})
                    conn.commit()
                    return render_template("insert_success.html")
	else:
		return abort(405)
def read():
        global table_name
        conn=sqlite3.connect('C:\sqlite\school.db')
        c=conn.cursor()
        c.execute("select * from students")
        result = c.fetchall()
        conn.commit()
        result = list(result)
        k=len(result)
        l=len(result[0])
        return render_template("display.html",result=result,l=l,k=k)

@app.route('/update',methods = ["GET","POST"])
def update():
	if request.method == "POST":
            studid=request.form["studentid"]
            studname=request.form["studentname"]
            depid=request.form["departmentid"]
            age=request.form["age"]
            conn=sqlite3.connect('C:\sqlite\school.db')
            c=conn.cursor()
            with conn:
                c.execute("""update department set studentname=:studentname,departmentid=:departmentid,age=:age where studentid=:studentid""",{'studentname':studname,'departmentid':depid,'age':age,'studentid':studid})
            conn.commit()
            return render_template("update_success.html")

@app.route("/delete",methods = ["GET","POST"])
def delete():
                          if request.method == "POST":
                                  global table_name
                                  studid=request.form["studentid"]
                                  conn=sqlite3.connect('C:\sqlite\school.db')
                                  c=conn.cursor()
                                  with conn:
                                          c.execute("delete from students where StudentId=:StudentId",{'StudentId':studid})
                                  conn.commit()
                                  return render_template("delete_success.html")
                          else:
                                  return abort(405)
    
@app.route("/search",methods = ["GET","POST"])
def search():
	if request.method == "POST":
                global table_name
                studid=request.form["studentid"]
                conn=sqlite3.connect('C:\sqlite\school.db')
                c=conn.cursor()
                c.execute("select * from students where StudentId=:StudentId",{'StudentId':studid})
                result=c.fetchall()
                conn.commit()
                if len(result) ==0:
                        return render_template("display_null.html")
                else:
                        result = list(result)
                        k = len(result)
                        l = len(result[0])
                        return render_template("display.html",result=result,l=l,k=k)
                
if __name__ == "__main__":
	app.run(debug=True)
