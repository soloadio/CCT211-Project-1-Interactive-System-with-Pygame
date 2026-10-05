# Pygame Interactive Application: Assignment Instructions

**Worth:** 100 points (20% of course grade)
**Size:** Roughly the same as 3 labs, extending your lab work
**Deliverable:** Source code zipped with any supporting resources (images, database files, etc.)

## Goal

Design and build an interactive, data-driven 2D application with Pygame. It should be a focused "tech demo" such as a sandbox, a design tool, or a micro-game. If you build a game, polish specific components with good practices rather than building something huge. You don't need to make a shooter.

Keep your **data model**, **rendering pipeline**, and **user interface** cleanly separated.

## Learning Goals

1. Understand event-based user interaction loops and event handlers.
2. Learn GUI fundamentals, including appropriate widgets and animation.

## Requirements Checklist

### 1. Object-Oriented Entities
- [ ] Design a class hierarchy for the things on screen.
- [ ] Use Pygame classes such as `Sprite` and inherit from them appropriately.
- [ ] Have **at least three distinct object hierarchies**.
- [ ] Every entity has its own class.

### 2. Event Handling
- [ ] The app responds fluidly, without freezing or dropping events.
- [ ] **Discrete events** are handled (e.g. a button to pause).
- [ ] **Continuous inputs** are handled (e.g. holding the mouse to drag, or holding a key to apply a force).

### 3. Application State
- [ ] Don't run everything in one massive loop.
- [ ] Use state management with clear transitions between states.
- [ ] Objects created in one state are cleaned up properly on transition.

### 4. Dynamic Data
- [ ] There is an underlying data model that changes over time, not only on clicks.
- [ ] Variables update from both user interaction and the passage of time.
- [ ] Time-based updates use **delta_time**, not just frame rate (e.g. decaying physics variables, or a tile grid that updates as the user paints).

### 5. Interaction
- [ ] A moderate amount of visible complexity.
- [ ] Objects that **move over time** on their own.
- [ ] Objects that **move or transform in reaction to the user**.
- [ ] **Collisions** between objects (obstacles, screen edges, etc.).

### 6. Modular Code Delivery
- [ ] Code is split into logical modules (e.g. `states.py`, `entities.py`, `character.py`), not one big `main.py`.

## Assets

- Art creation is **not** evaluated.
- Use open-source images from the internet and **cite them** (source, author, license).

## Academic Integrity (Important)

- **No generative AI may be used to produce code for this assignment.** Detected use counts as academic misconduct.
- Do not copy code from existing Pygame projects online.
- If you learn a technique from somewhere, **cite it in a code comment** (where you saw it).
- If you're unsure where learning a technique ends and plagiarism begins, talk to the instructor.

## Submission

1. Make sure the project runs from a clean folder.
2. Include all assets and resource files.
3. Include a README documenting how to run it, controls, structure, and credits.
4. Zip everything and submit.

## Final Self-Check

- [ ] 3+ class hierarchies using `Sprite` inheritance
- [ ] Discrete and continuous input both work
- [ ] Multiple states with clean transitions and cleanup
- [ ] Movement and updates are `delta_time`-based
- [ ] Moving objects, user-driven changes, and collisions are all visible
- [ ] Multiple modules, one class per entity
- [ ] All assets and borrowed techniques cited
- [ ] No AI-generated code