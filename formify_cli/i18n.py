"""Internationalization support for formify-cli form labels and messages."""

from __future__ import annotations

from typing import Dict, Optional

I18N_CATALOG: Dict[str, Dict[str, str]] = {
    "en": {
        "required_marker": "*",
        "required_legend": "Fields marked with * are required.",
        "submit_button": "Submit",
        "error_required": "This field is required.",
        "error_invalid_email": "Please enter a valid email address.",
        "error_min_length": "Must be at least {min} characters.",
        "error_max_length": "Must be no more than {max} characters.",
    },
    "fr": {
        "required_marker": "*",
        "required_legend": "Les champs marqués d'un * sont obligatoires.",
        "submit_button": "Envoyer",
        "error_required": "Ce champ est obligatoire.",
        "error_invalid_email": "Veuillez saisir une adresse e-mail valide.",
        "error_min_length": "Doit comporter au moins {min} caractères.",
        "error_max_length": "Ne doit pas dépasser {max} caractères.",
    },
    "es": {
        "required_marker": "*",
        "required_legend": "Los campos marcados con * son obligatorios.",
        "submit_button": "Enviar",
        "error_required": "Este campo es obligatorio.",
        "error_invalid_email": "Por favor, introduce una dirección de correo válida.",
        "error_min_length": "Debe tener al menos {min} caracteres.",
        "error_max_length": "No debe superar {max} caracteres.",
    },
    "de": {
        "required_marker": "*",
        "required_legend": "Mit * markierte Felder sind Pflichtfelder.",
        "submit_button": "Absenden",
        "error_required": "Dieses Feld ist erforderlich.",
        "error_invalid_email": "Bitte geben Sie eine gültige E-Mail-Adresse ein.",
        "error_min_length": "Muss mindestens {min} Zeichen lang sein.",
        "error_max_length": "Darf höchstens {max} Zeichen lang sein.",
    },
}


class I18NError(Exception):
    """Raised when an i18n locale or key is invalid."""


def list_locales() -> list[str]:
    """Return all supported locale codes."""
    return sorted(I18N_CATALOG.keys())


def get_locale(locale: str) -> Dict[str, str]:
    """Return the translation map for the given locale code.

    Raises I18NError if the locale is not supported.
    """
    key = locale.lower().strip()
    if key not in I18N_CATALOG:
        available = ", ".join(list_locales())
        raise I18NError(
            f"Unsupported locale '{locale}'. Available locales: {available}."
        )
    return dict(I18N_CATALOG[key])


def translate(key: str, locale: str = "en", **kwargs: str) -> str:
    """Return the translated string for *key* in *locale*.

    Extra keyword arguments are used for format substitution.
    Falls back to English if the key is missing in the requested locale.
    """
    catalog = get_locale(locale)
    fallback = I18N_CATALOG.get("en", {})
    template = catalog.get(key) or fallback.get(key, key)
    try:
        return template.format(**kwargs)
    except KeyError:
        return template


def apply_locale_to_schema(schema: dict, locale: str = "en") -> dict:
    """Inject locale-aware submit label and required legend into *schema*.

    Returns a shallow-copied schema dict with i18n keys added.
    """
    catalog = get_locale(locale)
    patched = dict(schema)
    patched.setdefault("submit_label", catalog["submit_button"])
    patched.setdefault("required_legend", catalog["required_legend"])
    patched["_locale"] = locale.lower().strip()
    return patched
