# NapoleonsTomb.py
# Contains definition of the Napoleon's Tomb class, which defines a game of Napoleon's Tomb solitaire.

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
        
        self.piles = [[] for i in range(12)]  # 12 piles: 4 for 7s, 1 for 6s, 4 for spares, 1 for spare 6s, 1 for discard, 1 for deck
        # 0 1 2 3: 7s
        # 4: 6s
        # 5 6 7 8: spares
        # 9: spare 6s
        # 10: discard
        # 11: deck
        self.pile_names = ["7s", "7s", "7s", "7s", "6s", "s1", "s2", "s3", "s4", "spare_6s", "discard", "deck"]
        self.piles[11] = list(range(13)) * 4    # Generate deck, shuffle. Suits are irrelevant. Aces are 0s, KQJ are 10 11 and 12.
        random.shuffle(self.piles[11])
        # self.piles[11] = [4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 4, 3, 2, 1, 0, 5, 5, 5, 5, 6, 6, 6, 6]
        # self.piles[11] = [0, 1, 2, 3, 4, 5, 5, 9, 10, 11, 12, 8, 8, 8, 8, 7, 7, 7, 7, 6, 6, 6, 6]
        self.piles[11] = [6, 8, 3, 6, 1, 8, 10, 6, 8, 7, 2, 8, 5, 11, 7, 0, 5, 10, 7, 2, 4, 3, 2, 2, 12, 10, 0, 4, 11, 0, 9, 12, 3, 12, 4, 7, 1, 9, 9, 1, 1, 3, 9, 0, 5, 12, 11, 6, 10, 11, 4, 5]
        self.hashmap = {    # What piles can a given card go on? it can go on self.hashmap.get(card, []).
            0:[5, 6, 7, 8],
            1: [5, 6, 7, 8],
            2: [5, 6, 7, 8],
            3: [5, 6, 7, 8],
            4: [5, 6, 7, 8],
            5: [4, 9],
            6: [0, 1, 2, 3],
            7: [5, 6, 7, 8],
            8: [5, 6, 7, 8],
            9: [5, 6, 7, 8],
            10: [5, 6, 7, 8],
            11: [5, 6, 7, 8],
            12: [5, 6, 7, 8],
        }

        self.reverse_hashmap = {}    # I've occupied a pile. Where else in the hashmap do I need to update?
        for k, v in self.hashmap.items():
            for vv in v:
                self.reverse_hashmap[vv] = self.reverse_hashmap.get(vv, []) + [k]


    def print_state(self):
        """ Pretty-print the game state. """
        print(f"######## Piles:")
        for i, p in enumerate(self.piles):
            print(f"({i}) {self.pile_names[i]}: {p}")
        print("##### Hashmap:")
        for k, v in self.hashmap.items():
            print(f"{k}: {v}")


    def simulate_game(self) -> bool:
        """ Simulate one game. Return bool (True if win else False.) 

        Returns:
            bool: Whether a win occurred.
        """
        num_moves = 0
        while (any([len(self.piles[i]) > 0 for i in range(5, 12)])):    # Win condition: no placeable cards left.
            num_moves += 1
            # print(f"Move {num_moves}: {[len(self.piles[i]) for i in range(len(self.piles))]}")

            self.print_state()
            breakpoint()

            # Check discard pile
            if self._attempt_pile_placement(pile_idx=10):
                continue

            # Check spares piles
            elif any([self._attempt_pile_placement(pile_idx=i) for i in range(5, 10)]):
                continue

            # Both failed, so attempt deck placement
            elif self._attempt_pile_placement(pile_idx=11):
                continue
            else:
                if len(self.piles[11]) == 0:
                    # print(f"Failed, {num_moves} moves.")
                    if (all(self.piles[i] == [] for i in [5, 6, 7, 8, 9, 10, 11])) and \
                        (all(self.piles[i] == [6, 7, 8, 9, 10, 11, 12]) for i in [0, 1, 2, 3]) and \
                        self.piles[4] == [5, 4, 3, 2, 1, 0, 5, 4, 3, 2, 1, 0, 5, 4, 3, 2, 1, 0, 5, 4, 3, 2, 1, 0]:
                            breakpoint()
                    return False    # Discard is still full, but couldn't place it or anything else and there's nothing left to draw
                else:
                    # print(f"Placed a {self.piles[11][-1]} on the discard pile")
                    self.piles[10].append(self.piles[11].pop())

        # print(f"Succeeded, {num_moves} moves")
        if not ((all(self.piles[i] == [] for i in [5, 6, 7, 8, 9, 10, 11])) and \
            (all(self.piles[i] == [6, 7, 8, 9, 10, 11, 12]) for i in [0, 1, 2, 3]) and \
            self.piles[4] == [5, 4, 3, 2, 1, 0, 5, 4, 3, 2, 1, 0, 5, 4, 3, 2, 1, 0, 5, 4, 3, 2, 1, 0]):
                breakpoint()
        return True


    def _attempt_pile_placement(self, pile_idx: int) -> bool:
        """ Try to place the top card of a given pile on one of the other piles.

        Returns:
            bool: Whether placement was successful. 
        """
        # print(f"Placing card from pile: {pile_idx}")
        destination = None

        if pile_idx == 11:
            breakpoint()
        if len(self.piles[pile_idx]) > 0:
            card_val = self.piles[pile_idx][-1]
            if len(self.hashmap.get(card_val, [])) > 0:
                # If moving from a spares pile, cannot move to other spares piles.
                if pile_idx in [5, 6, 7, 8]:
                    # These piles can only move to 0, 1, 2, 3 or 9.
                    for i, val in enumerate(self.hashmap[card_val]):
                        if val <= 4 or val == 9:
                            destination = self.hashmap[card_val].pop(i)
                            # Re-add as a valid destination everywhere
                            for k, v in self.hashmap.items():
                                self.hashmap[k] = v + [pile_idx]
                            break
                    if destination is None:
                        return False    # No valid target pile found.
                elif pile_idx == 9:
                    if len(self.hashmap[card_val]) > 1:
                        for i, val in enumerate(self.hashmap[card_val]):
                            if val != 9:
                                destination = self.hashmap[card_val].pop(i)
                    elif self.hashmap[card_val] == 9:
                        return False
                    else:
                        destination = self.hashmap[card_val].pop()

                else:
                    if len(self.hashmap[card_val]) > 0:
                        destination = self.hashmap[card_val].pop()
                    else:
                        return False
                self.piles[destination].append(self.piles[pile_idx].pop())

                # print(f"Placed a {card_val} on pile {destination}")
                if destination in [0, 1, 2, 3]: # 7s: pile grows upwards
                    card_val += 1
                    self.hashmap[card_val] = self.hashmap.get(card_val, []) + [destination]
                elif destination == 4:  # 6s: pile growns downwards
                    card_val = (card_val - 1) % 6
                    self.hashmap[card_val] = self.hashmap.get(card_val, []) + [destination]
                elif destination in [5, 6, 7, 8]:   # Spares pile is occupied now; remove as candidate everywhere.
                    if len(self.reverse_hashmap[destination]) > 1:
                        for d in self.reverse_hashmap[destination]:
                            for i, val in enumerate(self.hashmap[d]):
                                if val == destination:
                                    self.hashmap[d].pop(i)
                elif destination == 9:
                    if len(self.piles[destination]) < 4 and 9 not in self.hashmap[5]:
                        self.hashmap[5].append(9)

                return True
    
        return False