import sqlite3
from model_types import ModelType
from itertools import chain

class DatabaseLayer:
    def __init__(self):
        self.conn = sqlite3.connect('database.db')
        self.cursor = self.conn.cursor()
        self.create_model_table()

    def create_model_table(self):
        model_types = "', '".join([model_type.model_name for model_type in ModelType])

        self.cursor.execute(
            f'''
                CREATE TABLE IF NOT EXISTS models(
                    id INTEGER PRIMARY KEY, 
                    model_name TEXT, 
                    model_type TEXT CHECK(model_type IN ('{model_types}')), 
                    model BLOB
            )'''
        )
        self.conn.commit()

    def add_model(self, model_name: str, model_type: ModelType, model):
        insert_query = '''
            INSERT INTO models (model_name, model_type, model) 
            VALUES (:model_name, :model_type, :model)
        '''
        self.cursor.execute(insert_query, {
            'model_name': model_name, 'model_type': model_type.model_name, 'model': model
        })
        self.conn.commit()


    def delete_model(self, model_name: str):
        self.cursor.execute(
            "DELETE FROM models WHERE model_name = :model_name",
            { 'model_name': model_name }
        )
        self.conn.commit()


    def get_model(self, name: str):
        self.cursor.execute(
            'SELECT model_type, model FROM models WHERE model_name = :model_name', 
            {'model_name': name}
        )
        result = self.cursor.fetchone()
        if result is not None:
            model_type, model = result
            return ModelType.from_name(model_type), model
        return None, None

    def get_models(self):
        models = self.cursor.execute('SELECT model_name FROM models').fetchall()
        return list(chain.from_iterable(models))


