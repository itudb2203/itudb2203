class HallOfFame:
    def __init__(self, yearid, votedBy, ballots, needed, votes, inducted, category):
        self.yearid = yearid # Year
        self.votedBy = votedBy # Voting method
        self.ballots = ballots # Total cast ballots
        self.needed = needed # Needed votes
        self.votes = votes # Received votes
        self.inducted = inducted # If player is inducted
        self.category = category # Category of Hall of Fame