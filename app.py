# Install required packages
# pip install Flask flask-restful sqlalchemy pandas pymysql
# app.py
import pandas as pd
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from sqlalchemy import create_engine, Column, Integer, String, MetaData, Table
import os

app = Flask(__name__)
api = Api(app)

# Define MySQL database connection
DATABASE_URL = 'mysql://root:123456@localhost:3306/data_engineer_challenge'
engine = create_engine(DATABASE_URL)
metadata = MetaData()

# Define tables
departments = Table('departments', metadata,
                    Column('id', Integer, primary_key=True),
                    Column('name', String(255)),
                    )

jobs = Table('jobs', metadata,
             Column('id', Integer, primary_key=True),
             Column('name', String(255)),
             )

employees = Table('employees', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('name', String(255)),
                  Column('job_id', Integer),
                  Column('department_id', Integer),
                  )

metadata.create_all(engine)


# Function to insert batch transactions
def insert_batch_data(table, data):
    conn = engine.connect()
    try:
        conn.execute(table.insert().values(data))
        return True
    except Exception as e:
        print(f"Error inserting data: {str(e)}")
        return False
    finally:
        conn.close()


# REST API endpoint to receive historical data from CSV files
# REST API endpoint to receive historical data from CSV files
class HistoricalData(Resource):
    def post(self):
        try:
            # Specify the folder location
            folder_path = r"C:\Users\juanc\Documents\Laburo\Globant\Data engineer\Code challenge"
            # ... (existing code)

            # Iterate through files in the folder
            for filename in os.listdir(folder_path):
                filepath = os.path.join(folder_path, filename)

                print(f"Processing file: {filename}")

                # Assuming the CSV files don't have headers
                df = pd.read_csv(filepath, header=None)

                # Extract table name from filename
                table_name = filename.split('.')[0]

                # Insert batch transactions
                batch_size = 1000
                for i in range(0, len(df), batch_size):
                    batch_data = df.iloc[i:i + batch_size].to_dict(orient='records')

                    # Print the batch_data for debugging
                    print(f"Inserting data into {table_name} table: {batch_data}")

                    if not insert_batch_data(metadata.tables[table_name], batch_data):
                        return jsonify({"error": "Failed to insert data"}), 500

            return jsonify({"message": "Data uploaded successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


# Add resource to API
api.add_resource(HistoricalData, "/upload", methods=['POST'])

if __name__ == "__main__":
    app.run(debug=True)
