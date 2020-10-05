from . import db


class Taxonomies(db.Model):
    taxonomy_id = db.Column(db.Integer, primary_key=True)
    taxonomy_common_name = db.Column(db.String(80))
    taxonomy_scientific_name = db.Column(db.String(80))
    projects = db.relationship('Projects', backref='taxonomy', lazy=True)

    def __init__(
            self,
            taxonomy_id,
            taxonomy_common_name,
            taxonomy_scientific_name
    ):
        self.taxonomy_id = taxonomy_id
        self.taxonomy_common_name = taxonomy_common_name
        self.taxonomy_scientific_name = taxonomy_scientific_name

    def dictify(self):
        return {
            'taxonomy_id': self.taxonomy_id,
            'taxonomy_common_name': self.taxonomy_common_name,
            'taxonomy_scientific_name': self.taxonomy_scientific_name,
        }


class Projects(db.Model):
    project_id = db.Column(db.String, primary_key=True)
    title = db.Column(db.Text)
    description = db.Column(db.Text)
    source_type = db.Column(db.String(80))
    study_type = db.Column(db.String(80))
    eva_center_name = db.Column(db.String(80))
    center_name = db.Column(db.String(80))
    taxonomy_id = db.Column(
        db.Integer,
        db.ForeignKey('taxonomies.taxonomy_id')
    )

    def __init__(
            self,
            project_id,
            title,
            description,
            source_type,
            study_type,
            eva_center_name,
            taxonomy_id
    ):
        self.project_id = project_id
        self.title = title
        self.description = description
        self.source_type = source_type
        self.study_type = study_type
        self.eva_center_name = eva_center_name
        self.taxonomy_id = taxonomy_id

    def dictify(self):
        return {
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'source_type': self.source_type,
            'study_type': self.study_type,
            'eva_center_name': self.eva_center_name,
            'center_name': self.center_name,
            'taxonomy_id': self.taxonomy_id,
        }
