from werkzeug.security import generate_password_hash
from website import create_app, models

def setup():
    """
    Sets up the database for the app with some default data.
    """    

    app = create_app()

    # Now we can do things within the context of the app.
    with app.app_context():
        
        # Creates all tables
        models.db.create_all()

        savings_apy = 0.25
        savings_min = 5.0
        checkings_apy = 0.0
        checkings_min = 0.0

        # Creates the default bank settings.
        models.db.session.add(models.Bank_Settings(savings_apy=savings_apy,
        savings_min=savings_min, checkings_apy=checkings_apy, 
        checkings_min=checkings_min))

        # Creates the default admin user.
        models.db.session.add(models.User(id=1, username='executive', 
        password=generate_password_hash('HarrisonWells', method='sha256'), 
        name='Admin'))

        # Initializes the current term to be 0.
        models.db.session.add(models.Curr_Term(term=0))

        # Commit to database
        models.db.session.commit()

if __name__ == '__main__':
    main()