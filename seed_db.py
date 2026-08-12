from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
from config import Config

def seed():
    print("Connecting to MongoDB for database seeding...")
    client = MongoClient(Config.MONGO_URI, serverSelectionTimeoutMS=5000)
    db_name = Config.MONGO_URI.split("/")[-1].split("?")[0] or "ielts_master_hub"
    db = client[db_name]

    print("Seeding Users...")
    db.users.delete_many({})
    
    admin_user = {
        "full_name": "Admin Manager",
        "email": "admin@ielts.uz",
        "password_hash": generate_password_hash("admin123"),
        "target_band": 8.0,
        "current_band": 8.0,
        "subscription": "premium",
        "role": "admin",
        "created_at": datetime.utcnow(),
        "streak": 15,
        "last_login_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=admin@ielts.uz"
    }

    demo_user = {
        "full_name": "Bekzod Rahimov",
        "email": "user@ielts.uz",
        "password_hash": generate_password_hash("user123"),
        "target_band": 7.0,
        "current_band": 6.5,
        "subscription": "free",
        "role": "user",
        "created_at": datetime.utcnow(),
        "streak": 5,
        "last_login_date": datetime.utcnow().strftime("%Y-%m-%d"),
        "avatar": "https://api.dicebear.com/7.x/avataaars/svg?seed=user@ielts.uz"
    }

    db.users.insert_many([admin_user, demo_user])

    print("Seeding Reading Tests...")
    db.reading_tests.delete_many({})
    reading_tests = [
        {
            "title": "Passage 1: The Future of Artificial Intelligence",
            "difficulty": "Medium",
            "time_limit": 20,
            "passage_text": """Artificial Intelligence (AI) has progressed rapidly over the past decade. Once confined to science fiction, AI technologies now power search engines, recommendation systems, medical diagnostics, and autonomous vehicles.

The rise of machine learning algorithms, particularly deep learning inspired by the human brain's neural networks, has enabled computers to process massive datasets and recognize complex patterns. Researchers note that AI applications are accelerating breakthroughs in climate modeling, drug discovery, and robotics.

However, ethical concerns remain prominent. Questions regarding data privacy, algorithmic bias, and potential job displacement continue to spark global debate. Experts emphasize the necessity of human oversight and transparent safety frameworks as AI models become increasingly sophisticated.""",
            "questions": [
                {
                    "id": 1,
                    "type": "multiple_choice",
                    "question": "What has enabled computers to process massive datasets and recognize complex patterns?",
                    "options": ["Deep learning algorithms", "Traditional computing", "Quantum physics", "Human brain implants"],
                    "correct_answer": "Deep learning algorithms",
                    "explanation": "Matnda 'deep learning inspired by the human brain's neural networks, has enabled computers to process massive datasets' deb aniq ko'rsatilgan."
                },
                {
                    "id": 2,
                    "type": "text",
                    "question": "Data privacy and algorithmic bias are ethical concerns. (True/False/Not Given)",
                    "correct_answer": "True",
                    "explanation": "Matnning oxirgi xatboshisida ushbu axloqiy xavotirlar haqida gapirilgan."
                }
            ]
        },
        {
            "title": "Passage 2: The Migration of Monarch Butterflies",
            "difficulty": "Hard",
            "time_limit": 20,
            "passage_text": """Every autumn, millions of Monarch butterflies undertake an extraordinary journey across North America. Traveling up to 3,000 miles from southern Canada to the oyamel fir forests of central Mexico, these delicate insects demonstrate remarkable navigational capabilities.

Scientists have discovered that Monarchs utilize a combination of a solar compass and magnetic sensors to maintain direction. Despite weighing less than a gram, they navigate across mountains and rivers with astonishing accuracy.

Regrettably, habitat degradation, deforestation, and climate variations pose critical threats to Monarch populations. Environmental conservation efforts are underway to protect their milkweed breeding grounds.""",
            "questions": [
                {
                    "id": 1,
                    "type": "multiple_choice",
                    "question": "Where do Monarch butterflies migrate every autumn?",
                    "options": ["Central Mexico", "Northern Canada", "South America", "Africa"],
                    "correct_answer": "Central Mexico",
                    "explanation": "Matnda 'from southern Canada to the oyamel fir forests of central Mexico' deb berilgan."
                }
            ]
        }
    ]
    db.reading_tests.insert_many(reading_tests)

    print("Seeding Listening Tests...")
    db.listening_tests.delete_many({})
    listening_tests = [
        {
            "title": "Section 1: University Student Accommodation Inquiry",
            "section": 1,
            "duration": "10:00",
            "audio_url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3",
            "transcript": "Receptionist: Good morning, Student Housing Office. How can I help you today?\nStudent: Hello! I'd like to ask about available rooms near the main campus for the next semester.",
            "questions": [
                {
                    "id": 1,
                    "type": "multiple_choice",
                    "question": "What is the student inquiring about?",
                    "options": ["Room accommodation", "Library books", "Bus schedule", "Exam results"],
                    "correct_answer": "Room accommodation",
                    "explanation": "Talaba talabalar turar joyi xonalari haqida so'ramoqda."
                }
            ]
        }
    ]
    db.listening_tests.insert_many(listening_tests)

    print("Seeding Writing Prompts...")
    db.writing_prompts.delete_many({})
    writing_prompts = [
        {
            "title": "Task 2: Impact of Technology on Education",
            "task_type": "Task 2",
            "prompt_text": "Some people believe that technology has improved the quality of modern education, while others argue that it causes distractions for students. Discuss both views and give your opinion."
        },
        {
            "title": "Task 1: Global Energy Consumption Chart",
            "task_type": "Task 1",
            "prompt_text": "The chart below shows the total global energy consumption by source between 1990 and 2020. Summarise the information by selecting and reporting the main features, and make comparisons where relevant."
        }
    ]
    db.writing_prompts.insert_many(writing_prompts)

    print("Seeding Speaking Questions...")
    db.speaking_questions.delete_many({})
    speaking_questions = [
        {
            "part": 1,
            "topic": "Hometown & Hometown Changes",
            "question": "Where is your hometown located, and what do you like most about living there?"
        },
        {
            "part": 2,
            "topic": "Describe a Memorable Trip",
            "question": "Describe a memorable trip or travel experience you had recently.",
            "bullet_points": [
                "Where you went and who you were with",
                "What activities you did during the trip",
                "Why this trip was particularly memorable for you"
            ]
        }
    ]
    db.speaking_questions.insert_many(speaking_questions)

    print("Seeding Grammar Lessons...")
    db.grammar_lessons.delete_many({})
    grammar_lessons = [
        {
            "title": "1. English Tenses in IELTS",
            "slug": "tenses",
            "description": "Present Simple, Present Perfect, and Past Simple tenses usage in Writing & Speaking",
            "content_html": "<p>IELTS insholarida va gapirishda zamonlardan to'g'ri foydalanish juda muhim. <strong>Present Perfect</strong> muayyan natija bergan tajribalarni aytishda ishlatiladi.</p>",
            "examples": [
                "Recent studies have shown a dramatic increase in renewable energy adoption.",
                "Historically, education was limited to wealthy social classes."
            ],
            "exercises": [
                {
                    "id": 1,
                    "question": "Many scientists _____ (discover) innovative solutions in recent years.",
                    "options": ["discovered", "have discovered", "will discover"],
                    "correct_answer": "have discovered",
                    "explanation": "'In recent years' birikmasi Present Perfect zamonini talab qiladi."
                }
            ]
        },
        {
            "title": "2. Passive Voice in Academic Writing",
            "slug": "passive",
            "description": "Passive voice structures for Academic Task 1 process diagrams and Task 2 essays",
            "content_html": "<p>Akademik yozuvda sub'ektdan ko'ra harakatning o'zi muhim bo'lganda Passive Voice ishlatiladi.</p>",
            "examples": [
                "The water is heated to 100 degrees Celsius before being filtered."
            ],
            "exercises": [
                {
                    "id": 1,
                    "question": "The data _____ (collect) by researchers last month.",
                    "options": ["was collected", "is collected", "collected"],
                    "correct_answer": "was collected",
                    "explanation": "O'tgan vaqt passive shakli: was + past participle."
                }
            ]
        },
        {
            "title": "3. Conditionals (If Clauses)",
            "slug": "conditionals",
            "description": "First, Second, and Third Conditionals for hypothethical essay arguments",
            "content_html": "<p>Shart ergash gaplar muammoga gipotetik yechimlar taklif etishda ishlatiladi.</p>",
            "examples": [
                "If governments invested more in public transport, traffic congestion would decrease significantly."
            ],
            "exercises": [
                {
                    "id": 1,
                    "question": "If governments _____ (enforce) stricter regulations, pollution levels would fall.",
                    "options": ["enforce", "enforced", "had enforced"],
                    "correct_answer": "enforced",
                    "explanation": "Second conditional tuzilishi: If + Past Simple, would + verb."
                }
            ]
        },
        {
            "title": "4. Relative Clauses (Who, Which, That, Where)",
            "slug": "relative-clauses",
            "description": "Complex sentence construction using relative pronouns",
            "content_html": "<p>Sifat ergash gaplar gaplarni mantiqan bog'lab, <strong>Grammatical Range</strong> ballini oshiradi.</p>",
            "examples": [
                "Individuals who possess high digital literacy are more adaptable in the job market."
            ],
            "exercises": [
                {
                    "id": 1,
                    "question": "Students _____ study regularly achieve higher IELTS bands.",
                    "options": ["which", "who", "where"],
                    "correct_answer": "who",
                    "explanation": "Insonlarga nisbatan 'who' nisbiy olmoshi ishlatiladi."
                }
            ]
        },
        {
            "title": "5. Articles (A, An, The)",
            "slug": "articles",
            "description": "Definite and indefinite articles in formal English",
            "content_html": "<p>Artikllar IELTS yozuvida eng ko'p yo'l qo'yiladigan xatolardan biridir.</p>",
            "examples": ["The internet has revolutionized global communication."],
            "exercises": [
                {
                    "id": 1,
                    "question": "____ Internet has changed modern communication.",
                    "options": ["A", "An", "The"],
                    "correct_answer": "The",
                    "explanation": "Internet so'zi oldidan aniqlik artikli 'The' ishlatiladi."
                }
            ]
        },
        {
            "title": "6. Prepositions of Place and Time",
            "slug": "prepositions",
            "description": "Accurate preposition usage in task descriptions and graphs",
            "content_html": "<p>In, at, on va boshqa predloglar o'rnida ishlatilishi ta'kidlanadi.</p>",
            "examples": ["Sales reached a peak of $5 million in 2020."],
            "exercises": [
                {
                    "id": 1,
                    "question": "The percentage peaked ____ 85% in 2015.",
                    "options": ["at", "in", "on"],
                    "correct_answer": "at",
                    "explanation": "'Peaked at' birikmasi to'g'ri."
                }
            ]
        },
        {
            "title": "7. Linking Words and Cohesive Devices",
            "slug": "linking-words",
            "description": "Coherence & Cohesion transition words (Furthermore, Consequently, On the other hand)",
            "content_html": "<p>Paragraflar o'rtasida mantiqiy bog'lovchi so'zlar Coherence mezonini oshiradi.</p>",
            "examples": ["Furthermore, implementing renewable energy reduces carbon footprints."],
            "exercises": [
                {
                    "id": 1,
                    "question": "_____ the financial risks, the company decided to invest.",
                    "options": ["Despite", "Although", "However"],
                    "correct_answer": "Despite",
                    "explanation": "'Despite' dan keyin ot birikmasi keladi."
                }
            ]
        },
        {
            "title": "8. Complex Sentences & Subordination",
            "slug": "complex-sentences",
            "description": "Building multi-clause complex sentence structures for Band 7+",
            "content_html": "<p>Murakkab gaplar (Complex sentences) qo'llash GRA bo'yicha yuqori ball beradi.</p>",
            "examples": ["Although online learning offers flexibility, face-to-face interaction remains indispensable."],
            "exercises": [
                {
                    "id": 1,
                    "question": "_____ technology brings conveniences, it also creates privacy concerns.",
                    "options": ["Although", "Because", "Despite"],
                    "correct_answer": "Although",
                    "explanation": "Zidlikni ifodalash uchun 'Although' ishlatiladi."
                }
            ]
        }
    ]
    db.grammar_lessons.insert_many(grammar_lessons)

    print("Seeding Vocabulary Words...")
    db.vocabulary_words.delete_many({})
    vocabulary_words = [
        {
            "word": "Meticulous",
            "phonetic": "/məˈtɪkjələs/",
            "topic": "Academic",
            "meaning_uz": "O'ta sinchkov, puxta, qunt bilan qilingan",
            "example": "He conducted a meticulous research into climate change.",
            "synonyms": ["thorough", "precise", "diligent"],
            "collocations": ["meticulous planning", "meticulous attention"]
        },
        {
            "word": "Paramount",
            "phonetic": "/ˈpærəmaʊnt/",
            "topic": "Academic",
            "meaning_uz": "Eng muhim, birinchi darajali",
            "example": "Safety is of paramount importance in industrial design.",
            "synonyms": ["crucial", "vital", "supreme"],
            "collocations": ["paramount importance", "paramount role"]
        },
        {
            "word": "Facilitate",
            "phonetic": "/fəˈsɪlɪteɪt/",
            "topic": "Academic",
            "meaning_uz": "Yengillashtirmoq, yordam bermoq, qulaylashtirmoq",
            "example": "Modern tools facilitate efficient remote communication.",
            "synonyms": ["assist", "enable", "ease"],
            "collocations": ["facilitate learning", "facilitate growth"]
        },
        {
            "word": "Prevalent",
            "phonetic": "/ˈprevələnt/",
            "topic": "Academic",
            "meaning_uz": "Keng tarqalgan, ommalashgan",
            "example": "Remote work has become prevalent across tech industries.",
            "synonyms": ["widespread", "common", "pervasive"],
            "collocations": ["prevalent trend", "prevalent view"]
        },
        {
            "word": "Substantial",
            "phonetic": "/səbˈstænʃl/",
            "topic": "Academic",
            "meaning_uz": "Sezilarli, salmoqli, katta",
            "example": "There has been a substantial increase in public funding.",
            "synonyms": ["significant", "considerable"],
            "collocations": ["substantial increase", "substantial amount"]
        }
    ]
    db.vocabulary_words.insert_many(vocabulary_words)

    print("Seeding Mock Tests...")
    db.mock_tests.delete_many({})
    db.mock_tests.insert_one({
        "title": "IELTS Official Simulation Test #1",
        "description": "Full simulation test encompassing Reading, Listening, Writing, and Speaking",
        "created_at": datetime.utcnow()
    })

    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
