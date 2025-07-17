# 🐍 Snake Game – Machine Learning with Weka

> ⚠️ **Note**: This project was developed as part of my coursework during the first year of my **Data Science & Engineering** degree. It represents an early exploration of applying machine learning concepts in practice.

## 🧠 Project Overview

This project applies **Machine Learning methodologies** to the classic **Snake game**, using the Weka platform for data analysis and modeling. The core objectives include:

- Developing predictive and classification models based on gameplay data.
- Constructing an **autonomous agent** that can control the snake intelligently using the trained models.

Through this project, we explored how traditional ML techniques can be adapted to real-time decision-making in games.

### 🐍 Game Implementation

- `SnakeGame.py`: Basic Snake game logic
- `SnakeGame_intelligent_agent.py`: Integrates Weka predictions to automate snake behavior
- `wekaI.py`: Interface with Weka classifiers
- `Prediction-Classification/Datasets/`: Contains ARFF-formatted data for training models
- `Report/`: Contains the full report for this phase

📄 [Click here to read the Prediction/Classification report](Prediction-Classification/Report/MLI___Assignment_I.pdf)

---

## 🔁 Second Activity: Q-Learning Agent (Phase 2 & 3)

In the second phase of the course, we implemented a **Reinforcement Learning agent** using the **Q-learning algorithm**. This agent:

- Learns to chase food while avoiding its own body
- Is trained via trial-and-error using Q-values
- Aims to maximize the score over many episodes

📂 You can find this part of the project in the [`Q-Learning/`](./Q-Learning/) folder, including:
- `Phase 2/`: Initial Q-learning implementation
- `Phase 3/`: Extended/optimized version
- `Report/`: Project documentation for this phase

📄 [Click here to read the Q-Learning report](Q-Learning/Report/MLI___Assignment_II.pdf)

---

## 📌 Summary of Techniques

| Phase              | Methodology         | Tools Used | Description                              |
|--------------------|---------------------|-------------|------------------------------------------|
| Prediction-Classification | Supervised ML        | Weka        | Build a model to guide the snake using predictions |
| Q-Learning         | Reinforcement Learning | Python (custom) | Train an agent that learns through rewards |

---

## 👩‍💻 Made by

[![GitHub](https://img.shields.io/badge/GitHub-Raqueljadel-181717?logo=github&style=flat-square)](https://github.com/Raqueljadel)


