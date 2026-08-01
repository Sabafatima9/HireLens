"""
ats_scorer.py
Two scoring modes:
  1. score_against_jd()  -> compares CV text to a pasted Job Description
  2. score_general()     -> checklist-based CV health score (no JD needed)
"""

import re


STOPWORDS = {
    "the", "a", "an", "and", "or", "of", "to", "in", "on", "for", "with",
    "is", "are", "was", "were", "be", "been", "as", "at", "by", "this",
    "that", "it", "from", "will", "you", "your", "we", "our", "i", "he",
    "she", "they", "them", "his", "her", "their", "us", "have", "has",
    "had", "do", "does", "did", "not", "but", "if", "so", "than", "then",
    "into", "about", "such", "can", "could", "would", "should", "must",
    "all", "any", "some", "no", "yes", "etc", "per", "via",
}

SECTION_PATTERNS = {
    "Contact Info": re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}"),
    "Skills": re.compile(r"\bskills?\b", re.IGNORECASE),
    "Experience": re.compile(r"\b(experience|employment|work history)\b", re.IGNORECASE),
    "Education": re.compile(r"\beducation\b", re.IGNORECASE),
    "Summary/Objective": re.compile(r"\b(summary|objective|profile)\b", re.IGNORECASE),
}

ACTION_VERBS = {
    "managed", "led", "developed", "created", "designed", "built", "improved",
    "increased", "reduced", "achieved", "implemented", "coordinated",
    "organized", "analyzed", "researched", "trained", "supervised", "launched",
}


def _tokenize(text):
    words = re.findall(r"[a-zA-Z][a-zA-Z\-]{2,}", text.lower())
    return [w for w in words if w not in STOPWORDS]


def _keyword_set(text, top_n=40):
    """Pulls the most frequent meaningful words out of a text block."""
    words = _tokenize(text)
    freq = {}
    for w in words:
        freq[w] = freq.get(w, 0) + 1
    ranked = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return set(w for w, _ in ranked[:top_n])


def score_against_jd(cv_text, jd_text):
    """
    Returns a dict:
      score: 0-100
      matched: list of matched keywords
      missing: list of important JD keywords not found in the CV
    """
    jd_keywords = _keyword_set(jd_text, top_n=40)
    cv_words = set(_tokenize(cv_text))

    if not jd_keywords:
        return {"score": 0, "matched": [], "missing": [], "total_keywords": 0}

    matched = sorted(jd_keywords & cv_words)
    missing = sorted(jd_keywords - cv_words)

    score = round((len(matched) / len(jd_keywords)) * 100)

    return {
        "score": score,
        "matched": matched,
        "missing": missing,
        "total_keywords": len(jd_keywords),
    }


def score_general(cv_text):
    """
    Checklist-based health score, no JD required.
    Returns dict: score (0-100) and details (list of (label, passed:bool, note))
    """
    details = []
    points = 0
    max_points = 0

    # 1. Section presence (15 pts each, 5 sections = 75 pts)
    for label, pattern in SECTION_PATTERNS.items():
        max_points += 15
        found = bool(pattern.search(cv_text))
        if found:
            points += 15
        details.append((f"{label} section found", found, ""))

    # 2. Reasonable length (10 pts) - not too short, not a wall of text
    max_points += 10
    word_count = len(cv_text.split())
    length_ok = 150 <= word_count <= 1200
    if length_ok:
        points += 10
    details.append((
        "Reasonable length",
        length_ok,
        f"{word_count} words (ideal range: 150-1200)"
    ))

    # 3. Action verbs used (10 pts)
    max_points += 10
    cv_words = set(_tokenize(cv_text))
    verbs_found = ACTION_VERBS & cv_words
    verbs_ok = len(verbs_found) >= 3
    if verbs_ok:
        points += 10
    details.append((
        "Uses strong action verbs",
        verbs_ok,
        f"Found: {', '.join(sorted(verbs_found)) if verbs_found else 'none'}"
    ))

    # 4. No obvious parsing hazards - basic tables/graphics heuristic isn't
    #    reliably detectable from extracted text, so we check for excessive
    #    special characters instead, which often signals a broken text layout.
    max_points += 5
    special_char_ratio = len(re.findall(r"[^\w\s.,\-@]", cv_text)) / max(len(cv_text), 1)
    clean_layout = special_char_ratio < 0.03
    if clean_layout:
        points += 5
    details.append((
        "Clean, parseable layout",
        clean_layout,
        "High symbol density can confuse real ATS parsers" if not clean_layout else ""
    ))

    score = round((points / max_points) * 100) if max_points else 0
    return {"score": score, "details": details}
