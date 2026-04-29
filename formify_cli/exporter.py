"""Exporter module for saving generated HTML forms to various output targets."""

import os
from pathlib import Path


class ExportError(Exception):
    """Raised when an export operation fails."""
    pass


def export_html(html: str, output_path: str, overwrite: bool = False) -> Path:
    """Write HTML content to a file at the given path.

    Args:
        html: The HTML string to write.
        output_path: Destination file path (will create parent dirs).
        overwrite: If False, raises ExportError when file already exists.

    Returns:
        The resolved Path of the written file.

    Raises:
        ExportError: If the file exists and overwrite is False, or on I/O failure.
    """
    if not html or not html.strip():
        raise ExportError("Cannot export empty HTML content.")

    path = Path(output_path)

    if path.exists() and not overwrite:
        raise ExportError(
            f"Output file already exists: '{path}'. Use overwrite=True to replace it."
        )

    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(html, encoding="utf-8")
    except OSError as exc:
        raise ExportError(f"Failed to write output file '{path}': {exc}") from exc

    return path.resolve()


def export_to_stdout(html: str) -> None:
    """Print HTML content to standard output.

    Args:
        html: The HTML string to print.

    Raises:
        ExportError: If html is empty.
    """
    if not html or not html.strip():
        raise ExportError("Cannot export empty HTML content.")
    print(html)


def get_output_path(schema_path: str, output_dir: str = ".") -> Path:
    """Derive a default output file path from the schema file name.

    Args:
        schema_path: Path to the source JSON schema file.
        output_dir: Directory in which to place the output file.

    Returns:
        A Path like '<output_dir>/<schema_stem>.html'.
    """
    stem = Path(schema_path).stem
    return Path(output_dir) / f"{stem}.html"
