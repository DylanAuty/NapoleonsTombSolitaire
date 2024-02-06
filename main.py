# Napoleons Tomb simulator
# Simulates a version of the Napoleon's Tomb solitaire game to work out the chances of winning.
import sys
import argparse
import random


class NapoleonsTomb:
    def __init__(self):
        """ Represent a game of Napoleons Tomb solitaire.
        
        Game rules:
        Shuffle deck. Start turning over cards.
        If card is a 6, it goes in the middle. If it's a 7, it goes in the corners.
        If it's neither a 6 nor a 7, it goes at the top/bottom/left/right.
        If there's already a 6 in the middle, it goes to the side for later use.
        Aim is to build the 7s pile up to K, and the 6s down to A.
        Once the 6s pile reaches A, a 6 can be placed on top.
        The top/bottom/left/right cards can be placed on top of the 7s or 6s piles if consecutively above/below respectively.
        To fill the gaps, the discard pile is used first, then drawing from the deck.
        If no legal move can be played, draw another card from the deck.
        Win if deck and discard pile are both exhausted and all cards are played, else lose. 
        
        """
        
        # Set up deck
        self.deck = list(range(13)) * 4  # Suits are irrelevant
        random.shuffle(self.deck)

        self.sevens = [[], [], [], []]
        self.sixes = []
        self.spare_sixes = []
        self.spares = []  # Max length == 4
        self.discard = []


    def simulate_game(self) -> bool:
        """ Simulate one game. Return bool (True if win else False.) 

        Returns:
            bool: Whether a win occurred.
        """

        while len(self.deck) > 0 or len(self.discard) > 0 or len(self.spares) > 0:
            placed = False
            # Fill empty spaces (spares, 7s, 6s).
            self._fill_empty_slots()

            # Try to place all spares.
            while(not self._place_spares()):
                continue
                
            
            
            # Try to place top of discard pile.
            
            # Try to place top card of deck. Succeeds unless deck is empty.

            if not placed:
                return False

        return True # Guaranteed win if deck, discard pile, and spares piles are all empty.

    
    def _place_spares(self) -> bool:
        """ Check spares piles for valid plays. 

        Returns:
            bool: whether play was found.
        """
        for card in self.spares:
            if card <= 5:
                if card == 5:
                    if self.sixes == [] or self.sixes[-1] == 0:
                        self.sixes.append(card)
                        return True
                    else:
                        self.spare_sixes.append(card)
                elif card == (self.sixes[-1] - 1):
                    self.sixes.append(card)
                    return True
                
            else:
                # Handle 7-Ks
                break
        return False

    
    def _fill_empty_slots(self) -> bool:
        # Check and fill empty slots
        while len(self.spares) != 4:
            if len(self.discard) > 0:
                self.spares.append(self.discard.pop(0))
            elif len(self.deck) > 0:
                self.spares.append(self.deck.pop(0))   # 6s will be handled when checking the board later
            else:
                sys.exit("Error: both discard and spares are empty, but trying to fill slots?")
        if len(self.spare_sixes) > 0:
            if self.sixes == [] or self.sixes[-1] == 0:
                self.sixes.append(self.spare_sixes.pop(0))
        


    


def main(args):
    wins = losses = 0   # Define both to allow early stopping
    for i in range(args.num_trials):
        game = NapoleonsTomb()
        result = game.simulate_game()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="NapoleonsTomb",
        description="Simulate the Napoleon's Tomb solitaire game",
    )
    parser.add_argument('-n', '--num_trials', type=int, default=1000, help="How many trials to simulate for.")

    args = parser.parse_args()
    main(args)