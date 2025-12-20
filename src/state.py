from dataclasses import dataclass, field
from typing import Any, List, Dict

@dataclass
class PipelineState:
    """A centralized data container for the agent pipeline."""
    
    source_text: str = ""
    concepts: Dict[str, Any] = field(default_factory=dict)
    quiz: List[Dict[str, Any]] = field(default_factory=list)
    validation: List[Dict[str, Any]] = field(default_factory=list)
    
    def clear(self):
        """Resets the state for a new run."""
        self.source_text = ""
        self.concepts = {}
        self.quiz = []
        self.validation = []