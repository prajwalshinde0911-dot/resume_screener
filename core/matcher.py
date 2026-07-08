from sentence_transformers import SentenceTransformer, util

# Load model once (this may take a few seconds the first time)
model = SentenceTransformer('all-MiniLM-L6-v2')

def compute_similarity(jd_text, resume_text):
    """Compute semantic similarity score (0-100) between JD and resume."""
    embeddings = model.encode([jd_text, resume_text], convert_to_tensor=True)
    similarity = util.cos_sim(embeddings[0], embeddings[1]).item()
    # Convert from -1..1 range to a 0-100 score
    score = round((similarity + 1) / 2 * 100, 2)
    return score