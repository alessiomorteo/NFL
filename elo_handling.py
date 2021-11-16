
class elo_match_handler():
    def __init__(self, team1_elo, team2_elo, team1_score, team2_score, k_value, beta_value):
        """This is class facilitates the handling of ELO scoring.

        Args:
            team1_elo (float): The ELO score of team 1 prior to the game
            team2_elo (float): The ELO score of team 2 prior to the game
            team1_score (int): The final score achieved by team 1 in the game
            team2_score (int): The final score achieved by team 2 in the game
            k_value (int): The K value to be used within the ELO calculations
            beta_value (int): The Beta value to be used within the ELO calculation
        """
        self.team1_elo = team1_elo
        self.team2_elo = team2_elo
        self.team1_score = team1_score
        self.team2_score = team2_score
        self.k_value = k_value
        self.beta_value = beta_value
        self.__set_expected_outcomes()
        self.__set_outcome()
        self.__update_elo_scores()
    
    @staticmethod
    def get_expected_outcome(RA, RB, f_factor):
        """Calculate the expected outcome of the game for team A (RA) according to the ELO scoring system.

        Args:
            RA (float): The pre-game ELO score of team A
            RB (float): The pre-game ELO score of team B
            f_factor (int): The f_factor is the beta value used within the ELO scoring equation

        Returns:
            float: Returns a float (between 0 and 1) reflecting the expected outcome of the game, relative to team A
        """
        expected_outcome_A = 1.0/(1 + 10**((RB - RA)/f_factor))
        return expected_outcome_A
    
    def __set_expected_outcomes(self):
        self.exp_outcome_team1 = elo_match_handler.get_expected_outcome(self.team1_elo, self.team2_elo, self.beta_value)
        self.exp_outcome_team2 = elo_match_handler.get_expected_outcome(self.team2_elo, self.team1_elo, self.beta_value)
        
    def __set_outcome(self):
        """Set the outcome of the game as a binary, whereby 1 indicates a win, 0 a loss, and 0.5 a draw.
        """
        if self.team1_score > self.team2_score:
            self.outcome_team1 = 1.0
            self.outcome_team2 = 0.0
        elif self.team2_score < self.team2_score:
            self.outcome_team1 = 0.0
            self.outcome_team2 = 1.0
        else:
            self.outcome_team1 = 0.5
            self.outcome_team2 = 0.5
    
    def __update_elo_scores(self):
        """Update each team's ELO score according to the ELO formula.
        """
        if self.outcome_team1 == 1.0:
            self.team1_elo = self.team1_elo + (self.k_value * (1.0 - self.exp_outcome_team1))
            self.team2_elo = self.team2_elo + (self.k_value * (0.0 - self.exp_outcome_team2))
        elif self.outcome_team2 == 1.0:
            self.team1_elo = self.team1_elo + (self.k_value * (0.0 - self.exp_outcome_team1))
            self.team2_elo = self.team2_elo + self.k_value * (1.0 - self.exp_outcome_team2)
        else:
            self.team1_elo = self.team1_elo + (self.k_value * (0.5 - self.exp_outcome_team1))
            self.team2_elo = self.team2_elo + (self.k_value * (0.5 - self.exp_outcome_team2))
            
    
    def get_both_expected_outcomes(self):
        return self.exp_outcome_team1, self.exp_outcome_team2
    
    def get_updated_scores(self):
        """Returns the post-game ELO score for each of the two teams

        Returns:
            tuple: The updated elo score for the two teams present
        """
        return (self.team1_elo, self.team2_elo)
    