import argparse
import logging

from sqlalchemy.exc import IntegrityError

from app import create_app
from db import db


def execute_sql_file(db, filename):
    with open(filename, 'r') as f:
        commands = f.readlines()
        for command in commands:
            try:
                db.session.execute(command)
            except IntegrityError as e:
                logging.error(e)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Load taxonomies and projects database from files.')
    parser.add_argument('--taxonomies', help='taxonomies filename')
    parser.add_argument('--projects', help='projects filename')
    args = parser.parse_args()

    app = create_app()
    app.app_context().push()

    db.create_all()

    if args.taxonomies:
        execute_sql_file(db, args.taxonomies)
        logging.info('Taxonomies data added.')
    if args.projects:
        execute_sql_file(db, args.projects)
        logging.info('Projects data added.')
    if not (args.taxonomies or args.projects):
        logging.warning('Database created but no data added; '
                        'maybe you forgot to pass a filename?')

    db.session.commit()
