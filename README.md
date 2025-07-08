# 🃏 Baccarat Strategy Simulation

A Python-based simulation tool that models Baccarat gameplay and evaluates the performance of various betting strategies over thousands of hands.

This project simulates multiple players, each using a distinct strategy (Flat, Martingale, Paroli, Fibonacci, 1-3-2-4, Banker Only), and outputs both individual and comparative results across multiple simulations.

## 🎯 Features

- Simulates full Baccarat gameplay including dealing, third card rules, and outcome determination
- Implements and compares popular betting strategies
- Tracks performance metrics like profit/loss, bankroll highs/lows, and hands won/lost
- Supports rebuy logic if bankroll drops below minimum
- Runs multiple simulations and prints summarized strategy performance

## 🧠 Strategies Implemented

- **Flat Betting**: Same bet every hand
- **Martingale**: Double after a loss
- **Paroli**: Double after a win
- **Fibonacci**: Increase bet using Fibonacci sequence after losses
- **1-3-2-4**: Structured progression on wins
- **Banker Only**: Always bets on banker

## 🚀 Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/baccarat-simulation.git
   cd baccarat-simulation

2. Run the simulation:
'''bash
python Baccarat_Simulation.py

🔹 Running Simulation 1...

Player 1 (flat Strategy) - P/L: 80, Highest: 1080, Lowest: 880, Wins: 489, Losses: 491
...

🔹 Final Strategy Summary After 10 Simulations 🔹

Flat Strategy - Avg P/L: 42.00, Highest: 1120, Lowest: 890
Martingale Strategy - Avg P/L: -208.00, Highest: 1030, Lowest: 600
...

✅ Best Strategy: Flat with Avg P/L: 42.00
❌ Worst Strategy: Martingale with Avg P/L: -208.00



