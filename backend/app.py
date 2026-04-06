from flask import Flask, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# ---------------- DATA ----------------
events_data = {
    "Event Name": [
        "AI Innovations Summit","Artificial Intelligence Workshop","Deep Learning Bootcamp",
        "AI Ethics Conference","Neural Networks Masterclass","Generative AI Hackathon",
        "Machine Learning Fundamentals","ML Model Deployment Workshop","Supervised Learning Deep Dive",
        "Reinforcement Learning Seminar","Applied ML for Engineers",
        "Data Science Bootcamp","Data Analytics & Visualization","Big Data Processing Workshop",
        "Python for Data Science","Statistics for Data Scientists","Data Engineering Summit",
        "React.js Advanced Workshop","Full Stack Development Bootcamp","Node.js and Express Masterclass",
        "Modern CSS & UI Design","Web Performance Optimization","JavaScript ES2024 Features",
        "Ethical Hacking Workshop","Cyber Security Fundamentals","Network Security Masterclass",
        "Penetration Testing Bootcamp","Cloud Security Summit","CTF Competition"
    ],
    "Category": [
        "AI","AI","AI","AI","AI","AI",
        "Machine Learning","Machine Learning","Machine Learning","Machine Learning","Machine Learning",
        "Data Science","Data Science","Data Science","Data Science","Data Science","Data Science",
        "Web Development","Web Development","Web Development","Web Development","Web Development","Web Development",
        "Cyber Security","Cyber Security","Cyber Security","Cyber Security","Cyber Security","Cyber Security"
    ],
    "Tags": [
        "artificial intelligence machine learning deep learning neural networks automation",
        "artificial intelligence python automation robotics nlp transformers",
        "deep learning neural networks tensorflow pytorch gpu training",
        "artificial intelligence ethics policy fairness responsible ai",
        "neural networks deep learning backpropagation perceptron layers",
        "generative ai llm gpt diffusion models creative ai prompting",
        "machine learning algorithms supervised unsupervised scikit-learn python",
        "machine learning mlops deployment docker kubernetes flask api",
        "supervised learning regression classification decision trees random forest",
        "reinforcement learning agents rewards policy q-learning openai gym",
        "machine learning applied engineering production pipelines feature engineering",
        "data science python pandas numpy analysis statistics visualization",
        "data analytics tableau powerbi visualization dashboard insights",
        "big data spark hadoop distributed computing processing pipeline",
        "python data science jupyter numpy matplotlib seaborn",
        "statistics probability hypothesis testing regression analysis r",
        "data engineering etl pipeline sql databases warehousing airflow",
        "react javascript frontend components hooks state management redux",
        "full stack web development node react mongodb express javascript",
        "node express backend api rest javascript server npm",
        "css html ui design responsive animations flexbox grid",
        "web performance optimization lighthouse caching cdn lazy loading",
        "javascript es6 async promises modules browser web apis",
        "ethical hacking penetration testing kali linux vulnerabilities exploits",
        "cyber security network firewalls threats defense awareness",
        "network security protocols encryption vpn firewall intrusion detection",
        "penetration testing tools burpsuite metasploit vulnerability assessment",
        "cloud security aws azure devSecOps iam zero trust",
        "ctf challenges hacking puzzles reverse engineering forensics",
    ]
}

df = pd.DataFrame(events_data)
df["Features"] = df["Category"].str.lower() + " " + df["Tags"]

vectorizer = CountVectorizer(stop_words="english")
count_matrix = vectorizer.fit_transform(df["Features"])
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# ---------------- MODEL ----------------
def recommend_events(user_input, top_n=5):
    user_vec = vectorizer.transform([user_input.lower()])
    sim_scores = cosine_similarity(user_vec, count_matrix)[0]
    top_indices = sim_scores.argsort()[::-1][:top_n]

    results = df.iloc[top_indices][["Event Name", "Category"]].copy()
    results["Similarity Score"] = [round(sim_scores[i], 2) for i in top_indices]

    return results

# ---------------- API ----------------
@app.route("/recommend", methods=["POST"])
def recommend():
    data = request.json
    user_input = data.get("input")

    results = recommend_events(user_input)

    return jsonify(results.to_dict(orient="records"))
@app.route("/")
def home():
    return "EventHive Backend Running 🚀"

if __name__ == "__main__":
    app.run(debug=True)