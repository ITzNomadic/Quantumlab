"""
Internationalization (i18n) Manager for QuantumLab.
Handles language selection, dictionary lookup, config persistence,
and real-time notification to registered GUI and formatting components.
"""

import os
import json
from typing import Dict, Any, Callable, List, Optional

from .es import STRINGS_ES
from .en import STRINGS_EN

TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "es": STRINGS_ES,
    "en": STRINGS_EN,
}

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".quantumlab")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")


class I18NManager:
    SUPPORTED_LANGUAGES = ["es", "en"]
    DEFAULT_LANGUAGE = "es"

    def __init__(self):
        self._current_language: str = self._load_saved_preference()
        self._listeners: List[Callable[[str], None]] = []

    def _load_saved_preference(self) -> str:
        """Loads saved language preference from user config directory."""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    lang = data.get("language")
                    if lang in self.SUPPORTED_LANGUAGES:
                        return lang
        except Exception:
            pass
        return self.DEFAULT_LANGUAGE

    def _save_preference(self, lang: str) -> None:
        """Saves language preference safely without writing to repo."""
        try:
            os.makedirs(CONFIG_DIR, exist_ok=True)
            config = {}
            if os.path.exists(CONFIG_FILE):
                try:
                    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                        config = json.load(f)
                except Exception:
                    config = {}
            config["language"] = lang
            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    @property
    def current_language(self) -> str:
        return self._current_language

    def set_language(self, lang: str) -> None:
        """Switches the active language, persists the choice and notifies listeners."""
        if lang not in self.SUPPORTED_LANGUAGES:
            raise ValueError(f"Unsupported language: {lang}. Must be one of {self.SUPPORTED_LANGUAGES}")
        if lang == self._current_language:
            return

        self._current_language = lang
        self._save_preference(lang)

        # Notify UI and components
        for listener in list(self._listeners):
            try:
                listener(lang)
            except Exception:
                pass

    def add_listener(self, listener: Callable[[str], None]) -> None:
        """Registers a callback function to be called when language changes."""
        if listener not in self._listeners:
            self._listeners.append(listener)

    def remove_listener(self, listener: Callable[[str], None]) -> None:
        """Unregisters a language change callback."""
        if listener in self._listeners:
            self._listeners.remove(listener)

    def get_text(self, key: str, lang: Optional[str] = None, **kwargs) -> str:
        """
        Retrieves a translated string by key with fallback to DEFAULT_LANGUAGE.
        Supports formatting kwargs and optional explicit language override.
        """
        target_lang = lang if lang in self.SUPPORTED_LANGUAGES else self._current_language
        lang_dict = TRANSLATIONS.get(target_lang, STRINGS_ES)
        text = lang_dict.get(key)
        if text is None:
            # Fallback to default
            text = STRINGS_ES.get(key, key)

        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text

    def t(self, key: str, lang: Optional[str] = None, **kwargs) -> str:
        """Shorthand alias for get_text."""
        return self.get_text(key, lang=lang, **kwargs)


# Global singleton manager instance
_default_manager: Optional[I18NManager] = None


def get_i18n() -> I18NManager:
    global _default_manager
    if _default_manager is None:
        _default_manager = I18NManager()
    return _default_manager


def t(key: str, lang: Optional[str] = None, **kwargs) -> str:
    """Convenience global translation function."""
    return get_i18n().get_text(key, lang=lang, **kwargs)
