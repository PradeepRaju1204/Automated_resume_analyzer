from analyzer.skills import skills


def get_missing_skills(found_skills):

    missing = []

    for skill in skills:

        if skill not in found_skills:
            missing.append(skill)

    return missing[:10]