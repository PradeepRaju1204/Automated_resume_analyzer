from analyzer.skills import skills


def calculate_score(resume_text, job_role):

    resume_text = resume_text.lower()

    matched_skills = []

    for skill in skills:

        if skill.lower() in resume_text:

            matched_skills.append(skill)

    score = len(matched_skills) * 4

    if score > 100:
        score = 100

    return score, matched_skills