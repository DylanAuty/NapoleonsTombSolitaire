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
        # self.piles[11] = [6, 8, 3, 6, 1, 8, 10, 6, 8, 7, 2, 8, 5, 11, 7, 0, 5, 10, 7, 2, 4, 3, 2, 2, 12, 10, 0, 4, 11, 0, 9, 12, 3, 12, 4, 7, 1, 9, 9, 1, 1, 3, 9, 0, 5, 12, 11, 6, 10, 11, 4, 5]
        
        # self.hashmap = {    # What piles can a given card go on? On self.hashmap.get(card, []).
        #     0:[5, 6, 7, 8],
        #     1: [5, 6, 7, 8],
        #     2: [5, 6, 7, 8],
        #     3: [5, 6, 7, 8],
        #     4: [5, 6, 7, 8],
        #     5: [4, 5, 6, 7, 8, 9],
        #     6: [0, 1, 2, 3, 5, 6, 7, 8],
        #     7: [5, 6, 7, 8],
        #     8: [5, 6, 7, 8],
        #     9: [5, 6, 7, 8],
        #     10: [5, 6, 7, 8],
        #     11: [5, 6, 7, 8],
        #     12: [5, 6, 7, 8],
        # }
        self.hashmap = self._rebuild_get_hashmap()  # Stores card: valid destination pile mappings (what piles can this card go on?).
        self.reverse_hashmap = self._rebuild_get_reverse_hashmap()  # Stores pile: valid card placement mappings (what cards can go on this pile?).


    def print_state(self):
        """ Pretty-print the game state. """
        print("##### Hashmap:")
        for k, v in self.hashmap.items():
            print(f"{k}: {v}")
        print(f"######## Piles:")
        for i, p in enumerate(self.piles):
            print(f"({i}) {self.pile_names[i]}: {p}")


    def _check_hashmap(self) -> bool:
        """ Check that the hashmap is correct by recomputing it.
        
        Returns:
            bool: whether the current hashmap is what it should be based on the state of the piles.
        """
        return self.hashmap == self._rebuild_get_hashmap()


    def _rebuild_get_hashmap(self) -> dict:
        """ Build the hashmap from scratch and return it. 
        Hashmap shows which piles a given card can be placed on.

        Returns:
            dict: The rebuilt hashmap, with 12 items. Keys are card values, values are lists of pile indices
         """
        hashmap = {}
        for i, p in enumerate(self.piles):
            top_card = p[-1] if len(p) > 0 else None
            if i <= 3:  # 7s
                if top_card is None:    # Empty pile: accepts 7s only.
                    hashmap[6] = hashmap.get(6, []) + [i]
                else:
                    new_val = top_card + 1
                    hashmap[new_val] = hashmap.get(new_val, []) + [i]
            elif i == 4:    # 6s
                if top_card is None or top_card == 0:    # Empty pile or ace on top: accepts 6s only.
                    hashmap[5] = hashmap.get(5, []) + [i]
                else:
                    new_val = top_card - 1
                    hashmap[new_val] = hashmap.get(new_val, []) + [i]
            elif i >= 5 and i <= 8:
                if len(p) == 0:
                    for j in range(13):
                        hashmap[j] = hashmap.get(j, []) + [i]
            elif i == 9:    # Spare 6s
                if len(p) < 4:
                    hashmap[5] = hashmap.get(5, []) + [i]

            # 10 == discard. Ignored as it's the last place anything should go.
            # 11 == deck. things never go on the deck.

        return hashmap


    def _check_reverse_hashmap(self) -> bool:
        """ Confirm the reverse hashmap is correct by fully rebuilding it and confirming. 
        
        Returns:
            bool: Whether or not self.reverse_hashmap is correct.
        """
        return self._rebuild_get_reverse_hashmap() == self.reverse_hashmap
    

    def _rebuild_get_reverse_hashmap(self) -> dict:
        """ Build the reverse hashmap from the hashmap. 
        Reverse hashmap shows what cards are mapped to which piles in the hashmap. 
        
        Returns:
            dict: the reverse_hashmap. Keys are card values, values are pile indices.
        """
        reverse_hashmap = {}    # Use a pile index to look up which cards have it as a valid destination.
        for k, v in self.hashmap.items():
            for vv in v:
                reverse_hashmap[vv] = reverse_hashmap.get(vv, []) + [k]

        return reverse_hashmap


    def _attempt_pile_placement(self, source_pile_idx: int) -> bool:
        """ Try to place the top card of a given pile on one of the other piles.

        Params:
            pile_idx (int): Index of pile to attempt placement from (not to). 0123 are 7s piles, 4 is 6s, 5678 are spares, 9 is spare 6s, 10 is discard, and 11 is deck.

        Returns:
            bool: Whether placement was successful. 
        """
        # print(f"Attempting placement from {source_pile_idx}")
        dest_pile_idx = None

        # Define definitely invalid destination piles
        invalid_dest_idxs = [source_pile_idx]   # Disallow self-moves
        if source_pile_idx >= 5 and source_pile_idx <= 9:
            invalid_dest_idxs += [5, 6, 7, 8]   # Disallow spare-to-spare moves

        # Find destination
        top_card = self.piles[source_pile_idx][-1] if len(self.piles[source_pile_idx]) > 0 else None
        if top_card is None:
            return False  # Nothing to place, so nothing to do
        else:
            valid_destinations = self.hashmap.get(top_card, [])
            if len(valid_destinations) == 0:
                return False
            else:
                for i, d in enumerate(valid_destinations):
                    if d not in invalid_dest_idxs:
                        dest_pile_idx = self.hashmap[top_card]
                        break
        
                # Execute move and update hashmap
                if dest_pile_idx is None:
                    return False
                else:
                    self.piles[dest_pile_idx].append(self.piles[source_pile_idx].pop(-1))

                    # Reconcile source and destination hashmaps.
                    self.hashmap = self._rebuild_get_hashmap()
                    self.reverse_hashmap = self._rebuild_get_reverse_hashmap()
                    return True
                    
        return False
    

    def simulate_game(self) -> bool:
        """ Simulate one game. Return bool (True if win else False.) 

        Returns:
            bool: Whether a win occurred.
        """
        num_moves = 0
        while (any([len(self.piles[i]) > 0 for i in range(5, 12)])):    # Win condition: no placeable cards left.
            num_moves += 1
            # print(f"Move {num_moves}: {[len(self.piles[i]) for i in range(len(self.piles))]}")

            # self.print_state()
            # breakpoint()

            # Check discard pile
            if self._attempt_pile_placement(source_pile_idx=10):
                continue

            # Check spares piles
            elif self._attempt_pile_placement(source_pile_idx=5):
                # print("Succeeded placement from 5")
                continue
            elif self._attempt_pile_placement(source_pile_idx=6):
                # print("Succeeded placement from 6")
                continue
            elif self._attempt_pile_placement(source_pile_idx=7):
                # print("Succeeded placement from 7")
                continue
            elif self._attempt_pile_placement(source_pile_idx=8):
                # print("Succeeded placement from 8")
                continue
            elif self._attempt_pile_placement(source_pile_idx=9):
                # print("Succeeded placement from 9")
                continue

            # Both failed, so attempt deck placement
            elif self._attempt_pile_placement(source_pile_idx=11):
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