import models
from app import db, create_app
from werkzeug.security import generate_password_hash

def main():
    app = create_app()
    with app.app_context():
        db.create_all()

        savings_ir = 0.25
        savings_min = 5.0
        checkings_ir = 0.0
        checkings_min = 0.0

        db.session.add(models.Bank_Settings(savings_ir=savings_ir,
        savings_min=savings_min, checkings_ir=checkings_ir, 
        checkings_min=checkings_min))

        db.session.add(models.User(id=1, username='executive',
                                   password=generate_password_hash(
                                    'HarrisonWells', method='sha256'),
                                   name='admin'))

        db.session.commit()

    return 1

if __name__ == '__main__':
    main()