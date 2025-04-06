from flask import Flask, jsonify, request
from models import db, Episode, Guest, Appearance

# Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///lateshow.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# database
db.init_app(app)

# Index Route added just for fun 
@app.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to my code challenge solving!"}), 200

# Route to get all episodes
@app.route('/episodes', methods=['GET'])
def get_episodes():
    episodes = Episode.query.all()
    return jsonify([episode.to_dict() for episode in episodes]), 200

# Route to get a specific episode by id
@app.route('/episodes/<int:id>', methods=['GET'])
def get_episode(id):
    episode = Episode.query.get(id)
    if episode:
        return jsonify(episode.to_dict(include_appearances=True)), 200
    return jsonify({"error": "Episode not found"}), 404

# Route to get all guests
@app.route('/guests', methods=['GET'])
def get_guests():
    guests = Guest.query.all()
    return jsonify([guest.to_dict() for guest in guests]), 200

#  Route to create a new appearance
@app.route('/appearances', methods=['POST'])
def create_appearance():
    data = request.get_json()
    rating = data.get('rating')
    
    # I need to validate rating
    if rating is None or not (1 <= rating <= 5):
        return jsonify({"errors": ["Rating must be between 1 and 5"]}), 400
    try:
        # Check if episode and guest exist
        episode = Episode.query.get(data['episode_id'])
        guest = Guest.query.get(data['guest_id'])
        
        if not episode:
            return jsonify({"errors": ["Episode not found"]}), 404
        if not guest:
            return jsonify({"errors": ["Guest not found"]}), 404
        
        # once all is done create and add the appearance
        appearance = Appearance(
            rating=rating,
            episode_id=data['episode_id'],
            guest_id=data['guest_id']
        )
        db.session.add(appearance)
        db.session.commit()
        return jsonify(appearance.to_dict(include_episode=True, include_guest=True)), 201
    except Exception as e:
        return jsonify({"errors": ["Invalid data", str(e)]}), 400



if __name__ == '__main__':
    app.run(debug=True)
