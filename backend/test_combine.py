from services.summarization import combine_summaries

fake_chunk_summaries = [
    {
        "discussion_points": ["Discussed Q3 roadmap priorities"],
        "decisions": ["Push mobile redesign to Q4"],
        "action_items": ["Sarah owns design mockups"],
        "open_questions": ["Safari support undecided"]
    },
    {
        "discussion_points": ["Reviewed backend API timeline", "Discussed Q3 roadmap priorities again"],
        "decisions": [],
        "action_items": ["James handles backend API changes", "Sarah owns design mockups"],
        "open_questions": []
    }
]

result = combine_summaries(fake_chunk_summaries)
print(result)