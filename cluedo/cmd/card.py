class Card:
    """card indicating informations in the game

    Attrs:
        category (str): falls in one of ["character", "weapon", "room"]
        description (str): name of the card, no idea why I chose such long name
        is_answer (bool): is this card one of the correct answer cards
    """
    def __init__(self, category, description):
        self.category = category
        self.description = description
        self.is_answer = False

    def make_answer(self):
        """mark this card to be correct answer
        
        """
        self.is_answer = not self.is_answer

    def __repr__(self) -> str:
        """DEBUG: for command line output

        """
        if self.is_answer:
            constr = "Answer"
        else:
            constr = ""
        return "\n[Type: {self.category}, Text: {self.description}, {constr}]".format(self = self, constr = constr)

