from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

class Recipe:
    db = "recipes"

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under30 = data['under30']
        self.dateMade = data['dateMade']
        self.user_id = data ['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = 'INSERT INTO recipes (name, description, instructions, under30, dateMade, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(under30)s, %(dateMade)s, %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)
    
    @classmethod
    def getOne(cls,data):
        query = 'SELECT * FROM recipes WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def getAll(cls):
        query = 'SELECT * FROM recipes;'
        results = connectToMySQL(cls.db).query_db(query)
        allRecipes = []
        for row in results:
            print(row['dateMade'])
            allRecipes.append(cls(row))
        return allRecipes

    @classmethod
    def update(cls,data):
        query = 'UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, under30=%(under30)s, dateMade=%(dateMade)s, updated_at=NOW() WHERE id=%(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = 'DELETE FROM recipes WHERE id=%(id)s;'
        return connectToMySQL(cls.db).query_db(query,data)

    @staticmethod
    def validateRecipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters","recipe")
        if len(recipe['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters","recipe")
        if len(recipe['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","recipe")
        if recipe['dateMade'] == "":
            is_valid = False
            flash("Please enter a date","recipe")
        return is_valid