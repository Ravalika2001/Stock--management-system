from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base

db = SQLAlchemy()
Base = declarative_base()

# DATABASE_URI = "postgresql+psycopg2://postgres:Password0#@localhost:5432/CC"

DATABASE_URI = "postgresql://postgres:Password0#@database1.cuetvdodk2bh.us-east-1.rds.amazonaws.com:5432/final "


# Create the engine and bind it to the session
engine = create_engine(DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

def init_db(app):
    app.teardown_appcontext(teardown_db)
    app.cli.add_command(init_database)
    db.init_app(app)

def teardown_db(exception=None):
    db_session.remove()

def init_database():
    from models import Supplier, Product, Category, SupplierOrder, SupplierOrderItem, ConsumerOrder, ConsumerOrderItem, C
    from flask import current_app
    db.drop_all(bind=engine)
    db.create_all(bind=engine)
    current_app.logger.info('Initialized the database.')

