<<<<<<< HEAD
# CONXENSEVE: Synergistic AI Code Generation

**CONXENSEVE** (Consensus LLM Agent - Codename: EVE-Enhancer) is a cutting-edge prototype designed as a core component for our AI Agent Ecosystem (led by EVE). Its primary mission is to **empower fully autonomous operation and self-improvement** by leveraging the collective intelligence of multiple leading Large Language Models (LLMs) for complex code generation tasks.

## The Challenge: Limits of Singular AI

Even the most advanced individual LLMs possess unique strengths and weaknesses. Relying on a single model for critical autonomous tasks limits robustness, introduces potential biases, and caps the potential for creative problem-solving.

## The Solution: Collective Consensus

CONXENSEVE tackles this by orchestrating a dynamic, multi-stage collaboration between diverse LLMs:

1.  🚀 **Generation Phase:** Multiple expert LLMs independently propose initial solutions to a given coding challenge.
2.  💡 **Revision Phase:** Each AI reviews all proposals and intelligently refines *its own* solution, guided by specialized instructions that harness its unique strengths (e.g., syntactic precision, architectural insight, novel optimizations).
3.  🗳️ **Consensus Phase:** The models collaboratively evaluate the revised solutions, vote for the most promising candidate(s), and a designated Consolidator LLM synthesizes and polishes the final output.

> **CONXENSEVE is engineered for scenarios demanding the absolute highest levels of accuracy, robustness, and code quality. It aims to transcend the capabilities of any single AI by creating a synergistic effect, driving the ecosystem towards more effective and autonomous self-development.**

## Strategic Purpose within the Ecosystem

*   **Autonomous Enhancement:** Provide EVE and the wider agent system with a superior tool for high-fidelity, autonomous code generation and modification.
*   **Accelerated Self-Improvement:** Enable the ecosystem to learn and evolve more rapidly by integrating insights from multiple AI perspectives.
*   **Foundation for ASINGULARITY.AI:** Serve as a critical testbed and demonstrator for advanced AI collaboration, underpinning the development of our core projects.
*   **Pushing Boundaries:** Validate the power of consensus mechanisms to achieve breakthrough results in complex AI domains.

## MVP Status

The current version is a functional command-line Python script (`main.py`) implementing the core 3-step logic using models accessed via the OpenRouter API.

## Getting Started

### Using Docker (Recommended)

1. **Clone the repository.**
2. **Create a `.env` file** in the root directory with your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=your_key_here
   ```
   *Note: You can copy the `.env.example` file to `.env` and replace the placeholder value.*
3. **Build and run the Docker container:**
   ```bash
   docker compose up --build
   ```
   This will build the Docker image and start the container. The script will prompt you to enter a coding task directly in the terminal.

### Manual Setup (Alternative)

1. **Clone the repository.**
2. **Create a `.env` file** as described above.
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the script:**
   ```bash
   python main.py
   ```
   The script will prompt you to enter a coding task.

## Memory Bank

Project context, technical details, and progress are tracked in the `memory-bank/` directory, following Cursor's Memory Bank standard.
=======
# CONXENSEVE
Multi-LLM Consensus: The core engine for advanced AI agent autonomy.
>>>>>>> 3ad3eb547aa11b5249d538921b899f44d6f297c6
