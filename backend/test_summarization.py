from services.summarization import summarize_chunk

sample_chunk = """
Alright team, let's discuss the Q3 roadmap. We need to finalize the new onboarding flow by end of month.
Sarah will own the design mockups, and James will handle the backend API changes.
One open question — we still haven't decided if we're supporting Safari for the initial launch.
We did agree to push the mobile app redesign to Q4 instead of Q3.
"""

result = summarize_chunk(sample_chunk)
print(result)