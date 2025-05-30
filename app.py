from flask import Flask, render_template, request, jsonify, session
from career_data import CareerRecommendationEngine
import uuid

app = Flask(__name__)
app.secret_key = 'career-advisor-secret-2024'

# Initialize recommendation engine
career_engine = CareerRecommendationEngine()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/save-profile', methods=['POST'])
def save_profile():
    data = request.get_json()
    
    # Generate session ID if not exists
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())
    
    # Save profile data to session
    session['profile'] = {
        'name': data.get('name'),
        'education': data.get('education'),
        'experience': int(data.get('experience', 0)),
        'interests': data.get('interests', []),
        'skills': [s.strip() for s in data.get('skills', '').split(',') if s.strip()]
    }
    
    return jsonify({'success': True, 'message': 'Profil berhasil disimpan'})

@app.route('/api/personality-test', methods=['GET'])
def get_personality_test():
    questions = career_engine.get_personality_questions()
    return jsonify(questions)

@app.route('/api/submit-test', methods=['POST'])
def submit_test():
    data = request.get_json()
    answers = data.get('answers', [])
    
    # Analyze personality
    personality_result = career_engine.analyze_personality(answers)
    session['personality'] = personality_result
    
    return jsonify({
        'success': True, 
        'personality': personality_result,
        'message': 'Tes kepribadian selesai'
    })

@app.route('/api/recommendations', methods=['GET'])
def get_recommendations():
    if 'profile' not in session or 'personality' not in session:
        return jsonify({'error': 'Lengkapi profil dan tes kepribadian terlebih dahulu'})
    
    profile = session['profile']
    personality = session['personality']
    
    # Generate recommendations using AI reasoning
    recommendations = career_engine.generate_recommendations(profile, personality)
    
    return jsonify(recommendations)

if __name__ == '__main__':
    app.run(debug=True)