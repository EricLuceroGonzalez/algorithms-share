# 🧪 Eric Lucero | Optimization and AI

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![JavaScript](https://img.shields.io/badge/javascript-ES6+-yellow.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

# FIFA World Cup 2026 Draw Generator 🧬⚽

A Genetic Algorithm implementation to solve the complex constraint satisfaction problem of the FIFA World Cup 2026 group draw.

## 🚀 Overview

The 2026 World Cup introduces a 48-team format with 12 groups, creating a combinatorial explosion of possibilities ($3.9 \times 10^{31}$). This project uses an evolutionary approach to find a valid draw that satisfies all FIFA constraints in milliseconds.

**Read the full article and explanation:** [Generador de grupos de la Copa Mundial de la FIFA](https://eric-lucero-gonzalez.vercel.app/es/blog/sorteo-mundial)

## 🛠️ Constraints Handled

1.  **Hard Constraints:**
    * Valid Pot distribution (1 team from each pot per group).
    * Confederation separation (No duplicate confederations per group, except UEFA max 2).
    * Host allocation (Mexico A1, Canada B1, USA D1).
2.  **Soft/Heuristic Constraints:**
    * Top Seeds itinerary separation (Spain/Argentina and France/England on opposite bracket sides).

## 💻 Tech Stack

* **Logic:** JavaScript (ES6+) / Python
* **Visualization:** React + Next.js + Styled Components (view `visualization.js`)

## 🧬 Algorithm Details

* **Representation:** Array of 12 groups.
* **Selection:** Roulette Wheel Selection (inverse fitness).
* **Crossover:** Stratified Crossover (swaps entire pots to maintain structure).
* **Mutation:** Intra-pot swap (probability 0.2).

## 📦 Usage

### Python Version
```bash
cd python
python main.py
```

### JavaScript Logic
You can import the `logic.js` file into any Node.js or browser project.

```javascript
import { ejecutarGA } from './javascript/logic';
const result = ejecutarGA();
console.log(result);
```

## 👨‍💻 Author

**Eric Lucero**
* [Website]([https://](https://eric-lucero-gonzalez.vercel.app/))
* [Twitter](https://x.com/EricLuceroG)