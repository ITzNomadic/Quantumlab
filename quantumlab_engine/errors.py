"""
Structured exception hierarchy for QuantumLab.
Provides stable error codes, structured parameters, and non-destructive localization.
Addresses DEF-01 by eliminating hardcoded error strings and decoupling error reporting
from any specific language.
"""

from typing import Optional, Dict, Any


class QuantumLabError(ValueError):
    """
    Base class for all scientific, mathematical, and parser errors in QuantumLab.
    Inherits from ValueError for 100% backward compatibility with existing exception handlers.
    """
    def __init__(self, code: str, **params):
        self.code = code
        self.params = params
        # Default message in current language (or Spanish if i18n not initialized yet)
        super().__init__(self._render(None))

    def _render(self, lang: Optional[str] = None) -> str:
        try:
            from quantumlab_i18n import t
            return t(self.code, lang=lang, **self.params)
        except Exception:
            return f"[{self.code}] {self.params}"

    def to_localized(self, lang: Optional[str] = None) -> str:
        """Returns the translated error message for the requested or currently active language."""
        return self._render(lang)

    def __str__(self) -> str:
        try:
            from quantumlab_i18n import get_i18n
            return self._render(get_i18n().current_language)
        except Exception:
            return self._render(None)


class MathParseError(QuantumLabError):
    """Raised when mathematical syntax, tokens, or grammar are invalid."""
    pass


class ParseSecurityError(MathParseError):
    """Raised when an expression violates AST whitelist or security restrictions."""
    pass


class ScientificValidationError(QuantumLabError):
    """Raised when physical bounds, quantum state requirements, or invariants are violated."""
    pass
