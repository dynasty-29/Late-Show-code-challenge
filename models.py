from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# my episode table should look like this
class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    number = db.Column(db.Integer, nullable=False)
    
    # the one-to-many relationship with the Appearance model
    appearances = db.relationship('Appearance', backref='episode', cascade='all, delete-orphan')

    # the to_dict method to convert the episode object to a dictionary
    def to_dict(self, include_appearances=False):
        data = {
            'id': self.id,
            'date': self.date,
            'number': self.number
        }
        if include_appearances:
            data['appearances'] = [appearance.to_dict(include_guest=True) for appearance in self.appearances]
        return data

# my guest table should look like this
class Guest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    occupation = db.Column(db.String, nullable=False)
    
    # the one-to-many relationship with the Appearance model
    appearances = db.relationship('Appearance', backref='guest', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'occupation': self.occupation
        }


# Appearance Model
class Appearance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'), nullable=False)
    guest_id = db.Column(db.Integer, db.ForeignKey('guest.id'), nullable=False)

    def to_dict(self, include_episode=False, include_guest=False):
        data = {
            'id': self.id,
            'rating': self.rating,
            'episode_id': self.episode_id,
            'guest_id': self.guest_id
        }
        # This is where i went wrong before let see if it works
        # i need to check if episode and guest exist, and include them in the dict
        if include_episode:
            data['episode'] = {
                'id': self.episode.id,
                'date': self.episode.date,
                'number': self.episode.number
            }
        if include_guest:
            data['guest'] = {
                'id': self.guest.id,
                'name': self.guest.name,
                'occupation': self.guest.occupation
            }
        return data

