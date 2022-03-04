from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Painting:
    db_name = "artists_paintings"

    def __init__(self,db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.description = db_data['description']
        self.price = db_data['price']
        self.painter = db_data['painter']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM paintings;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        paintings = []
        for new_row in results:
            paintings.append( cls(new_row) )
            print(new_row['title'])
        return paintings

    @classmethod
    def save(cls,data):
        query = "INSERT INTO paintings (title, description, price, painter, user_id) VALUES (%(title)s,%(description)s,%(price)s,%(painter)s,%(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM paintings WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    @classmethod
    def get_all_with_paintor (cls):
        query = "SELECT * FROM paintings LEFT JOIN users ON paintings.user_id = users.id;"
        results = connectToMySQL(cls.db_name).query_db(query)
        print(results)
        all_paintings = []
        for one_painting in results:
            painting_data = {
                "id": one_painting['id'],
                "title": one_painting['title'],
                "description": one_painting['description'],
                "price": one_painting['price'],
                "painter": one_painting['painter'],
                "created_at": one_painting['created_at'],
                "updated_at": one_painting['updated_at']
            }
            painting_object = cls(painting_data)
            user_data = {
                "id": one_painting['users.id'],
                "first_name": one_painting['first_name'],
                "last_name": one_painting['last_name'],
                "email": one_painting['email'],
                "password": one_painting['password'],
                "created_at": one_painting['users.created_at'],
                "updated_at": one_painting['users.updated_at']
            }
            single_user = user.User(user_data)
            painting_object.painter = single_user
            all_paintings.append(painting_object)
        return results

    @classmethod
    def update(cls, data):
        query = "UPDATE paintings SET title=%(title)s, description=%(description)s, price=%(price)s, painter=%(painter)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)
    
    @classmethod
    def delete(cls,data):
        query = "DELETE FROM paintings WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_painting_report(painting):
        is_valid = True
        if len(painting['title']) < 2:
            is_valid = False
            flash("The title must be at least 2 characters", "painting")
        if len(painting['description']) < 10:
            is_valid = False
            flash("Description must be at least 10 characters", "painting")
        if float(painting['price']) <= 0:
            is_valid = False
            flash("Price should be greater than $0.00", "painting")
        return is_valid

