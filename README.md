# 🧪 Eric Lucero | Research & Algorithms Lab

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![JavaScript](https://img.shields.io/badge/javascript-ES6+-yellow.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

Welcome to the **code repository** companion for my research blog. Here you will find the source code, algorithms, and simulations discussed in my articles, ranging from Genetic Algorithms in Python to interactive React components.

🌐 **Read the articles:** [ericlucero.com/blog](https://ericlucero.com/blog)

---

## 📂 Repository Structure

The code is organized by topic and technology stack.

```text
.
├── 🧬 genetic-algorithms/   # Python scripts for evolution simulations
│   ├── world-cup-draw/      # The FIFA World Cup Draw logic
│   └── optimization/        # General function optimization
│
├── ⚛️ react-components/     # UI snippets shared on the blog
│   ├── hooks/               # Custom hooks (e.g., useTransition)
│   └── ui-kits/             # Styled-components and layouts
│
├── 📊 data-science/         # Jupyter Notebooks & Visualization
│   ├── chartjs-demos/       # Configurations for Chart.js
│   └── statistics/          # Probability models
│
└── 📝 latex-templates/      # LaTeX snippets for scientific notation
```

## 🚀 Highlights & Featured Code

1. Genetic Algorithms (Python)

Implementation of evolutionary strategies to solve constraint satisfaction problems (CSP), specifically applied to sports tournament draws.

Key File: `genetic-algorithms/world-cup-draw/fitness.py`

Concepts: Chromosomes, Mutation, Crossover, Fitness Function constraints (confederations, itinerary logic).

2. Next.js & React Patterns

Modern frontend architecture examples using the App Router, Server Components, and Internationalization.

Key File: `react-components/hooks/useLanguageSwitcher.js`

Concepts: `useTransition`, `styled-components`, `next-intl`.

## 🛠️ Installation & Usage
To run these scripts locally, follow the instructions for each language environment.

Python Environment

Recommended for simulations and algorithms.

```Bash
# Clone the repository
git clone [https://github.com/your-username/blog-algorithms.git](https://github.com/your-username/blog-algorithms.git)

# Navigate to the folder
cd blog-algorithms

# Create a virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install requirements (if provided in specific folders)
pip install -r requirements.txt
```

### JavaScript/React Environment

Most React components are isolated snippets, but you can run them in a sandbox or integrate them into your Next.js project.
```Bash
# Navigate to a JS folder
cd react-components

# (Assuming a package.json exists for specific demos)
npm install
npm run dev
```
## 🤝 Contributing & Open Science
This repository follows Open Science principles. You are welcome to fork, audit the code, or propose improvements via Pull Requests.

Fork the Project

Create your Feature Branch (`git checkout -b feature/AmazingFeature`)

Commit your Changes (`git commit -m 'Add some AmazingFeature'`)

Push to the Branch (`git push origin feature/AmazingFeature`)

Open a Pull Request

## ⚖️ License
Distributed under the MIT License. See `LICENSE` for more information.