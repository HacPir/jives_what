class Agent:
    """Base Agent class for the family connection system"""
    
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
        
    async def llm_call(self, prompt: str) -> str:
        """Base method for LLM calls - to be implemented by subclasses"""
        raise NotImplementedError("Subclasses must implement llm_call method") 