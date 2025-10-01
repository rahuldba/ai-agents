"""
CrewAI Runner: Generic utility to run any CrewAI agent and task.
"""
import logging

def run_agent_task(agent, task_prompt):
    """
    Runs a CrewAI agent with the given prompt/task.
    Args:
        agent: CrewAI Agent instance (already initialized with LLM and persona).
        task_prompt (str): The prompt or task description for the agent.
    Returns:
        str: Agent's response or error message.
    """
    try:
        if hasattr(agent, 'run'):
            return agent.run(task_prompt)
        elif hasattr(agent, 'kickoff'):
            return agent.kickoff(task_prompt)
        else:
            raise Exception("Agent does not support 'run' or 'kickoff' methods.")
    except Exception as e:
        logging.error(f"CrewAI runner error: {e}")
        return f"Error running agent: {e}"

# Example usage:
# from agents.unit_test_generator import SmartUnitTestGenerator
# agent = SmartUnitTestGenerator().agent
# result = run_agent_task(agent, "Your prompt here")
# print(result)
