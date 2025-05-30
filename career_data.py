class CareerRecommendationEngine:
    def __init__(self):
        # Database karir sederhana
        self.careers = {
            'Software Developer': {
                'category': 'Teknologi',
                'required_skills': ['Programming', 'Problem Solving'],
                'personality_match': ['Analytical', 'Introvert'],
                'education': ['S1', 'D3'],
                'min_experience': 0,
                'description': 'Mengembangkan aplikasi dan sistem software',
                'salary_range': '8-25 juta/bulan'
            },
            'Data Analyst': {
                'category': 'Teknologi',
                'required_skills': ['Excel', 'Statistics', 'Data Analysis'],
                'personality_match': ['Analytical', 'Detail-oriented'],
                'education': ['S1', 'D3'],
                'min_experience': 0,
                'description': 'Menganalisis data untuk insight bisnis',
                'salary_range': '7-20 juta/bulan'
            },
            'Digital Marketing': {
                'category': 'Bisnis',
                'required_skills': ['Social Media', 'Content Creation'],
                'personality_match': ['Creative', 'Extrovert'],
                'education': ['S1', 'D3', 'SMA'],
                'min_experience': 0,
                'description': 'Mengelola pemasaran digital dan media sosial',
                'salary_range': '5-15 juta/bulan'
            },
            'UI/UX Designer': {
                'category': 'Kreatif',
                'required_skills': ['Design', 'User Research', 'Prototyping'],
                'personality_match': ['Creative', 'Empathetic'],
                'education': ['S1', 'D3'],
                'min_experience': 0,
                'description': 'Merancang interface dan user experience',
                'salary_range': '7-22 juta/bulan'
            },
            'Business Analyst': {
                'category': 'Bisnis',
                'required_skills': ['Analysis', 'Communication', 'Problem Solving'],
                'personality_match': ['Analytical', 'Communicative'],
                'education': ['S1'],
                'min_experience': 1,
                'description': 'Menganalisis proses bisnis dan memberikan solusi',
                'salary_range': '8-25 juta/bulan'
            }
        }
        
        # Pertanyaan tes kepribadian sederhana
        self.personality_questions = [
            {
                'question': 'Saya lebih suka bekerja:',
                'options': [
                    {'text': 'Sendiri dengan fokus tinggi', 'traits': ['Introvert', 'Analytical']},
                    {'text': 'Dalam tim dengan banyak diskusi', 'traits': ['Extrovert', 'Communicative']},
                    {'text': 'Fleksibel tergantung situasi', 'traits': ['Adaptable']}
                ]
            },
            {
                'question': 'Ketika menghadapi masalah, saya:',
                'options': [
                    {'text': 'Menganalisis data dan fakta', 'traits': ['Analytical', 'Detail-oriented']},
                    {'text': 'Mencari solusi kreatif', 'traits': ['Creative', 'Innovative']},
                    {'text': 'Diskusi dengan orang lain', 'traits': ['Communicative', 'Collaborative']}
                ]
            },
            {
                'question': 'Saya paling termotivasi ketika:',
                'options': [
                    {'text': 'Menyelesaikan tugas dengan detail', 'traits': ['Detail-oriented', 'Perfectionist']},
                    {'text': 'Membuat sesuatu yang baru', 'traits': ['Creative', 'Innovative']},
                    {'text': 'Membantu orang lain', 'traits': ['Empathetic', 'Helper']}
                ]
            },
            {
                'question': 'Dalam bekerja, saya lebih fokus pada:',
                'options': [
                    {'text': 'Proses dan sistem yang teratur', 'traits': ['Systematic', 'Organized']},
                    {'text': 'Hasil akhir dan pencapaian', 'traits': ['Goal-oriented', 'Achiever']},
                    {'text': 'Hubungan dan kerjasama tim', 'traits': ['Team-player', 'Communicative']}
                ]
            }
        ]

    def get_personality_questions(self):
        return self.personality_questions

    def analyze_personality(self, answers):
        trait_scores = {}
        
        for i, answer_index in enumerate(answers):
            if i < len(self.personality_questions) and answer_index < len(self.personality_questions[i]['options']):
                traits = self.personality_questions[i]['options'][answer_index]['traits']
                for trait in traits:
                    trait_scores[trait] = trait_scores.get(trait, 0) + 1
        
        # Get top 3 traits
        sorted_traits = sorted(trait_scores.items(), key=lambda x: x[1], reverse=True)
        dominant_traits = [trait[0] for trait in sorted_traits[:3]]
        
        return {
            'dominant_traits': dominant_traits,
            'all_scores': trait_scores
        }

    def generate_recommendations(self, profile, personality):
        recommendations = []
        
        for career_name, career_data in self.careers.items():
            score = 0
            reasoning = []
            
            # 1. Education match (30%)
            if profile['education'] in career_data['education']:
                score += 30
                reasoning.append(f"Pendidikan {profile['education']} sesuai persyaratan")
            else:
                reasoning.append("Pendidikan perlu dipertimbangkan")
            
            # 2. Experience match (20%)
            if profile['experience'] >= career_data['min_experience']:
                score += 20
                reasoning.append(f"Pengalaman {profile['experience']} tahun mencukupi")
            else:
                reasoning.append(f"Perlu minimal {career_data['min_experience']} tahun pengalaman")
            
            # 3. Interest match (25%)
            user_interests = [interest.lower() for interest in profile['interests']]
            career_category = career_data['category'].lower()
            if any(career_category in interest or interest in career_category for interest in user_interests):
                score += 25
                reasoning.append(f"Minat pada {career_data['category']} sangat sesuai")
            else:
                reasoning.append("Bidang minat kurang sesuai")
            
            # 4. Personality match (15%)
            personality_matches = 0
            for trait in career_data['personality_match']:
                if trait in personality['dominant_traits']:
                    personality_matches += 1
            
            personality_score = (personality_matches / len(career_data['personality_match'])) * 15
            score += personality_score
            if personality_matches > 0:
                reasoning.append(f"Kepribadian {', '.join(personality['dominant_traits'][:personality_matches])} cocok")
            
            # 5. Skills match (10%)
            skill_matches = 0
            user_skills = [skill.lower() for skill in profile['skills']]
            for req_skill in career_data['required_skills']:
                if any(req_skill.lower() in user_skill or user_skill in req_skill.lower() for user_skill in user_skills):
                    skill_matches += 1
            
            skill_score = (skill_matches / len(career_data['required_skills'])) * 10
            score += skill_score
            if skill_matches > 0:
                reasoning.append(f"{skill_matches} dari {len(career_data['required_skills'])} skill sesuai")
            
            recommendations.append({
                'career': career_name,
                'score': round(score, 1),
                'category': career_data['category'],
                'description': career_data['description'],
                'salary_range': career_data['salary_range'],
                'required_skills': career_data['required_skills'],
                'reasoning': reasoning,
                'match_level': 'Tinggi' if score >= 70 else 'Sedang' if score >= 50 else 'Rendah'
            })
        
        # Sort by score
        recommendations.sort(key=lambda x: x['score'], reverse=True)
        return recommendations[:5]  # Top 5 recommendations