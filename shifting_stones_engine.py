import random

class Card:
    
    def __init__(self, card_id, pattern, points):
        self.id = card_id
        self.points = points
        self.pattern = pattern 

    def render(self):
        """Returns an array of strings representing the clean visual card box."""
        header = f" ID: {self.id} ({self.points}pts)"
        lines = [header.ljust(21),"+-------+".ljust(21)]
        for r in range(3):
            row_chars = []
            for c in range(3):
                if (r, c) in self.pattern:
                    row_chars.append(self.pattern[(r, c)])
                else:
                    row_chars.append(".")
            row_str = f"| {row_chars[0]} {row_chars[1]} {row_chars[2]} |"
            lines.append(row_str.ljust(21))
            
        lines.append("+-------+".ljust(21))
        return lines

class Stone:
    
    def __init__(self, color_pair):
        self.pair = color_pair
        self.current_index = 0      

    @property
    def color(self):
        return self.pair[self.current_index]

    def flip(self):
        self.current_index = 1 - self.current_index

    def __repr__(self):
        return self.color


class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.cards_scored_count = 0
        self.hand = []  
        self.has_skipped_last_turn = False  

    def spend_card(self, card_id):
        for index, card in enumerate(self.hand):
            if card.id == card_id:
                return self.hand.pop(index)
        return None


class ShiftingStones:
    def __init__(self, player_names):
        
        # O = orange ; R = red : P = purple ; B = blue ; Y = yellow ; K = black ; W = white ; G = green
        
        tile_pool = [('Y', 'K'),('O', 'R'), ('O', 'R'),('B', 'P'), ('B', 'P'), ('B', 'P'),('W', 'G'), ('W', 'G'), ('W', 'G')]  
        random.shuffle(tile_pool)
        
        self.grid = []
        idx = 0
        
        for r in range(3):
            row = []
            for c in range(3):
                row.append(Stone(tile_pool[idx]))
                idx += 1
            self.grid.append(row)
            
        self.deck = self._create_structured_deck()
        self.discard_pile = []
        
        self.endgame_triggered = False
        self.endgame_trigger_player_idx = None
        
        self.players = [Player(name) for name in player_names]
        
        for p in self.players:
            for _ in range(4):
                card = self._draw_card()
                if card:
                    p.hand.append(card)
                    
        self.current_player_idx = 0

    def _draw_card(self):
        if not self.deck:
            if not self.discard_pile:
                return None  
            print("\n[ Deck exhausted! Shuffling discard pile back into the deck... ]")
            self.deck = list(self.discard_pile)
            random.shuffle(self.deck)
            self.discard_pile.clear()
        return self.deck.pop() if self.deck else None

    def _is_valid_pattern(self, pattern_dict):
        counts = {'YK': 0, 'OR': 0, 'BP': 0, 'WG': 0}
        for symbol in pattern_dict.values():
            if symbol in ['Y', 'K']: counts['YK'] += 1
            elif symbol in ['O', 'R']: counts['OR'] += 1
            elif symbol in ['B', 'P']: counts['BP'] += 1
            elif symbol in ['W', 'G']: counts['WG'] += 1
        if counts['YK'] > 1 or counts['OR'] > 2 or counts['BP'] > 3 or counts['WG'] > 3: 
            return False
        return True

    def _generate_valid_symbols(self, count):
        symbols_pool = ['Y', 'K', 'O', 'R', 'B', 'P', 'W', 'G']
        while True:
            sampled = random.sample(symbols_pool, count)
            dummy_pattern = {i: sym for i, sym in enumerate(sampled)}
            if self._is_valid_pattern(dummy_pattern):
                return sampled

    def _create_structured_deck(self):
        deck = []
        card_id = 1

        chosen_symbols = self._generate_valid_symbols(6)
        for sym in chosen_symbols:
            deck.append(Card(card_id, {(1, 1): sym}, 1))
            card_id += 1

        for i in range(24):
            while True:
                sym1, sym2 = self._generate_valid_symbols(2)
                r1, c1 = random.randint(0, 2), random.randint(0, 2)
                if r1 < 2 and (c1 == 2 or random.choice([True, False])):
                    r2, c2 = r1 + 1, c1
                else:
                    c2 = c1 + 1 if c1 < 2 else c1 - 1
                    r2 = r1
                pattern = {(r1, c1): sym1, (r2, c2): sym2}
                if self._is_valid_pattern(pattern):
                    deck.append(Card(card_id, pattern, 1))
                    card_id += 1
                    break

        for i in range(12):
            while True:
                sym1, sym2 = self._generate_valid_symbols(2)
                r1, c1 = random.choice([(0,0), (0,2), (2,0), (2,2)])
                r2, c2 = random.choice([(0,1), (1,0), (1,2), (2,1), (1,1)])
                pattern = {(r1, c1): sym1, (r2, c2): sym2}
                if self._is_valid_pattern(pattern):
                    deck.append(Card(card_id, pattern, 2))
                    card_id += 1
                    break

        for j in range(12):
            while True:
                line_syms = self._generate_valid_symbols(3)
                is_row = random.choice([True, False])
                fixed_index = random.randint(0, 2)
                pattern = {}
                for i in range(3):
                    r, c = (fixed_index, i) if is_row else (i, fixed_index)
                    pattern[(r, c)] = line_syms[i]
                if self._is_valid_pattern(pattern):
                    deck.append(Card(card_id, pattern, 2))
                    card_id += 1
                    break

        for i in range(4):
            while True:
                diag_syms = self._generate_valid_symbols(3)
                coords = [(0, 0), (1, 1), (2, 2)] if random.choice([True, False]) else [(0, 2), (1, 1), (2, 0)]
                pattern = {pos: diag_syms[idx] for idx, pos in enumerate(coords)}
                if self._is_valid_pattern(pattern):
                    deck.append(Card(card_id, pattern, 3))
                    card_id += 1
                    break

        v_configurations = [[(0,1), (2,0), (2,2)], [(2,1), (0,0), (0,2)], [(1,0), (0,2), (2,2)], [(1,1), (0,0), (2,2)]]
        for i in range(4):
            while True:
                v_syms = self._generate_valid_symbols(3)
                coords = random.choice(v_configurations)
                pattern = {pos: v_syms[idx] for idx, pos in enumerate(coords)}
                if self._is_valid_pattern(pattern):
                    deck.append(Card(card_id, pattern, 3))
                    card_id += 1
                    break

        for i in range(4):
            while True:
                split_syms = self._generate_valid_symbols(3)
                r1, c1 = random.randint(0, 1), random.randint(0, 1)
                pair = [(r1, c1), (r1 + 1, c1) if random.choice([True, False]) else (r1, c1 + 1)]
                all_coords = [(r, c) for r in range(3) for c in range(3)]
                valid_isolated = [
                    pos for pos in all_coords 
                    if pos not in pair and all(abs(pos[0]-p[0]) + abs(pos[1]-p[1]) > 1 for p in pair)
                ]
                if not valid_isolated: continue
                coords = pair + [random.choice(valid_isolated)]
                pattern = {pos: split_syms[idx] for idx, pos in enumerate(coords)}
                if self._is_valid_pattern(pattern):
                    deck.append(Card(card_id, pattern, 3))
                    card_id += 1
                    break

        for i in range(3):
            while True:
                x_syms = self._generate_valid_symbols(4)
                pattern = {(0, 0): x_syms[0], (0, 2): x_syms[1], (2, 0): x_syms[2], (2, 2): x_syms[3]}
                if self._is_valid_pattern(pattern):
                    deck.append(Card(card_id, pattern, 5))
                    card_id += 1
                    break

        for i in range(3):
            while True:
                cross_syms = self._generate_valid_symbols(4)
                pattern = {(0, 1): cross_syms[0], (2, 1): cross_syms[1], (1, 0): cross_syms[2], (1, 2): cross_syms[3]}
                if self._is_valid_pattern(pattern):
                    deck.append(Card(card_id, pattern, 5))
                    card_id += 1
                    break

        random.shuffle(deck)
        return deck

    def get_current_player(self):
        return self.players[self.current_player_idx]

    def next_turn(self):
        self.current_player_idx = (self.current_player_idx + 1) % len(self.players)

    def process_turn_end(self, player):
        player.has_skipped_last_turn = False
        while len(player.hand) < 4:
            card = self._draw_card()
            if card:
                player.hand.append(card)
            else:
                break
        self.next_turn()

    def check_and_auto_end_turn(self, player):
        if not player.hand:
            print(f"\n[ Notice: {player.name} has no cards left! Refilling hand and ending turn. ]")
            self.process_turn_end(player)
            return True
        return False

    def display(self):
        print("\n=== CURRENT BOARD CONFIGURATION ===")
        print("        Col 0   Col 1   Col 2")
        for r, row in enumerate(self.grid):
            print(f"Row {r}   " + "   |   ".join([str(stone) for stone in row]))
        print(f"=================================== [Deck Remainder: {len(self.deck)} Cards | Discard Pile: {len(self.discard_pile)} Cards]")
        if self.endgame_triggered:
            trigger_player = self.players[self.endgame_trigger_player_idx].name
            print(f"⚠️  [ ENDGAME ACTIVE: Triggered by {trigger_player}. This is the FINAL round! ]")

    def display_player_hand(self, player):
        print(f"=== {player.name}'s Current Hand ===")
        if not player.hand:
            print("[ Empty Hand ]")
            return
        rendered_hands = [card.render() for card in player.hand]
        for row_idx in range(6):
            combined_row = "    ".join(card_lines[row_idx] for card_lines in rendered_hands)
            print(combined_row)
        print("=" * 110)

    def verify_pattern_match(self, pattern):
        for (r, c), color_req in pattern.items():
            if self.grid[r][c].color != color_req:
                return False
        return True

    def flip_stone(self, r, c):
        if 0 <= r < 3 and 0 <= c < 3:
            self.grid[r][c].flip()
            return True
        return False

    def swap_stones(self, r1, c1, r2, c2):
        if not (0 <= r1 < 3 and 0 <= c1 < 3 and 0 <= r2 < 3 and 0 <= c2 < 3):
            return False
        if (abs(r1 - r2) + abs(c1 - c2)) == 1:
            self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]
            return True
        return False

    def check_endgame_condition(self, player):
        if not self.endgame_triggered and player.cards_scored_count >= 8:
            self.endgame_triggered = True
            self.endgame_trigger_player_idx = self.current_player_idx
            print(f"\n🚀 {player.name} has scored {player.cards_scored_count} cards! The endgame has been triggered!")
            print("All other players get one final turn to finish the current round.")

    def display_final_scores(self):
        print("\n" + "═" * 45)
        print("            🏆 FINAL LEADERBOARD 🏆            ")
        print("═" * 45)
        sorted_players = sorted(self.players, key=lambda p: (p.score, p.cards_scored_count), reverse=True)
        
        print(f"{'Rank':<6}{'Player':<15}{'Score':<12}{'Cards Scored':<10}")
        print("-" * 45)
        for idx, p in enumerate(sorted_players):
            medal = "🥇" if idx == 0 else "🥈" if idx == 1 else "🥉" if idx == 2 else f" {idx+1} "
            print(f"{medal:<5} {p.name:<15} {p.score:<12} {p.cards_scored_count:<10}")
        print("═" * 45)
        print("Thanks for playing Shifting Stones!\n")


def main():
    print("Welcome to Shifting Stones!")
    
    player_names = ["Player 1", "Player 2", "Player 3", "Player 4"]
    game = ShiftingStones(player_names)
    game_over = False

    last_player_idx = -1
    actions_taken_this_turn = 0

    while not game_over:
        current_player = game.get_current_player()
        

        if game.current_player_idx != last_player_idx:
            actions_taken_this_turn = 0
            last_player_idx = game.current_player_idx


        if game.endgame_triggered and game.current_player_idx == game.endgame_trigger_player_idx:
            print("\n[ The final round has completed! ]")
            game_over = True
            break

        game.display()
        game.display_player_hand(current_player)
        
        print(f"Active Player: {current_player.name}")
        print(f"Score: {current_player.score}  |  Cards Scored: {current_player.cards_scored_count}/8")
        print(f"Actions Taken This Turn: {actions_taken_this_turn}")
        print("-" * 50)
        
        print("Commands:")
        print("  > swap [r1] [c1] [r2] [c2] card [id]")
        print("  > flip [r] [c] card [id]")
        print("  > score card [id]")
        

        if actions_taken_this_turn == 0 and len(current_player.hand) < 5:
            print("  > skip  (Only valid as first action if hand size < 5)")
            
        if current_player.hand and len(current_player.hand) < 6:
            print("  > end   (Only valid if hand size is less than 6)")
        elif len(current_player.hand) == 6:
            print("  > [Hand is full (6 cards)! You MUST spend or score a card before ending your turn]")
        print("-" * 50)
        
        raw_input = input("Enter action: ").strip().split()

        if not raw_input:
            continue
            
        command = raw_input[0].lower()
        
        if command == "swap":
            try:
                r1, c1, r2, c2 = map(int, raw_input[1:5])
                target_card_id = int(raw_input[6])
            except (ValueError, IndexError):
                print("Format error! Use: swap [r1] [c1] [r2] [c2] card [id]")
                continue
                
            spent_card = current_player.spend_card(target_card_id)
            if not spent_card:
                print("Error: Card not in hand!")
                continue
                
            if game.swap_stones(r1, c1, r2, c2):
                game.discard_pile.append(spent_card)
                print(f"Executed Swap: Spent card ID {spent_card.id}.")
                actions_taken_this_turn += 1
                game.check_and_auto_end_turn(current_player)
            else:
                print("Error: Invalid spatial swap parameters.")
                current_player.hand.append(spent_card)
                
        elif command == "flip":
            try:
                r, c = map(int, raw_input[1:3])
                target_card_id = int(raw_input[4])
            except (ValueError, IndexError):
                print("Format error! Use: flip [r] [c] card [id]")
                continue
                
            spent_card = current_player.spend_card(target_card_id)
            if not spent_card:
                print("Error: Card not in hand!")
                continue
                
            if game.flip_stone(r, c):
                game.discard_pile.append(spent_card)
                print(f"Executed Flip: Spent card ID {spent_card.id}.")
                actions_taken_this_turn += 1
                game.check_and_auto_end_turn(current_player)
            else:
                print("Error: Invalid grid parameters.")
                current_player.hand.append(spent_card)

        elif command == "score":
            try:
                target_card_id = int(raw_input[2])
            except (ValueError, IndexError):
                print("Format error! Use: score card [id]")
                continue
                
            target_card = next((c for c in current_player.hand if c.id == target_card_id), None)
            if not target_card:
                print("Error: Card not found in hand.")
                continue

            if game.verify_pattern_match(target_card.pattern):
                current_player.hand.remove(target_card)
                game.discard_pile.append(target_card)
                current_player.score += target_card.points
                current_player.cards_scored_count += 1
                print(f"🎉 Success! Scored card ID {target_card.id} (+{target_card.points} pts).")
                
                actions_taken_this_turn += 1
                game.check_endgame_condition(current_player)
                game.check_and_auto_end_turn(current_player)
            else:
                print("Failed! Board state does not match this pattern.")
            input("Press Enter to continue...")

        elif command == "skip":
            if actions_taken_this_turn > 0:
                print("Error: You cannot skip after taking actions on your turn!")
                continue
            if len(current_player.hand) >= 5:
                print("Error: You cannot skip if you have 5 or more cards in hand!")
                continue
            if current_player.has_skipped_last_turn:
                print("Error: Double skipping is against constraints!")
                continue
                
            print(f"{current_player.name} draws 2 cards and skips the turn.")
            for _ in range(2):
                card = game._draw_card()
                if card:
                    current_player.hand.append(card)
            current_player.has_skipped_last_turn = True
            game.next_turn()

        elif command == "end":
            if len(current_player.hand) >= 6:
                print("Error: Hand is completely full! You must play at least one card to free up space.")
                continue
            print(f"Ending turn for {current_player.name}.")
            game.process_turn_end(current_player)

        elif command == "quit":
            game_over = True
            print("Exiting match.")
            break

    game.display_final_scores()


if __name__ == "__main__":
    main()
