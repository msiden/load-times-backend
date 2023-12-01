import connexion
from flask_cors import CORS


def app():
    app = connexion.FlaskApp(__name__, specification_dir='.')
    app.add_api('api_spec.yaml')
    CORS(app.app, origins='*')
    return app
