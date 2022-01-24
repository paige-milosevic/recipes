from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from flask import flash

class User:
    db = 'recipes'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        # self.recipes = []
    
    # @classmethod
    # def getAllRecipes(cls,data):
    #     query = 'SELECT * FROM dojos LEFT JOIN recipes ON users.id = recipe.user_id WHERE user.id =%(id)s;'
    #     results = connectToMySQL(cls.db).query_db(query,data)
    #     print(results)
    #     user = cls(results[0])
    #     for row_from_db in results:
    #         recipe_data = {
    #             "name": row_from_db['name'],
    #             "under30": row_from_db['under30']
    #         }

    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email=%(email)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        user = []
        for i in results:
            user.append(i)
        if len(user) < 1:
            return False
        return cls(user[0])

    @classmethod
    def get_by_id(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])


    @classmethod
    def save(cls, data):
        query = 'INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(User.db).query_db(query,user)
        if len(results) >= 1:
            flash('Email already in use.', 'register')
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid Email!', 'register')
            is_valid = False
        if len(user['first_name']) < 3:
            flash('First name must be at least 3 characters', 'register')
            is_valid = False
        if len(user['last_name']) < 3:
            flash('Last name must be at least 3 characters', 'register')
            is_valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters', 'register')
            is_valid = False
        if user['password'] != user['passCon']:
            flash('Passwods do not match', 'register')
        return is_valid