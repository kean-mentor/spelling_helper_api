from flask import Flask

from configs import WebConfig


def create_app(config_class=WebConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    from web import bp
    app.register_blueprint(bp)

    return app


app = create_app()
