from flask import Flask, request, make_response
from sqlalchemy import func

from db import db
from db.models import Taxonomies, Projects

# should be in a config file
DB_FILENAME = '/tmp/test.db'


def create_app(db_filename=DB_FILENAME):
    """Initialise flask app and db."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_filename}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    return app


app = create_app()


@app.route('/studies')
def studies():
    """Return studies with given taxonomy common name (provided in query params),
    or all studies if none provided."""
    common_name = request.args.get('taxonomy_common_name', '').lower()
    if common_name == '':
        results = Projects.query.all()
    else:
        results = Projects.query.join(Taxonomies).filter(
            func.lower(Taxonomies.taxonomy_common_name) == common_name
        ).all()
    return make_response({'results': [r.dictify() for r in results]})


@app.route('/study/<pid>')
def study(pid):
    """Return study with given project id, or 404 if not found."""
    result = Projects.query.get_or_404(pid)
    return make_response(result.dictify())


if __name__ == '__main__':
    app.run(port=7799)
