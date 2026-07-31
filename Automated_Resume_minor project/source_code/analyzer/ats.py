def ats_score(score):

    if score >= 80:
        return "Excellent ATS Score"

    elif score >= 60:
        return "Good ATS Score"

    elif score >= 40:
        return "Average ATS Score"

    else:
        return "Poor ATS Score"