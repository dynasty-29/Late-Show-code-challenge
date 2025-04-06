from app import app
from models import db, Episode, Guest, Appearance

with app.app_context():
    # check if table exist if it does: Drop else create tables
    db.drop_all()
    db.create_all()

    # lets create the episodes data
    episode1 = Episode(date='1/11/99', number=1)
    episode2 = Episode(date='1/12/99', number=2)
    db.session.add_all([episode1, episode2])

    # lets create the guests data
    guest1 = Guest(name='Michael J. Fox', occupation='actor')
    guest2 = Guest(name='Sandra Bernhard', occupation='Comedian')
    guest3 = Guest(name='Tracey Ullman', occupation='television actress')
    db.session.add_all([guest1, guest2, guest3])

    # lets create the appearances data
    appearance1 = Appearance(rating=4, episode_id=1, guest_id=1)
    appearance2 = Appearance(rating=5, episode_id=2, guest_id=3)
    db.session.add_all([appearance1, appearance2])

    # commit the session
    db.session.commit()
    print("Database seeded!")
