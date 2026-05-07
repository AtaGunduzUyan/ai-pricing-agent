# AI Pricing Agent

This repository contains simulations of LLM-based firms competing in a repeated pricing environment.

The project extends a traditional Agent-Based Modeling (ABM) setup by replacing rule-based seller behavior with Large Language Model (LLM) agents.

The main focus is to observe how information visibility changes pricing behavior, market stability, and strategic interaction between firms.

## Repository Overview

The repository includes two different simulation settings:

### Black Box

Firms only observe their own historical performance:

- previous prices
- demand
- profit values

Competitor prices are hidden.

This creates a limited-information environment where agents learn only from self-feedback.

### No Black Box

Firms observe both their own historical data and competitor price information.

This creates a more transparent market structure and allows stronger strategic interaction between firms.

## Repository Structure

```text
ai-pricing-agent/
│
├── BlackBox-ai-pricing-agent/
│   └── Black Box simulation
│
├── NoBlackBox-ai-pricing-agent/
│   └── No Black Box simulation
│
├── README.md
└── .gitignore
```

## Main Features

- LLM-based pricing agents
- Repeated duopoly competition
- Black Box and No Black Box information structures
- Customer demand simulation
- Profit and sales tracking
- Data visualization
- Simulation-based market analysis

## Technologies

- Python
- Gemini / Vertex AI
- NumPy
- Pandas
- Matplotlib
- Tkinter

## Running the Project

Each folder contains its own simulation setup and requirements.

Example:

```bash
pip install -r requirements.txt
python main.py
```

## Academic Context

This project was developed as part of a graduation project focused on combining Agent-Based Modeling (ABM) with LLM-driven decision systems.
