from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


association_table = db.Table(
    "association_table_roles",
    db.Column("user", db.Integer, db.ForeignKey("user.id")),
    db.Column("role", db.Integer, db.ForeignKey("role.id")),
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    role = db.relationship("Role", secondary=association_table)

    def __init__(self, name, lastname, email, password):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "roles": [rol.serialize() for rol in self.role ]
            # do not serialize the password, its a security breach
        }


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return '<Role %r>' % self.role

    def serialize(self):
        return {
            "id": self.id,
            "role": self.role
        }


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    image = db.Column(db.String(9999), nullable=False)
    business = db.Column(db.String(40), nullable=False)
    description = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(20), nullable=False)

    def repr(self):
        return '<Client %r>' % self.name

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "phone": self.phone,
            "image": self.image,
            "business": self.business,
            "description": self.description,
            "status": self.status
        }

class Row(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    text = db.Column(db.Text, nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "user_id":self.user_id,
            "text": self.text
        }


