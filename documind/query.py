def extract_answer(context, question):
    import re
    q = question.lower()

    # ---- Joining Date ----
    if "joining" in q or "date" in q:
        match = re.search(r'\b\d{1,2}[-/]\d{1,2}[-/]\d{2,4}\b', context)
        if match:
            return match.group(0)

    # ---- Salary / Stipend ----
    if "salary" in q or "stipend" in q:
        match = re.search(r'₹\s?\d{1,3}(?:,\d{3})*(?:\s?per\s?month)?', context, re.IGNORECASE)
        if match:
            return match.group(0)

    # ---- Company / Issued by ----
    if "who issued" in q or "company" in q or "issued" in q:
        match = re.search(r'Infotact\s+Solutions', context, re.IGNORECASE)
        if match:
            return match.group(0)

    # ---- Fallback (short answer only) ----
    sentences = context.split(".")
    return sentences[0][:200]