from flask_api import FlaskAPI


def create_app(config_name=None):
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(config_name)

    from . import sample
    app.register_blueprint(sample.sample_blueprint)

    return app
