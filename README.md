# ♟️ Chess Game with Toggleable AI (Python)

A fully playable **chess application built in Python** featuring a graphical user interface and a **toggleable AI opponent**. The project emphasizes **object-oriented design**, **game-state management**, and **AI decision-making**, while providing a clean, interactive player experience.

---

## 🚀 Features

- Complete chess ruleset:
  - Legal move validation
  - Check, checkmate, and stalemate detection
  - Turn-based gameplay
- **Toggleable AI opponent**
  - Play human vs. human or human vs. AI
  - AI can be enabled or disabled at runtime
- Graphical user interface built with **Pygame**
- Click-based piece selection and movement
- Visual feedback for selected pieces and valid moves
- Modular architecture separating game logic from rendering

---

## 🧠 AI Overview

The AI operates as an independent module and can be toggled on or off during gameplay.  
It evaluates board positions and selects moves based on:

- Legal move generation
- Board evaluation heuristics (material balance, positional value)
- Depth-limited search

This design allows the AI to be extended or replaced without modifying core game logic.

---

## 🛠️ Tech Stack

- **Language:** Python  
- **Libraries:**  
  - `pygame` – GUI rendering and input handling  
  - `math` / custom utilities – board evaluation & move logic  

---
