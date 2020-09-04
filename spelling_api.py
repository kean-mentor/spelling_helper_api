from flask import Flask

from models import db, populate_db
from configs import ApiConfig


def create_app(config_class=ApiConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)

    from api import bp
    app.register_blueprint(bp)

    return app


app = create_app()
db.create_all(app=app)

# Add words to the database if it is empty
if not app.config['TESTING']:
    populate_db(app)
