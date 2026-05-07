## Market Making Simulator & Limit Order Book Engine
#### A high-performance Limit Order Book (LOB) simulator and market making research framework built in Python to study market microstructure, inventory risk, and optimal quoting strategies used in modern electronic trading systems.

#### This project implements:

- A price-time priority matching engine
- Realistic order book mechanics
- Inventory-aware market making
- Avellaneda–Stoikov optimal quoting model
- Backtesting & PnL analytics
- Strategy comparison framework
- Visualization pipeline for inventory and profitability analysis

#### Designed as a portfolio project targeting:

- Quant Developer roles
- HFT / Prop Trading interviews
- Electronic Trading Engineering positions
- Market Microstructure research

## Features
#### Matching Engine

- Price-time priority execution
- FIFO queue matching
- Limit & market order support
- Partial fills
- Order cancellation support
- Trade logging system

#### Market Simulation

- Simulated market order flow
- Bid/ask spread dynamics
- Mid-price tracking
- Inventory & cash accounting
- Controlled reproducibility via random seeds

### Trading Strategies
#### Heuristic Market Maker

- Inventory skew adjustment
- Spread control
- Quote refresh logic
- Risk-aware quoting

#### Avellaneda–Stoikov Model

- Reservation price calculation
- Optimal spread derivation
- Inventory risk penalization
- Time-decay adjustment
- Inventory limits

### Analytics

- PnL tracking
- Inventory tracking
- Sharpe ratio
- Maximum drawdown
- Comparative strategy evaluation

### Visualization

- PnL comparison plots
- Inventory trajectory plots
- Saved experiment outputs

## Project Structure

```
market-making-simulator/
│
├── core/
│   ├── order.py
│   └── order_book.py
│
├── strategies/
│   ├── base_strategy.py
│   ├── heuristic_mm.py
│   └── avellaneda_stoikov.py
│
├── simulation/
│   └── simulator.py
│
├── analysis/
│   ├── metrics.py
│   └── plots.py
│
├── results/
│   ├── pnl_comparison.png
│   └── inventory_comparison.png
│
├── main.py
└── README.md
```

## Core Engine Architecture
### Order Matching Logic

The matching engine follows strict price-time priority:

1) Better price executes first
2) Earlier order gets priority within same price level
3) Supports partial execution and queue continuation

### Supported Order Types

- Limit Orders
- Market Orders

### Data Structures

- SortedDict for efficient bid/ask access
- deque for FIFO queue management

This design mirrors simplified versions of real exchange matching systems.

## Strategies
### 1. Heuristic Market Maker

A simple inventory-aware market making strategy.

#### Logic

- Quotes around mid-price
- Adjusts bid/ask skew based on inventory
- Avoids unnecessary quote refreshes
- Attempts to mean-revert inventory exposure

#### Risk Management

- Inventory skew parameter
- Quote suppression during low movement

### 2. Avellaneda–Stoikov Market Maker

Implementation of the classical stochastic control framework for optimal market making.

#### Reservation Price

$$
r = S - q\gamma\sigma^2 (T-t)
$$

#### Optimal Spread

$$
\delta = \gamma\sigma^2 (T-t) + \frac{2}{\gamma}\ln\left(1+\frac{\gamma}{k}\right)
$$

Where:

- $S$ = mid price
- $q$ = inventory
- $\gamma$ = risk aversion
- $\sigma$ = volatility
- $k$ = liquidity parameter

#### Features

- Dynamic spread optimization
- Inventory risk penalization
- Time-decay behavior
- Reservation pricing
- Inventory bounds

## Simulation Workflow
```
Market Orders Arrive
        ↓
Strategies Generate Quotes
        ↓
Order Book Matches Orders
        ↓
Trades Update Inventory & Cash
        ↓
PnL + Metrics Computed
        ↓
Results Visualized
```
## Results
### PnL Comparison

The Avellaneda–Stoikov model produced:

- Higher profitability
- Better Sharpe ratio
- Lower drawdown
- Improved inventory control

### Inventory Comparison

Inventory dynamics reveal:

- Heuristic MM stays near flat inventory
- AS model accepts larger inventory swings for higher expected profit

## Sample Output
```
===== COMPARISON =====

Heuristic MM:
final_pnl: 360.0000
sharpe: 0.2157
max_drawdown: 17.5000
mean_pnl: 191.6410

Avellaneda-Stoikov:
final_pnl: 520.0000
sharpe: 0.5009
max_drawdown: 10.0000
mean_pnl: 247.7375
```

## Performance Characteristics

| Operation | Complexity
| ----------|------------|
| Best Bid/Ask Lookup | O(1) |
| Insert Order | O(log n)|
| Cancel Order | O(n) |  
| Queue Match | O(1) |

## Technologies Used

- Python
- NumPy
- Matplotlib
- SortedContainers

## How to Run

### Install Dependencies

- pip install numpy matplotlib sortedcontainers

### Run Simulation

- python main.py

Results will automatically be saved inside:

- results/

## Future Improvements

- Latency simulation
- Multi-level order book depth
- Hawkes process order arrivals
- Queue position modeling
- Adverse selection modeling
- Reinforcement learning market maker
- Async matching engine
- Performance benchmarking
- Historical market data replay
- Transaction cost modeling

## Interview Talking Points

This project demonstrates understanding of:

- Market microstructure
- Electronic trading systems
- Inventory risk management
- Matching engine design
- Optimal market making
- Backtesting systems
- Simulation architecture
- Quantitative trading concepts
- Performance-oriented data structures

## Key Takeaways

- Implemented a realistic simplified exchange simulator
- Built inventory-aware market making systems
- Compared heuristic vs stochastic control approaches
- Evaluated strategies using quantitative metrics
- Designed modular architecture for future research extensions

## Disclaimer

This project is for educational and research purposes only and does not constitute financial advice or production trading infrastructure.
