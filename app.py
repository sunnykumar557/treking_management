from flask import Flask
from router import user_bp, dashboard_bp
from models import db,User

app = Flask(__name__)

app.config['SECRET_KEY'] = 'your_super_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


def create_default_admin():
    admin = User.query.filter_by(email = "admin@admin.com").first()
    if not admin:
        admin = User(
            fullname="Admin User",
            email="admin@admin.com",
            password="admin123",
            role= "admin"
        )
        db.session.add(admin)
        db.session.commit()
        print("Default admin user created.")
    else:
        print("Default admin user already exists.")

app.register_blueprint(user_bp)
app.register_blueprint(dashboard_bp)


if __name__ == "__main__":

    with app.app_context():
        db.create_all()
        create_default_admin()

    app.run(debug = True)