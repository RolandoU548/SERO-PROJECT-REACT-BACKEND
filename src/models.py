from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


association_table = db.Table(
    "association_table_role",
    db.Column("user", db.Integer, db.ForeignKey("user.id")),
    db.Column("role", db.Integer, db.ForeignKey("role.id")),
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    createdAt = db.Column(db.DateTime, nullable=False)
    role = db.relationship("Role", secondary=association_table)
    status = db.Column(db.String(20), nullable=True)
    phone = db.Column(db.Integer, nullable=True)
    address = db.Column(db.String(120), nullable=True)
    birthday = db.Column(db.DateTime, nullable=True)



    def init(self, name, lastname, email, password):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = password

    def repr(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "lastname": self.lastname,
            "email": self.email,
            "createdAt": self.createdAt,
            "status": self.status,
            "phone": self.phone,
            "address": self.address,
            "birthday": self.birthday,
            "role": [rol.serialize() for rol in self.role ]
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

    def __repr__(self):
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

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(120), nullable=False)
    method = db.Column(db.String(120), nullable=False)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    invoice = db.Column(db.String(120), nullable=False)
    service = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(20), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('client.id'), nullable=False)
    client = db.relationship('Client', backref=db.backref('payments', lazy=True))

    def __repr__(self):
        return '<Payment %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "status": self.status,
            "method": self.method,
            "date": self.date.strftime('%m/%d/%Y'),
            "amount": str(self.amount),
            "invoice": self.invoice,
            "service": self.service,
            "description": self.description,
            "client": self.client_id
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

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    completed = db.Column(db.Boolean, default=False, nullable=False)
    date = db.Column(db.Date, nullable=False)
    text = db.Column(db.String(120), nullable=False)
    
    def __repr__(self):
        return '<Task %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "completed": self.completed,
            "date": self.date.strftime('%Y-%m-%d'),
            "text": self.text
        }

class InvitationClientForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invitation_hash = db.Column(db.String(9999), nullable=False)
    expired_form = db.Column(db.Boolean, nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "invitation_hash":self.invitation_hash,
            "expired_form": self.expired_form
        }

class InvitationDatabaseForm(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    invitation_hash = db.Column(db.String(9999), nullable=False)
    expired_form = db.Column(db.Boolean, nullable=False)
    def serialize(self):
        return {
            "id": self.id,
            "invitation_hash":self.invitation_hash,
            "expired_form": self.expired_form
        }
