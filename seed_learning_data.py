import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brightsteps_admin.settings')
django.setup()

from core.models import Lesson, QuizQuestion

# Clear existing lessons and quizzes
Lesson.objects.all().delete()
QuizQuestion.objects.all().delete()

lessons_data = [
    # --- Marathi Lessons ---
    {
        "id": "78788dfb-b5d1-4171-80a5-f9f60f64c6a1",
        "subject": "Marathi",
        "grade_level": "Jr KG",
        "title_mr": "स्वर ओळख",
        "title_en": "Vowels Recognition",
        "description_mr": "मराठीतील मुळाक्षरे शिका",
        "description_en": "Learn Marathi vowels",
        "content_mr": "अ, आ, इ, ई, उ, ऊ, ए, ऐ, ओ, औ, अं, अः",
        "content_en": "a, aa, i, ee, u, oo, e, ai, o, au, am, ah",
        "icon_res": "abc",
        "color_hex": "#FF8A80"
    },
    {
        "id": "e9ff6b36-7e3e-4fb8-86d7-8e68e4c76b98",
        "subject": "Marathi",
        "grade_level": "Sr KG",
        "title_mr": "व्यंजन ओळख",
        "title_en": "Consonants Recognition",
        "description_mr": "मराठीतील व्यंजने शिका",
        "description_en": "Learn Marathi consonants",
        "content_mr": "क, ख, ग, घ, च, छ, ज, झ, ट, ठ, ड, ढ, ण, त, थ, द, ध, न",
        "content_en": "k, kh, g, gh, ch, chh, j, jh...",
        "icon_res": "abc",
        "color_hex": "#FF8A80"
    },
    {
        "id": "df6f0814-c8c3-4d7a-b2ff-fb9df28a7e30",
        "subject": "Marathi",
        "grade_level": "Class 1",
        "title_mr": "शब्द वाचन",
        "title_en": "Word Reading",
        "description_mr": "सोपे मराठी शब्द वाचा",
        "description_en": "Read simple Marathi words",
        "content_mr": "आई, बाबा, पाणी, दूध, भात",
        "content_en": "Mother, Father, Water, Milk, Rice",
        "icon_res": "book",
        "color_hex": "#FF8A80"
    },
    {
        "id": "c138d8d7-7d48-4cb1-97b0-8e108e404bf2",
        "subject": "Marathi",
        "grade_level": "Class 1",
        "title_mr": "बाराखडी",
        "title_en": "Barakhadi",
        "description_mr": "मराठी बाराखडी शिका",
        "description_en": "Learn Marathi Barakhadi",
        "content_mr": "का, कि, की, कु, कू, के, कै, को, कौ, कं, क:",
        "content_en": "ka, ki, kee, ku, koo...",
        "icon_res": "grid",
        "color_hex": "#FF8A80"
    },
    # --- English Lessons ---
    {
        "id": "e0b1d3d6-444f-4d3f-b3a6-b5ce9db29ba5",
        "subject": "English",
        "grade_level": "Jr KG",
        "title_mr": "अक्षरे ओळख",
        "title_en": "Alphabet Recognition",
        "description_mr": "इंग्रजी अक्षरे शिका",
        "description_en": "Learn English alphabet letters",
        "content_mr": "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z",
        "content_en": "A B C D E F G H I J K L M N O P Q R S T U V W X Y Z",
        "icon_res": "abc",
        "color_hex": "#81D4FA"
    },
    {
        "id": "8bb3d3d6-444f-4d3f-b3a6-b5ce9db29ba6",
        "subject": "English",
        "grade_level": "Class 1",
        "title_mr": "साधे शब्द",
        "title_en": "Simple Words",
        "description_mr": "तीन अक्षरी शब्द शिका",
        "description_en": "Learn three-letter words",
        "content_mr": "Cat, Dog, Bat, Hat, Rat, Mat, Sun, Run",
        "content_en": "Cat, Dog, Bat, Hat, Rat, Mat, Sun, Run",
        "icon_res": "spell",
        "color_hex": "#81D4FA"
    },
    {
        "id": "9cc3d3d6-444f-4d3f-b3a6-b5ce9db29ba7",
        "subject": "English",
        "grade_level": "Sr KG",
        "title_mr": "रंगांची नावे",
        "title_en": "Color Names",
        "description_mr": "इंग्रजीत रंगांची नावे शिका",
        "description_en": "Learn color names in English",
        "content_mr": "Red, Blue, Green, Yellow, Pink, Black, White",
        "content_en": "Red, Blue, Green, Yellow, Pink, Black, White",
        "icon_res": "palette",
        "color_hex": "#81D4FA"
    },
    # --- Mathematics Lessons ---
    {
        "id": "ad11a141-8bc6-4bdf-87db-2ee94a11dbf1",
        "subject": "Mathematics",
        "grade_level": "Jr KG",
        "title_mr": "अंक ओळख",
        "title_en": "Number Recognition",
        "description_mr": "१ ते १० अंक शिका",
        "description_en": "Learn numbers 1 to 10",
        "content_mr": "1 2 3 4 5 6 7 8 9 10",
        "content_en": "1 2 3 4 5 6 7 8 9 10",
        "icon_res": "123",
        "color_hex": "#A5D6A7"
    },
    {
        "id": "bd11a141-8bc6-4bdf-87db-2ee94a11dbf2",
        "subject": "Mathematics",
        "grade_level": "Class 1",
        "title_mr": "बेरीज",
        "title_en": "Addition",
        "description_mr": "सोपी बेरीज शिका",
        "description_en": "Learn simple addition",
        "content_mr": "1+1=2, 2+2=4, 3+3=6, 4+4=8",
        "content_en": "1+1=2, 2+2=4, 3+3=6, 4+4=8",
        "icon_res": "plus",
        "color_hex": "#A5D6A7"
    },
    {
        "id": "cd11a141-8bc6-4bdf-87db-2ee94a11dbf3",
        "subject": "Mathematics",
        "grade_level": "Class 1",
        "title_mr": "वजाबाकी",
        "title_en": "Subtraction",
        "description_mr": "सोपी वजाबाकी शिका",
        "description_en": "Learn simple subtraction",
        "content_mr": "2-1=1, 3-1=2, 4-2=2, 5-3=2",
        "content_en": "2-1=1, 3-1=2, 4-2=2, 5-3=2",
        "icon_res": "minus",
        "color_hex": "#A5D6A7"
    },
    {
        "id": "dd11a141-8bc6-4bdf-87db-2ee94a11dbf4",
        "subject": "Mathematics",
        "grade_level": "Sr KG",
        "title_mr": "मोजणी",
        "title_en": "Counting",
        "description_mr": "वस्तू मोजायला शिका",
        "description_en": "Learn to count objects",
        "content_mr": "🐱🐱 = 2, 🐱🐱🐱 = 3, 🌟🌟🌟🌟 = 4",
        "content_en": "🐱🐱 = 2, 🐱🐱🐱 = 3, 🌟🌟🌟🌟 = 4",
        "icon_res": "count",
        "color_hex": "#A5D6A7"
    },
    # --- Rhymes ---
    {
        "id": "f5a0a3d6-444f-4d3f-b3a6-b5ce9db29ba8",
        "subject": "Rhymes",
        "grade_level": "Jr KG",
        "title_mr": "निजरे मुग्याचे",
        "title_en": "Nijare Mugyache",
        "description_mr": "लोकप्रिय मराठी बालगीत",
        "description_en": "Popular Marathi rhyme for kids",
        "content_mr": "निजरे मुग्याचे गोड गोड बोल...",
        "content_en": "Nijare mugyache god god bol...",
        "icon_res": "music",
        "color_hex": "#FFD54F"
    },
    {
        "id": "f6a0a3d6-444f-4d3f-b3a6-b5ce9db29ba9",
        "subject": "Rhymes",
        "grade_level": "Sr KG",
        "title_mr": "एक होता राजा",
        "title_en": "Ek Hota Raja",
        "description_mr": "मजेदार मराठी कविता",
        "description_en": "Fun Marathi poem",
        "content_mr": "एक होता राजा, एक होती राणी...",
        "content_en": "Ek hota raja, ek hoti rani...",
        "icon_res": "music",
        "color_hex": "#FFD54F"
    },
    {
        "id": "f7a0a3d6-444f-4d3f-b3a6-b5ce9db29ba0",
        "subject": "Rhymes",
        "grade_level": "Jr KG",
        "title_mr": "Twinkle Twinkle",
        "title_en": "Twinkle Twinkle Little Star",
        "description_mr": "इंग्रजी बालगीत",
        "description_en": "Popular English nursery rhyme",
        "content_mr": "Twinkle twinkle little star, how I wonder what you are...",
        "content_en": "Twinkle twinkle little star...",
        "icon_res": "music",
        "color_hex": "#FFD54F"
    },
    # --- Stories ---
    {
        "id": "e5b0a3d6-444f-4d3f-b3a6-b5ce9db29ba1",
        "subject": "Stories",
        "grade_level": "Class 1",
        "title_mr": "आजोबांची गोष्ट",
        "title_en": "Grandpa's Story",
        "description_mr": "गावातील मजेदार गोष्ट",
        "description_en": "A fun story from the village",
        "content_mr": "एक होता शेतकरी. त्याच्या शेतात एक मोठा वृक्ष होता...",
        "content_en": "There was a farmer. He had a big tree in his farm...",
        "icon_res": "book",
        "color_hex": "#CE93D8"
    },
    {
        "id": "e6b0a3d6-444f-4d3f-b3a6-b5ce9db29ba2",
        "subject": "Stories",
        "grade_level": "Sr KG",
        "title_mr": "बुद्धिमान कासव",
        "title_en": "The Clever Tortoise",
        "description_mr": "हुशार कासवाची गोष्ट",
        "description_en": "Story of a clever tortoise",
        "content_mr": "एकदा एक कासव आणि ससा यांच्यात शर्यत झाली...",
        "content_en": "Once a tortoise and a hare had a race...",
        "icon_res": "book",
        "color_hex": "#CE93D8"
    },
    {
        "id": "e7b0a3d6-444f-4d3f-b3a6-b5ce9db29ba3",
        "subject": "Stories",
        "grade_level": "Jr KG",
        "title_mr": "The Lion and the Mouse",
        "title_en": "सिंह आणि उंदीर",
        "description_mr": "इंग्रजी गोष्ट",
        "description_en": "English story",
        "content_mr": "A lion caught a little mouse...",
        "content_en": "A lion caught a little mouse...",
        "icon_res": "book",
        "color_hex": "#CE93D8"
    },
    # --- Videos ---
    {
        "id": "d5b0a3d6-444f-4d3f-b3a6-b5ce9db29ba1",
        "subject": "Videos",
        "grade_level": "Jr KG",
        "title_mr": "अक्षर गीत",
        "title_en": "Alphabet Song",
        "description_mr": "मजेदार अक्षर गीत",
        "description_en": "Fun alphabet song video",
        "content_mr": "https://www.youtube.com/watch?v=some_vid1",
        "content_en": "https://www.youtube.com/watch?v=some_vid1",
        "icon_res": "play",
        "color_hex": "#9FA8DA"
    },
    {
        "id": "d6b0a3d6-444f-4d3f-b3a6-b5ce9db29ba2",
        "subject": "Videos",
        "grade_level": "Sr KG",
        "title_mr": "मोजणी गीत",
        "title_en": "Counting Song",
        "description_mr": "१ ते १० मोजणी गीत",
        "description_en": "Counting 1 to 10 song",
        "content_mr": "https://www.youtube.com/watch?v=some_vid2",
        "content_en": "https://www.youtube.com/watch?v=some_vid2",
        "icon_res": "play",
        "color_hex": "#9FA8DA"
    },
    {
        "id": "d7b0a3d6-444f-4d3f-b3a6-b5ce9db29ba3",
        "subject": "Videos",
        "grade_level": "Jr KG",
        "title_mr": "रंग ओळख",
        "title_en": "Color Recognition",
        "description_mr": "रंग शिकण्यासाठी व्हिडिओ",
        "description_en": "Colors learning video",
        "content_mr": "https://www.youtube.com/watch?v=some_vid3",
        "content_en": "https://www.youtube.com/watch?v=some_vid3",
        "icon_res": "play",
        "color_hex": "#9FA8DA"
    }
]

quizzes_data = [
    {
        "id": "5f1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d",
        "subject": "Mathematics",
        "grade_level": "Jr KG",
        "question_mr": "१+१ किती?",
        "question_en": "What is 1+1?",
        "option_1_en": "1", "option_2_en": "2", "option_3_en": "3", "option_4_en": "4",
        "option_1_mr": "१", "option_2_mr": "२", "option_3_mr": "३", "option_4_mr": "४",
        "correct_answer_index": 1,
        "points": 10
    },
    {
        "id": "6f1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d",
        "subject": "English",
        "grade_level": "Jr KG",
        "question_mr": "आकाशाचा रंग कोणता?",
        "question_en": "What color is the sky?",
        "option_1_en": "Red", "option_2_en": "Blue", "option_3_en": "Green", "option_4_en": "Yellow",
        "option_1_mr": "लाल", "option_2_mr": "निळा", "option_3_mr": "हिरवा", "option_4_mr": "पिवळा",
        "correct_answer_index": 1,
        "points": 10
    },
    {
        "id": "7f1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d",
        "subject": "Marathi",
        "grade_level": "Sr KG",
        "question_mr": "मांजर कोणता प्राणी?",
        "question_en": "Which animal is a cat?",
        "option_1_en": "Bird", "option_2_en": "Fish", "option_3_en": "Mammal", "option_4_en": "Reptile",
        "option_1_mr": "पक्षी", "option_2_mr": "मासा", "option_3_mr": "सस्तन", "option_4_mr": "सरपटणारा",
        "correct_answer_index": 2,
        "points": 10
    },
    {
        "id": "8f1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d",
        "subject": "Mathematics",
        "grade_level": "Jr KG",
        "question_mr": "वर्तुळाचा आकार?",
        "question_en": "Shape of a circle?",
        "option_1_en": "Square (⬛)", "option_2_en": "Circle (🟡)", "option_3_en": "Triangle (🔺)", "option_4_en": "Star (⭐)",
        "option_1_mr": "⬛", "option_2_mr": "🟡", "option_3_mr": "🔺", "option_4_mr": "⭐",
        "correct_answer_index": 1,
        "points": 10
    },
    {
        "id": "9f1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d",
        "subject": "Mathematics",
        "grade_level": "Sr KG",
        "question_mr": "७ नंतर कोणती संख्या?",
        "question_en": "Which number comes after 7?",
        "option_1_en": "5", "option_2_en": "6", "option_3_en": "8", "option_4_en": "9",
        "option_1_mr": "५", "option_2_mr": "६", "option_3_mr": "८", "option_4_mr": "९",
        "correct_answer_index": 2,
        "points": 10
    }
]

for l in lessons_data:
    Lesson.objects.create(**l)

for q in quizzes_data:
    QuizQuestion.objects.create(**q)

# Ensure default admin superuser (admin / admin123) exists
from django.contrib.auth.models import User
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@brightsteps.online', 'admin123')
    print("Created superuser admin with password admin123")
else:
    u = User.objects.get(username='admin')
    u.set_password('admin123')
    u.is_superuser = True
    u.is_staff = True
    u.save()
    print("Updated superuser admin password to admin123")

print("Learning and Quiz data seeded successfully with grade levels!")
