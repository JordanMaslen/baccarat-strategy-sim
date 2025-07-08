import random

class BaccaratGame:
    def __init__(self, players, num_hands=100, min_bet=1, max_bet=5000):
        self.players = players  
        self.num_hands = num_hands
        self.min_bet = min_bet
        self.max_bet = max_bet
        self.shoe = self.create_shoe()
        self.cut_card_position = random.randint(15, 20)
        self.burn_cards()
    
    def create_shoe(self):
        deck = [1,2,3,4,5,6,7,8,9,0,0,0,0] * 4 * 8  
        random.shuffle(deck)
        return deck
    
    def burn_cards(self):
        burn_count = min(10, len(self.shoe))
        self.shoe = self.shoe[burn_count:]
    
    def deal_card(self):
        return self.shoe.pop(0) if self.shoe else None

    def apply_strategy(self, player, count):
        if count == 1:
             return player["initial_bet"]
        else:
            strategy = player["strategy"]

            if strategy == "flat":
                return player["initial_bet"]  

            elif strategy == "martingale":
                return min(player["bet"] * 2 if not player["won_last_hand"] else player["initial_bet"], self.max_bet)

            elif strategy == "paroli":
                return min(player["bet"] * 2 if player["won_last_hand"] else player["initial_bet"], self.max_bet)

            elif strategy == "fibonacci":
                if not player["won_last_hand"] and player['consecutive_hands_lost'] > 0:
                    fib_sequence = [1, 1]
                    while len(fib_sequence) <= player['consecutive_hands_lost']:
                        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
                    return min(fib_sequence[player['consecutive_hands_lost']], self.max_bet)
                return player["initial_bet"]

            elif strategy == "1-3-2-4":
                sequence = [1, 3, 2, 4]
                stage = player['consecutive_hands_won'] % len(sequence)
                return min(sequence[stage] * player["initial_bet"], self.max_bet)

            return player["bet"]  

    def play_hand(self, count):
        if len(self.shoe) <= self.cut_card_position:
            self.shoe = self.create_shoe()
            self.burn_cards()
            
        player_hand = [self.deal_card(), self.deal_card()]
        banker_hand = [self.deal_card(), self.deal_card()]
        
        player_total = sum(player_hand) % 10
        banker_total = sum(banker_hand) % 10
        
        if player_total < 6:
            player_hand.append(self.deal_card())
            player_total = sum(player_hand) % 10
        
        if banker_total < 6:
            banker_hand.append(self.deal_card())
            banker_total = sum(banker_hand) % 10
        
        outcome = 'player' if player_total > banker_total else 'banker' if banker_total > player_total else 'tie'
        
        for player in self.players:
            bet_choice = "banker" if player["strategy"] == "banker_only" else random.choice(["player", "banker"])
            player["bet"] = self.apply_strategy(player, count)  
            bet_amount = min(max(player["bet"], self.min_bet), self.max_bet)  
            
            player['lowest_bankroll'] = min(player['lowest_bankroll'], player['bankroll'])

            if player['bankroll'] < bet_amount:
                shortfall = player['bankroll']
                player['bankroll'] = player['initial_bankroll'] + shortfall  
                player['rebuys'] += 1

            if bet_choice == outcome:
                if outcome == "banker":
                    winnings = (bet_amount * 0.95) + bet_amount 
                else:
                    winnings = bet_amount * 2  
                    
                player["won_last_hand"] = True     
                net_profit = winnings - bet_amount  
                player['bankroll'] += net_profit
                player['bankroll_total'] += net_profit
                player['profit_loss'] += net_profit  
                player['hands_won'] += 1
                player['bet'] = player['initial_bet'] 
                player['consecutive_hands_won'] += 1
                player['consecutive_hands_lost'] = 0

            elif outcome == 'tie':
                pass  
            
            else:
                player["won_last_hand"] = False   
                player['bankroll'] -= bet_amount
                player['bankroll_total'] -= bet_amount
                player['profit_loss'] -= bet_amount  
                player['hands_lost'] += 1
                player['bet'] = min(player['bet'] * 2, self.max_bet)  
                player['consecutive_hands_lost'] += 1
                player['consecutive_hands_won'] = 0
            
            player['lowest_bankroll'] = min(player['lowest_bankroll'], player['bankroll_total'])
            player['highest_bankroll'] = max(player['highest_bankroll'], player['bankroll_total'])

    def simulate(self):
        count = 1
        for _ in range(self.num_hands):
            self.play_hand(count)
            count += 1
        for player in self.players:
            print(f"Player {player['id']} ({player['strategy']} Strategy) - P/L: {player['profit_loss']}, Highest: {player['highest_bankroll']}, Lowest: {player['lowest_bankroll']}, Wins: {player['hands_won']}, Losses: {player['hands_lost']}")

# ✅ Function to create players with different strategies
def create_player(player_id, initial_bankroll, initial_bet, strategy):
    return {
        'id': player_id, 
        'bankroll': initial_bankroll, 
        'initial_bankroll': initial_bankroll, 
        'bankroll_total': initial_bankroll, 
        'bet': initial_bet, 
        'initial_bet': initial_bet,
        'rebuys': 0, 
        'profit_loss': 0, 
        'hands_won': 0, 
        'hands_lost': 0, 
        'consecutive_hands_won': 0, 
        'consecutive_hands_lost': 0, 
        'lowest_bankroll': initial_bankroll, 
        'highest_bankroll': initial_bankroll,
        'strategy': strategy,  
        'won_last_hand': False
    }

# ✅ Run multiple simulations and summarize results
simulations = 10
num_hands = 1000
summary = {}

for sim in range(simulations):
    print(f"\n🔹 Running Simulation {sim + 1}...\n")
    players = [
        create_player(1, 1000, 10, "flat"),
        create_player(2, 1000, 10, "martingale"),
        create_player(3, 1000, 10, "paroli"),
        create_player(4, 1000, 10, "fibonacci"),
        create_player(5, 1000, 10, "1-3-2-4"),
        create_player(6, 1000, 10, "banker_only")
    ]
    
    game = BaccaratGame(players=players, num_hands=num_hands, min_bet=1, max_bet=5000)
    game.simulate()
    
    # Track performance by strategy
    for player in players:
        strategy = player["strategy"]
        if strategy not in summary:
            summary[strategy] = {"total_PL": 0, "highest": float('-inf'), "lowest": float('inf')}
        
        summary[strategy]["total_PL"] += player["profit_loss"]
        summary[strategy]["highest"] = max(summary[strategy]["highest"], player["highest_bankroll"])
        summary[strategy]["lowest"] = min(summary[strategy]["lowest"], player["lowest_bankroll"])

# ✅ Print Summary
print("\n🔹 **Final Strategy Summary After 10 Simulations** 🔹\n")

best_strategy = None
worst_strategy = None
best_PL = float('-inf')
worst_PL = float('inf')

for strategy, stats in summary.items():
    avg_PL = stats['total_PL'] / simulations  # Calculate average P/L

    print(f"{strategy.capitalize()} Strategy - Avg P/L: {avg_PL:.2f}, Highest: {stats['highest']}, Lowest: {stats['lowest']}")

    # Track best and worst strategies based on Avg P/L
    if avg_PL > best_PL:
        best_PL = avg_PL
        best_strategy = strategy

    if avg_PL < worst_PL:
        worst_PL = avg_PL
        worst_strategy = strategy

# ✅ Print Best and Worst Strategies
print("\n🔹 **Best & Worst Strategies Based on Avg P/L** 🔹")
print(f"✅ Best Strategy: {best_strategy.capitalize()} with Avg P/L: {best_PL:.2f}")
print(f"❌ Worst Strategy: {worst_strategy.capitalize()} with Avg P/L: {worst_PL:.2f}")

