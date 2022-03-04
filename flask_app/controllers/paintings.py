from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.painting import Painting
from flask_app.models.user import User

#Directs the user to a new page in order to add a painting.
@app.route('/add/painting')
def add_painting():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('add_painting.html',user=User.get_by_id(data))

#Process the user's request to add a painting.
@app.route('/new/painting',methods=['POST'])
def new_painting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Painting.validate_painting_report(request.form):
        return redirect('/add/painting')
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "price": request.form["price"],
        "painter": request.form["painter"],
        "user_id": session["user_id"]
    }
    Painting.save(data)
    return redirect('/dashboard')

#Directs the user to a new page in order to edit their painting.
@app.route('/edit/painting/<int:id>')
def edit_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }
    return render_template("edit_painting.html",edit=Painting.get_one(data),user=User.get_by_id(user_data))

#Process the user's request to edit their painting.
@app.route('/update/painting',methods=['POST'])
def update_painting():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Painting.validate_painting_report(request.form):
        return redirect('/add/painting')
    data = {
        "title": request.form["title"],
        "description": request.form["description"],
        "price": int(request.form["price"]),
        "painter": request.form["painter"],
        "id": request.form['id']
    }
    Painting.update(data)
    return redirect('/dashboard')

#Directs the user to a new page in order to view the painting.
@app.route('/painting/<int:id>')
def show_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }

    user_data = {
        "id":session['user_id']
    }
    return render_template("show_painting.html", painting = Painting.get_one(data), user=User.get_by_id(user_data))

#Process the user's request to delete one of their paintings.
@app.route('/delete/painting/<int:id>')
def delete_painting(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Painting.delete(data)
    return redirect('/dashboard')

