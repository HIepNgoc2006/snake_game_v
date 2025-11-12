import json
import os
from datetime import datetime


class Leaderboard:
    def __init__(self, leaderboard_file="Scores/leaderboard.json"):
        self.leaderboard_file = leaderboard_file
        self.scores = self.load_scores()
        self.max_entries = 10

    def load_scores(self):
        """Load leaderboard from file"""
        try:
            if os.path.exists(self.leaderboard_file):
                with open(self.leaderboard_file, 'r') as f:
                    return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            pass
        return []

    def save_scores(self):
        """Save leaderboard to file"""
        os.makedirs(os.path.dirname(self.leaderboard_file), exist_ok=True)
        with open(self.leaderboard_file, 'w') as f:
            json.dump(self.scores, f, indent=2)

    def add_score(self, score, difficulty, gamemode):
        """Add a new score and keep only top 10"""
        entry = {
            "score": score,
            "difficulty": difficulty.name,
            "gamemode": gamemode.value,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.scores.append(entry)
        # Sort by score descending
        self.scores.sort(key=lambda x: x["score"], reverse=True)
        # Keep only top 10
        self.scores = self.scores[:self.max_entries]
        self.save_scores()

    def get_top_scores(self, limit=10):
        """Get top scores"""
        return self.scores[:limit]

    def is_high_score(self, score):
        """Check if score qualifies for leaderboard"""
        if len(self.scores) < self.max_entries:
            return True
        return score > self.scores[-1]["score"]

    def get_rank(self, score):
        """Get rank of a score if it's in leaderboard"""
        for i, entry in enumerate(self.scores):
            if entry["score"] == score:
                return i + 1
        return None
