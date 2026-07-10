"""
curriculum.py
Static data describing the full Kindergarten -> Postgraduate curriculum tree,
used to drive the cascading dropdowns in app.py.
"""

LEVELS = [
    "Kindergarten",
    "Class 1", "Class 2", "Class 3", "Class 4", "Class 5",
    "Class 6", "Class 7", "Class 8", "Class 9", "Class 10",
    "Intermediate (11th & 12th)",
    "Undergraduate (UG)",
    "Postgraduate (PG)",
]

SCHOOL_LEVELS = {f"Class {i}" for i in range(1, 11)}

KG_SUBJECTS = [
    "English", "Telugu", "Hindi", "Numbers", "Shapes", "Colors",
    "Rhymes", "General Knowledge", "Drawing", "Moral Stories",
]

# Classes 1-10: grouped in the spec, flattened here (order preserved) for a single dropdown
SCHOOL_SUBJECTS = [
    "English", "Telugu", "Hindi",                       # Languages
    "Mathematics", "Physics", "Chemistry", "Biology",     # STEM
    "Social Studies", "Geography", "History", "Civics",   # Social
    "Computer Science", "General Knowledge",              # Others
]

INTER_STREAMS = ["MPC", "BiPC", "MEC", "CEC", "HEC"]

INTER_SUBJECTS = {
    "MPC": ["Mathematics", "Physics", "Chemistry", "English", "Sanskrit"],
    "BiPC": ["Biology", "Botany", "Zoology", "Physics", "Chemistry", "English"],
    "MEC": ["Mathematics", "Economics", "Commerce", "English"],
    "CEC": ["Civics", "Economics", "Commerce", "English"],
    "HEC": ["History", "Economics", "Civics", "English"],
}

UG_DEGREES = ["B.Tech", "B.E.", "B.Sc.", "B.Com.", "BBA", "BA"]

UG_BTECH_BRANCHES = [
    "CSE", "AI & ML", "AI & DS", "Data Science", "ECE", "EEE",
    "Mechanical", "Civil", "IoT", "Cyber Security",
]

UG_BTECH_SUBJECTS = {
    "CSE": [
        "Programming in C", "Python", "Java", "Data Structures", "Algorithms",
        "Operating Systems", "DBMS", "Computer Networks", "Software Engineering",
        "Machine Learning", "Artificial Intelligence", "Cloud Computing", "Web Development",
    ],
    "AI & ML": ["Python", "Machine Learning", "Deep Learning", "NLP", "Computer Vision", "Data Mining"],
    "AI & DS": ["Python", "Statistics for AI", "Machine Learning", "Data Visualization", "Big Data Systems", "Deep Learning"],
    "Data Science": ["Python", "Statistics", "Data Wrangling", "Machine Learning", "Data Visualization", "Big Data Technologies"],
    "ECE": ["Electronic Devices", "Analog Circuits", "Digital Electronics", "Signals", "Communication Systems", "Embedded Systems", "Microprocessors"],
    "EEE": ["Electrical Machines", "Power Systems", "Control Systems", "Power Electronics"],
    "Mechanical": ["Thermodynamics", "Manufacturing", "Fluid Mechanics", "CAD"],
    "Civil": ["Surveying", "Structural Engineering", "RCC", "Transportation"],
    "IoT": ["Sensors", "Embedded Systems", "Networking", "IoT Architecture", "Cloud IoT"],
    "Cyber Security": ["Network Security", "Cryptography", "Ethical Hacking", "Cyber Forensics", "Security Operations", "Cloud Security"],
}

UG_BSC_SPECIALIZATIONS = ["Computer Science", "Mathematics", "Physics", "Chemistry", "Statistics", "Zoology", "Botany"]

UG_BSC_SUBJECTS = {
    "Computer Science": ["Programming Fundamentals", "Data Structures", "DBMS", "Operating Systems", "Computer Networks", "Web Technologies"],
    "Mathematics": ["Calculus", "Algebra", "Linear Algebra", "Differential Equations", "Probability & Statistics", "Real Analysis"],
    "Physics": ["Mechanics", "Electromagnetism", "Thermodynamics", "Optics", "Modern Physics", "Quantum Mechanics"],
    "Chemistry": ["Organic Chemistry", "Inorganic Chemistry", "Physical Chemistry", "Analytical Chemistry"],
    "Statistics": ["Probability Theory", "Statistical Inference", "Sampling Methods", "Regression Analysis", "Applied Statistics"],
    "Zoology": ["Animal Diversity", "Cell Biology", "Genetics", "Physiology", "Ecology"],
    "Botany": ["Plant Diversity", "Plant Physiology", "Genetics", "Ecology", "Plant Taxonomy"],
}

UG_BCOM_SUBJECTS = ["Accounting", "Taxation", "Economics", "Banking", "Finance", "Business Law"]
UG_BBA_SUBJECTS = ["Marketing", "HR", "Finance", "Management", "Entrepreneurship"]

UG_BA_SPECIALIZATIONS = ["History", "Economics", "Political Science", "English", "Psychology", "Journalism"]

UG_BA_SUBJECTS = {
    "History": ["Ancient History", "Medieval History", "Modern History", "World History"],
    "Economics": ["Microeconomics", "Macroeconomics", "Indian Economy", "Development Economics"],
    "Political Science": ["Political Theory", "Indian Government & Politics", "International Relations", "Public Administration"],
    "English": ["English Literature", "Poetry", "Prose", "Grammar & Composition"],
    "Psychology": ["General Psychology", "Developmental Psychology", "Social Psychology", "Abnormal Psychology"],
    "Journalism": ["Reporting", "Editing", "Media Ethics", "Mass Communication"],
}

PG_DEGREES = ["M.Tech", "MBA", "MCA", "M.Sc.", "MA", "M.Com."]

PG_MTECH_SPECIALIZATIONS = ["CSE", "AI", "Data Science", "ECE", "EEE", "Mechanical", "Civil"]

PG_MTECH_SUBJECTS = {
    "CSE": ["Advanced Algorithms", "Distributed Systems", "Advanced DBMS", "Cloud Computing", "Advanced Operating Systems"],
    "AI": ["Advanced Machine Learning", "Deep Learning", "Reinforcement Learning", "NLP", "Computer Vision", "AI Ethics"],
    "Data Science": ["Big Data Analytics", "Advanced Statistics", "Data Mining", "Predictive Modeling", "Data Engineering"],
    "ECE": ["Advanced Digital Signal Processing", "VLSI Design", "Wireless Communication", "Embedded Systems Design"],
    "EEE": ["Advanced Power Systems", "Smart Grids", "Advanced Control Systems", "Power Electronics Design"],
    "Mechanical": ["Advanced Thermodynamics", "Finite Element Analysis", "Robotics", "Advanced Manufacturing"],
    "Civil": ["Advanced Structural Analysis", "Earthquake Engineering", "Geotechnical Engineering", "Construction Management"],
}

PG_MBA_SPECIALIZATIONS = ["Finance", "HR", "Marketing", "Operations", "Business Analytics"]

PG_MBA_SUBJECTS = [
    "Organizational Behaviour", "Marketing Management", "HR Management",
    "Financial Management", "Strategic Management", "Business Analytics",
]

PG_MCA_SUBJECTS = ["Advanced Java", "Python", "AI", "Machine Learning", "DBMS", "Cloud Computing", "Cyber Security"]

PG_MSC_SPECIALIZATIONS = ["Computer Science", "Physics", "Chemistry", "Mathematics", "Statistics", "Botany", "Zoology"]

PG_MSC_SUBJECTS = {
    "Computer Science": ["Advanced Algorithms", "Advanced DBMS", "Machine Learning", "Distributed Computing"],
    "Physics": ["Quantum Mechanics", "Statistical Mechanics", "Electrodynamics", "Nuclear Physics"],
    "Chemistry": ["Advanced Organic Chemistry", "Advanced Inorganic Chemistry", "Spectroscopy", "Physical Chemistry"],
    "Mathematics": ["Abstract Algebra", "Real & Complex Analysis", "Topology", "Numerical Methods"],
    "Statistics": ["Advanced Statistical Inference", "Multivariate Analysis", "Time Series Analysis", "Bayesian Statistics"],
    "Botany": ["Plant Biotechnology", "Advanced Plant Physiology", "Molecular Biology of Plants"],
    "Zoology": ["Advanced Genetics", "Molecular Biology", "Animal Physiology", "Wildlife Biology"],
}

PG_MA_SPECIALIZATIONS = ["History", "Economics", "Political Science", "English", "Psychology", "Journalism"]

PG_MA_SUBJECTS = {
    "History": ["Historiography", "Advanced Ancient History", "Advanced Modern History"],
    "Economics": ["Advanced Microeconomics", "Advanced Macroeconomics", "Econometrics"],
    "Political Science": ["Advanced Political Theory", "Comparative Politics", "Public Policy"],
    "English": ["Literary Criticism", "Advanced English Literature", "Linguistics"],
    "Psychology": ["Advanced Cognitive Psychology", "Clinical Psychology", "Research Methodology"],
    "Journalism": ["Advanced Media Studies", "Digital Journalism", "Media Law & Ethics"],
}

PG_MCOM_SUBJECTS = [
    "Advanced Accounting", "Corporate Finance", "Advanced Taxation",
    "Financial Markets", "Business Research Methods",
]

# Activities available to every learner
ACTIVITIES_BASE = [
    "Explain Topic",
    "Real-Life Example",
    "Generate Notes",
    "Generate Summary",
    "Generate MCQs",
    "Generate Quiz",
    "Practice Questions",
    "Assignment Questions",
    "Study Plan",
]

# Activities that make sense mainly for older / exam-focused learners
ACTIVITIES_EXAM = ["Generate 10-Mark Answer", "Generate 5-Mark Answer", "Previous Exam Tips"]

# Activities restricted to UG & PG
ACTIVITIES_UG_PG_ONLY = ["Interview Questions (UG & PG)"]

# Only offered when the subject looks programming-related
CODING_ACTIVITY = "Coding Problem (for programming subjects)"

PROGRAMMING_KEYWORDS = [
    "programming", "python", "java", "c", "data structures", "algorithms",
    "dbms", "database", "sql", "software", "web development", "coding",
    "computer science", "machine learning", "artificial intelligence",
    "cloud computing", "cyber security", "networks",
]
