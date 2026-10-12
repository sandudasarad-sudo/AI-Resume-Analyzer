from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

ROLE_DESCRIPTIONS = {
    "Python Developer": (
        "Python programming, Django, Flask, SQL, "
        "Pandas, NumPy, REST API development"
    ),
    "Web Developer": (
        "HTML, CSS, JavaScript, React, website development, "
        "frontend development, responsive design"
    ),
    "Machine Learning Intern": (
        "Python, machine learning, data science, "
        "scikit-learn, Pandas, NumPy, model evaluation"
    ),
    "Flutter Developer": (
        "Flutter, Dart, mobile application development, "
        "Firebase, REST APIs"
    ),
    "Full Stack Developer": (
        "HTML, CSS, JavaScript, React, Node.js, "
        "Express, MongoDB, backend and frontend development"
    )
}


def compare_resume_to_roles(resume_text):
    role_names = list(ROLE_DESCRIPTIONS.keys())

    documents = [
        resume_text,
        *[ROLE_DESCRIPTIONS[role] for role in role_names]
    ]

    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2)
    )

    vectors = vectorizer.fit_transform(documents)

    similarities = cosine_similarity(
        vectors[0:1],
        vectors[1:]
    )[0]

    results = []

    for role, score in zip(role_names, similarities):
        results.append({
            "Job Role": role,
            "Text Similarity (%)": round(float(score) * 100, 2)
        })

    results.sort(
        key=lambda item: item["Text Similarity (%)"],
        reverse=True
    )

    return results