# Technical Context: CONXENSEVE

## 1. Core Technologies

*   **Language:** Python 3.11 (specified in Dockerfile)
*   **LLM Interaction:** `openai` Python library
*   **LLM Provider:** OpenRouter (API)
*   **Configuration:** `python-dotenv` for API key management (`.env` file, used by Docker Compose)
*   **Containerization:** Docker, Docker Compose
*   **Environment:** Docker container based on `python:3.11-slim`. Dependencies installed via `requirements.txt` during image build.

## 2. Specific LLM Models (MVP)

*   **Generators/Revisers/Voters (Step 1, 2, 3-Vote):**
    *   `anthropic/claude-3.7-sonnet:thinking` (Designated "generator1", focused on syntax/elegance)
    *   `google/gemini-2.5-pro-exp-03-25:free` (Designated "generator2", focused on context/completeness)
    *   `deepseek/deepseek-r1` (Designated "generator3", focused on alternatives/optimization)
*   **Consolidator (Step 3-Consolidate):**
    *   `anthropic/claude-3.7-sonnet` (Standard version for cost-effective polishing)

## 3. API Integration

*   Uses OpenRouter's OpenAI-compatible endpoint: `https://openrouter.ai/api/v1`
*   Requires an `OPENROUTER_API_KEY` environment variable (set in `.env`).
*   Standard Chat Completions API (`client.chat.completions.create`) is used for all calls.

## 4. Key Dependencies

*   `openai`: For API calls.
*   `python-dotenv`: For loading `.env` file.

## 5. Technical Constraints & Considerations

*   **API Costs:** Calls to multiple powerful models can be expensive. Monitor usage via OpenRouter dashboard.
*   **Latency:** Multi-step process involving multiple API calls will inherently have higher latency than a single call.
*   **Context Limits:**
    *   `deepseek/deepseek-r1` has a stated context limit (around 168k tokens). Prompts involving multiple large code responses might exceed this.
    *   MVP currently does *not* actively manage context limits; large inputs *may* cause errors with DeepSeek on Steps 2 & 3.
    *   Future versions may need context truncation or summarization strategies for DeepSeek.
*   **Model Availability/Changes:** Relies on specific models being available via OpenRouter. Model identifiers or availability might change.
*   **Error Handling:** Basic error handling for API calls is implemented, but complex failure scenarios (e.g., malformed votes) have simple fallbacks in MVP. 