"""3cerebros — um cérebro de IA com 3 cérebros (Projeto / Self / Conhecimento).

Repo isolado e embutível: qualquer host incorpora o `Brain` via repo.

    from cerebros import Brain
    brain = Brain("~/.cerebros")
"""
from .brain import Brain
from .interview import Interview
from .memory import Memory
from .policy import Policy
from .triage import triage

__version__ = "0.2.0"
__all__ = ["Brain", "Interview", "Memory", "Policy", "triage", "__version__"]
