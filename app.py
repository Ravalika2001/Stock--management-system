from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from strawberry.flask.views import GraphQLView
from schemas import schema
from database import init_db

app = Flask(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://postgres:Password0#@localhost:5432/CC"
app.config["SQLALCHEMY_DATABASE_URI"] = ("postgresql://postgres:Password0#@database1.cuetvdodk2bh.us-east-1.rds.amazonaws.com:5432/final ")

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

def create_app():
    try:
        init_db()
    except Exception as e:
        print(f"An error occurred while initializing the database: {str(e)}")

    app.add_url_rule(
        "/graphql",
        view_func=GraphQLView.as_view("graphql", schema=schema),
    )

    @app.route("/")
    def index():
        return "Stock Management App"

    return app

if __name__ == "__main__":
    try:
        stock_management_app = create_app()
        stock_management_app.run()
    except Exception as e:
        print(f"An error occurred while running the application: {str(e)}")
