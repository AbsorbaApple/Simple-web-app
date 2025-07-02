from Connection import get_connection
from flask import Flask,render_template,abort,request,redirect,url_for
app=Flask(__name__)
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        student_name = request.form.get('student_name')
        student_dob = request.form.get('student_dob')
        student_email = request.form.get('student_email')

        connection = get_connection()
        with connection.cursor() as cur:
            sql_stmt = "INSERT INTO student (student_name, date_of_birth, student_email) VALUES (?, ?, ?)"
            values = (student_name, student_dob, student_email)
            cur.execute(sql_stmt, values)
            connection.commit()
        connection.close()

    # ✅ ALWAYS run this part to get the student list
    connection = get_connection()
    with connection.cursor() as cur:
        sql_stmt = "SELECT * FROM student"
        cur.execute(sql_stmt)
        res = cur.fetchall()
    connection.close()

    return render_template('index.html', students=res)

@app.route('/delete/<int:student_id>', methods=['POST', 'GET'])
def delete_student(student_id):
    connection = get_connection()
    with connection.cursor() as cur:
        cur.execute("DELETE FROM student WHERE id = ?", (student_id,))
        connection.commit()
    connection.close()
    return redirect(url_for('index'))


@app.route("/student/<int:id>")
def get_student(id):
    connection=get_connection()
    with connection.cursor() as cur:
        sql_stmt="SELECT * FROM student where id=?"
        cur.execute(sql_stmt,(id,))
        res=cur.fetchone()
    connection.close()
    if res is None:
        abort(404)

    return render_template('student_detail.html',student=res)




@app.route('/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    connection = get_connection()

    if request.method == 'POST':
        # Get updated data from form
        student_name = request.form.get('student_name')
        student_dob = request.form.get('student_dob')
        student_email = request.form.get('student_email')

        with connection.cursor() as cur:
            # Update student in database
            cur.execute("""
                UPDATE student
                SET student_name = ?, date_of_birth = ?, student_email = ?
                WHERE id = ?
            """, (student_name, student_dob, student_email, student_id))
            connection.commit()

        connection.close()
        return redirect(url_for('index'))

    # For GET request, fetch student data to pre-fill form
    with connection.cursor() as cur:
        cur.execute("SELECT * FROM student WHERE id = ?", (student_id,))
        student = cur.fetchone()

    connection.close()

    if student:
        return render_template('edit.html', student=student)
    else:
        abort(404)

if __name__ == "__main__":
    app.run(debug=True)