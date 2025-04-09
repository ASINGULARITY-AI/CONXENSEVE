import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure OpenAI client for OpenRouter
client = openai.OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)

# Define the models to be used
MODELS = {
    "generator1": "anthropic/claude-3.7-sonnet:thinking",
    "generator2": "google/gemini-2.5-pro-exp-03-25:free",
    "generator3": "deepseek/deepseek-r1",
    "consolidator": "anthropic/claude-3.7-sonnet"
}

def call_llm(model_name: str, prompt: str, system_prompt: str = "You are a helpful AI assistant specializing in coding.") -> str:
    """
    Calls the specified LLM via OpenRouter.

    Args:
        model_name: The name of the model as defined in the MODELS dictionary key or OpenRouter identifier.
        prompt: The user prompt.
        system_prompt: The system prompt to guide the model's behavior.

    Returns:
        The content of the LLM's response, or an error message.
    """
    try:
        print(f"--- Calling {model_name} ---") # Debug print
        model_identifier = MODELS.get(model_name, model_name) # Use dict key or direct identifier
        
        response = client.chat.completions.create(
            model=model_identifier,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt},
            ],
            # Add other parameters like temperature if needed
        )
        content = response.choices[0].message.content
        print(f"--- Response from {model_name} received ---") # Debug print
        return content.strip() if content else ""
    except openai.APIError as e:
        print(f"Error calling {model_name}: {e}")
        return f"Error: {e}"
    except Exception as e:
        print(f"An unexpected error occurred with {model_name}: {e}")
        return f"Unexpected Error: {e}"

def run_consensus_agent(user_prompt: str):
    """
    Runs the 3-step consensus process for the given user prompt.

    Args:
        user_prompt: The initial prompt from the user.
    """
    print(f"\n=== Starting Consensus Process for Prompt: ===\n{user_prompt}\n")

    # --- Step 1: Generation ---
    print("\n=== Step 1: Generating Initial Responses ===")
    initial_responses = {}
    for i, model_key in enumerate(["generator1", "generator2", "generator3"], 1):
        # Simple system prompt for initial generation
        system_p = "You are an expert AI programmer. Generate the best possible code for the following request."
        response = call_llm(model_key, user_prompt, system_p)
        initial_responses[f"R{i}_1"] = response
        print(f"\nResponse from {MODELS[model_key]} (R{i}_1):\n{response}\n" + "-"*20)

    # --- Step 2: Revision ---
    print("\n=== Step 2: Revising Responses ===")
    revised_responses = {}
    
    # Prepare context for revision prompts
    r1_1 = initial_responses["R1_1"]
    r2_1 = initial_responses["R2_1"]
    r3_1 = initial_responses["R3_1"]

    # TODO: Implement specific prompts for each model based on the plan
    # TODO: Add context limit check for DeepSeek if necessary (MVP: skip check)

    # Example placeholder prompt for revision (needs refinement per model)
    revision_prompt_template = f"""
    Original Task: {user_prompt}

    Initial Solutions Provided:
    [1: Claude 3.7 Sonnet Thinking]
    {r1_1}

    [2: Gemini 2.5 Pro Exp]
    {r2_1}

    [3: DeepSeek R1]
    {r3_1}

    Your initial solution was number {{model_index}}. 
    Analyze all solutions. Focus on {{focus_area}}.
    Create your improved version of the code/solution. Output only the improved code/solution.
    """

    model_prompts = {
        "generator1": revision_prompt_template.format(model_index=1, focus_area="syntax, readability, and elegance"),
        "generator2": revision_prompt_template.format(model_index=2, focus_area="overall architecture, efficiency, and completeness, leveraging your large context"),
        "generator3": revision_prompt_template.format(model_index=3, focus_area="alternative approaches, non-obvious optimizations, and thoroughness")
    }
    
    system_p_revision = "You are an expert AI programmer participating in a multi-stage review process to refine a code solution."

    for i, model_key in enumerate(["generator1", "generator2", "generator3"], 1):
        prompt_for_revision = model_prompts[model_key]
        # print(f"\n--- Revision Prompt for {MODELS[model_key]} ---\n{prompt_for_revision[:500]}...\n" + "-"*10) # Debug: print start of prompt
        response = call_llm(model_key, prompt_for_revision, system_p_revision)
        revised_responses[f"R{i}_2"] = response
        print(f"\nRevised Response from {MODELS[model_key]} (R{i}_2):\n{response}\n" + "-"*20)


    # --- Step 3: Voting and Consolidation ---
    print("\n=== Step 3: Voting and Consolidation ===")
    votes = {}
    
    # Prepare context for voting
    r1_2 = revised_responses["R1_2"]
    r2_2 = revised_responses["R2_2"]
    r3_2 = revised_responses["R3_2"]

    # TODO: Implement voting prompt
    # TODO: Add context limit check for DeepSeek if necessary (MVP: skip check)

    voting_prompt_template = f"""
    Original Task: {user_prompt}

    Three revised solutions are proposed:
    [1: Claude's Revision]
    {r1_2}

    [2: Gemini's Revision]
    {r2_2}

    [3: DeepSeek's Revision]
    {r3_2}

    Based on your expertise ({{expertise}}), which solution (1, 2, or 3) is the best overall?
    Respond with ONLY the number (1, 2, or 3) followed by a brief justification (max 2 sentences).
    Example: 1 - This solution is the most elegant and robust.
    """

    vote_prompts = {
         "generator1": voting_prompt_template.format(expertise="syntax, readability, elegance"),
         "generator2": voting_prompt_template.format(expertise="overall architecture, efficiency, completeness"),
         "generator3": voting_prompt_template.format(expertise="alternative approaches, non-obvious optimizations, thoroughness")
    }
    
    system_p_voting = "You are an expert AI programmer acting as a judge in a code review process. Evaluate the provided solutions objectively based on your specific expertise."

    for i, model_key in enumerate(["generator1", "generator2", "generator3"], 1):
        prompt_for_voting = vote_prompts[model_key]
        # print(f"\n--- Voting Prompt for {MODELS[model_key]} ---\n{prompt_for_voting[:500]}...\n" + "-"*10) # Debug: print start of prompt
        vote_response = call_llm(model_key, prompt_for_voting, system_p_voting)
        votes[f"V{i}"] = vote_response
        print(f"\nVote from {MODELS[model_key]} (V{i}):\n{vote_response}\n" + "-"*20)

    # --- Process Votes ---
    # TODO: Implement robust vote parsing and winner determination
    # Simple parsing for MVP: assumes format "N - justification"
    vote_counts = {1: 0, 2: 0, 3: 0}
    try:
        for vote_str in votes.values():
            if vote_str and vote_str[0].isdigit():
                choice = int(vote_str[0])
                if choice in vote_counts:
                    vote_counts[choice] += 1
    except Exception as e:
        print(f"Error processing votes: {e}")
        # Handle error - maybe default to one model or ask user? For MVP, maybe pick R1_2.
        pass

    print(f"\nVote Counts: {vote_counts}")
    
    winning_choice = 0
    max_votes = 0
    winners = []
    for choice, count in vote_counts.items():
        if count > max_votes:
            max_votes = count
            winners = [choice]
        elif count == max_votes:
            winners.append(choice)

    if len(winners) == 1:
        winning_choice = winners[0]
        winning_response = revised_responses[f"R{winning_choice}_2"]
        print(f"\nWinning Choice: #{winning_choice}")
    elif len(winners) > 1:
         # Handle ties - For MVP, maybe pick the first winner (e.g., Claude's if 1 is tied)
         winning_choice = winners[0] 
         winning_response = revised_responses[f"R{winning_choice}_2"]
         print(f"\nTie between choices: {winners}. Selecting #{winning_choice} for consolidation.")
         # Potentially list all tied responses for consolidator?
         # winning_response = "\n---\n".join([revised_responses[f"R{w}_2"] for w in winners]) # Alternative for ties
    else:
        # No clear winner / error in voting? Fallback (e.g., use Claude's revised)
        print("\nWarning: No clear winner from votes. Using Claude's revised response as fallback.")
        winning_choice = 1 
        winning_response = revised_responses["R1_2"]


    # --- Consolidate ---
    # TODO: Implement consolidation prompt
    
    consolidation_prompt = f"""
    Original Task: {user_prompt}

    Based on a review and voting process by multiple AI experts, the following solution (number {winning_choice}) was selected as the best:
    --- SOLUTION START ---
    {winning_response}
    --- SOLUTION END ---
    
    Your task is to take this selected solution, ensure its correctness and completeness, polish the syntax, and present the final, ready-to-use code. 
    Output ONLY the final code. Do not include explanations, comments about the process, or markdown formatting around the code block unless the requested output itself is markdown.
    """

    system_p_consolidate = "You are an AI assistant whose sole job is to finalize and polish a pre-selected code solution. Output only the code."
    
    final_response = call_llm("consolidator", consolidation_prompt, system_p_consolidate)

    print(f"\n\n=== Final Consolidated Response ===\n{final_response}")

    # Return intermediate steps as well for analysis?
    return {
        "final_response": final_response,
        "step1_responses": initial_responses,
        "step2_responses": revised_responses,
        "step3_votes": votes
    }


if __name__ == "__main__":
    # Example Usage
    # Ensure you have a .env file with your OPENROUTER_API_KEY
    if not os.getenv("OPENROUTER_API_KEY"):
        print("Error: OPENROUTER_API_KEY not found in environment variables.")
        print("Please create a .env file with OPENROUTER_API_KEY=your_key")
    else:
        # test_prompt = "Write a simple Python function to calculate the factorial of a number using recursion."
        test_prompt = input("Enter your coding prompt: ")
        results = run_consensus_agent(test_prompt)
        # print(results) # Optionally print the full dictionary 