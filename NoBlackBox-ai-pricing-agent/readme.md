# No Black Box AI Pricing Agent

This project simulates price competition between LLM-based firms in a repeated market environment.

The main goal is to observe how agents behave when competitor information is visible.  
This folder contains the No Black Box version of the simulation.

## No Black Box Setting

In the No Black Box setup, firms have access to both their own historical data and competitor price information:

- previous prices
- demand
- profit values
- competitor prices

Because of this, agents can react more directly to competitor behavior and adapt their pricing strategies accordingly.

Compared to the Black Box setup, this environment creates a more transparent market structure and allows stronger strategic interaction between firms.

## Project Structure

```text
NoBlackBox-ai-pricing-agent/
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
- Competitor-aware pricing behavior
- Data visualization
- No Black Box information structure

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
