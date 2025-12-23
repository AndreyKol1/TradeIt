from pydantic import BaseModel, Field

class AgentOutput(BaseModel):
    reasoning: str = Field(description="Explanation of analysis")
    signal: str = Field(description="BUY, SELL or hold signal")
    score: float = Field(description="Score from 0.0 to 1.0")
    confidence: str = Field(description="LOW MEDIUM or HIGH confidence of decision")
