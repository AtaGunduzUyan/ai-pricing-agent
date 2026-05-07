# Black Box AI Pricing Agent

This project simulates price competition between LLM-based firms in a repeated market environment.

The main goal is to observe how agents behave under limited information conditions.  
This folder contains the Black Box version of the simulation.

## Black Box Setting

In the Black Box setup, firms only have access to their own historical data:

- previous prices
- demand
- profit values

They do not directly observe competitor prices.

Because of this, agents make decisions only from self-feedback and market outcomes instead of reacting to a visible competitor strategy.

## Project Structure

```text
BlackBox-ai-pricing-agent/
│
├── src/
│   └── core simulation logic
│
├── ui/
│   └── GUI components
│
├── main.py
├── README.md
└── requirements.txt
```

## Features

- LLM-based pricing agents
- Repeated duopoly competition
- Customer demand simulation
- Profit and sales tracking
- Data visualization
- Black Box information structure

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the simulation:

```bash
python main.py
```

## Notes

This project was developed as part of a graduation project focused on combining Agent-Based Modeling (ABM) with LLM-driven decision systems.
