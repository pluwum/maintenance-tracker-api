from flask.views import MethodView
from flask import Blueprint

sample_blueprint = Blueprint('sample', __name__, url_prefix='/sample')


class SampleView(MethodView):
    def get(self):
        return "Hello World"


sample_blueprint.add_url_rule(
    '/', view_func=SampleView.as_view('sample_views'), methods=['GET'])
