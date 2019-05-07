from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
import time


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    packages = db.relationship('Package', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Package(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    package_name = db.Column(db.String(64), index=True)
    package_content = db.Column(db.String(512))
    package_path = db.Column(db.String(256))
    package_version = db.Column(db.String(16))
    create_time = db.Column(db.DateTime, index=True, default=time.strftime('%Y-%m-%d %H:%M:%S'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Package {}>'.format(self.package_name)

    def get_packages(self):
        return Package.query.order_by(Package.create_time.desc()).all()


class UpgradeLog(db.Model):
    __tablename__ = "upgrade_log"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(32))
    content = db.Column(db.String(1024))
    create_time = db.Column(db.DateTime, index=True)
    modify_time = db.Column(db.DateTime, index=True)
    creator = db.Column(db.String(32))