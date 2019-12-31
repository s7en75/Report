from flask import Flask, render_template, request, redirect, url_for, session
import pymysql.cursors
from config import Config
import os


app = Flask(__name__)
app.secret_key = "SECRET_KEY_5542245580_mmohsenn_panj55555"


connection = pymysql.connect(host='localhost',
                             port=8889,
                             user='root',
                             password='root',
                             db='Report',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


@app.route('/login', methods=['GET', 'POST'])
def login():
    connection = pymysql.connect(host='localhost',
                                 port=8889,
                                 user='root',
                                 password='root',
                                 db='Report',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    if request.method == 'POST':
        try:
            with connection.cursor() as cursor:
                # Create a new record
                sql = "SELECT * from User where username=%s and password=%s"
                cursor.execute(sql, (request.form['username'], request.form['password']))
                result = cursor.fetchone()

                # connection is not autocommit by default. So you must commit to save
                # your changes.
                connection.commit()
                # Write after Login page
                print(result)
                if result is not None:
                    if result['role']=='admin':
                        session['logged_in'] = 'admin'
                        session['id']=result['id']
                    elif result['role'] == 'manager':
                        session['logged_in'] = 'manager'
                        session['id'] = result['id']
                    elif result['role'] == 'user':
                        session['logged_in'] = 'user'
                        session['id'] = result['id']
                    return redirect(url_for('task'))
                else:
                    return "Not Login Data Got : "+ request.form['username']
        finally:
            connection.close()
    else:
        return render_template('login.jinja2')


@app.route('/task', methods=['GET', 'POST'])
def task():
    if 'logged_in' in session:
        id = session['id']
        with connection.cursor() as cursor:
            sql = "SELECT * FROM task_user join task  ON task_user.task_id = task.id where task_user.user_id=%s"
            cursor.execute(sql, id)
            task = cursor.fetchall()
            if request.method == 'POST':
                insert = "UPDATE `task_user` SET `dkp` = %s, `status` = 'In Progress' WHERE `task_user`.`id` = %s;"
                cursor.execute(insert, (request.form['dkp'], request.form['task_id']))
                return render_template('task.jinja2', task=task)
            else:
                return render_template('task.jinja2', task=task)
    else:
        return redirect(url_for('login'))


@app.route('/home', methods=['GET', 'POST'])
def home():
    return render_template("home.jinja2")


@app.route('/admin/assign_task', methods=['GET', 'POST'])
def assign():
    if request.method == 'POST':
        for x in range(0, len(request.form.getlist('user[]'))):
            v = int(request.form.getlist('count[]')[x])
            for i in range(0, v):
                with connection.cursor() as cursor:
                    user_id = request.form.getlist('user[]')[x]
                    task_id = request.form.getlist('task[]')[x]
                    desc = request.form.getlist('desc[]')[x]
                    insert = "INSERT INTO task_user (user_id,description ,task_id,status) VALUES (%s,%s,%s,%s)"
                    cursor.execute(insert, (user_id, desc, task_id, "Assigned"))
                    connection.commit()
        return request.form.getlist('count[]')[x]
    else:
        sql = "SELECT * FROM user"
        sql2 = "SELECT * FROM task"
        with connection.cursor() as cursor:
            cursor.execute(sql)
            user = cursor.fetchall()
        with connection.cursor() as cursor:
            cursor.execute(sql2)
            task = cursor.fetchall()
        return render_template('task_creation.jinja2', user=user, task=task)


@app.route('/test', methods=['GET', 'POST'])
def test():
    if request.method == 'POST':
        print "mohsen"
        for x in request.form.getlist('task[]'):
            print x

        #     return render_template('test.html')
    return render_template('test.html')


@app.route('/logout')
def logout():
    session.pop('id', None)
    session.pop('logged_in', None)
    session.pop('role', None)
    return redirect(url_for('task'))


if __name__ == '__main__':
    app.debug = True
    app.run()