import os
import tempfile

import werkzeug
import pytest

from app import studies, study, create_app
from db import db
from db.models import Taxonomies, Projects


@pytest.fixture
def client():
    db_file, db_filename = tempfile.mkstemp()
    app = create_app(db_filename)
    app.config['TESTING'] = True

    # test data
    taxonomies = [
        Taxonomies(1, 'Sheep', 'Ovis orientalis'),
        Taxonomies(2, 'Sheep', 'Ovis vignei'),
        Taxonomies(3, 'Mouse', 'Mus'),
        Taxonomies(4, 'Common bean', 'Phaseolus vulgaris')
    ]
    projects = [
        Projects(1, 'Project 1', '', None, None, None, 1),
        Projects(2, 'Project 2', '', None, None, None, 1),
        Projects(3, 'Project 3', '', None, None, None, 3),
        Projects(4, 'Project 4', '', None, None, None, 2),
    ]

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

            for t in taxonomies:
                db.session.add(t)
            for p in projects:
                db.session.add(p)
            db.session.commit()

        yield client

    os.close(db_file)
    os.remove(db_filename)


def test_get_studies(client):
    with client.application.test_request_context('/studies'):
        response = studies()
        assert response.status_code == 200
        result_ids = [r['project_id'] for r in response.json['results']]
        assert result_ids == ['1', '2', '3', '4']


def test_get_studies_common_name_present(client):
    with client.application.test_request_context(
            '/studies?taxonomy_common_name=sheep'
    ):
        response = studies()
        assert response.status_code == 200
        result_ids = [r['project_id'] for r in response.json['results']]
        assert result_ids == ['1', '2', '4']


def test_get_studies_common_name_absent(client):
    with client.application.test_request_context(
            '/studies?taxonomy_common_name=potato'
    ):
        response = studies()
        assert response.status_code == 200  # probably not ideal
        assert len(response.json['results']) == 0


def test_get_study_pid_present(client):
    with client.application.test_request_context('/study'):
        response = study(3)
        assert response.status_code == 200
        assert response.json['project_id'] == '3'


def test_get_study_pid_absent(client):
    with client.application.test_request_context('/study'):
        with pytest.raises(werkzeug.exceptions.NotFound):
            _ = study(42)
