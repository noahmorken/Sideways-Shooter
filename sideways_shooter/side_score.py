import json

filename = 'side_high_score.json'

class HighestScore:
    """Tracks the highest score attained in Side Attack."""

    def __init__(self):
        """Nothing to do."""
        pass

    def load_score(self):
        # Retrieves the highest recorded score unless there is none.
        try:
            with open(filename) as f:
                return json.load(f)
        except FileNotFoundError:
            return 0

    def save_score(self, new_score):
        # Replaces the highest recorded score.
        try:
            with open(filename, 'w') as f:
                json.dump(new_score, f)
        except FileNotFoundError:
            with open(filename, 'w') as f:
                json.dump(new_score, f)