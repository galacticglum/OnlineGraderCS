from grader import application, db

class Problem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    points = db.Column(db.Integer)
    description = db.Column(db.Text)
    constraints = db.Column(db.Text)
    input_spec = db.Column(db.Text)
    output_spec = db.Column(db.Text)

    def __init__(self, title, points, description, constraints,
        input_spec, output_spec):
        
        self.title = title
        self.points = points
        self.description = description
        self.constraints = constraints
        self.input_spec = input_spec
        self.output_spec = output_spec


    def to_json(self):
        json_dict = {
            'id': self.id,
            'title': self.title,
            'points': self.points,
            'description': self.description,
            'constraints': self.constraints,
            'input_spec': self.input_spec,
            'output_spec': self.output_spec
        }

        return json_dict

    @staticmethod
    def find_by_id(id):
        return Problem.query.filter_by(id=id).first()