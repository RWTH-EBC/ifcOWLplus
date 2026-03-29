import logging
from pathlib import Path

from graphDBdrivers.graphDB import GraphDBClient


def _format_sparql_value(v: dict | None) -> str:
    """Formatiert ein einzelnes SPARQL-JSON-Binding zu einem lesbaren String.

    Erwartete Shapes (GraphDB/SPARQL JSON):
      - {"type": "literal", "value": "...", "datatype": "..."?, "xml:lang": "..."?}
      - {"type": "uri", "value": "http://..."}
      - {"type": "bnode", "value": "..."}
    """
    if not v:
        return ""

    v_type = v.get("type")
    value = v.get("value", "")

    if v_type == "uri":
        # Keep it compact: prefer last fragment/segment.
        if isinstance(value, str):
            return value.rsplit("#", 1)[-1].rsplit("/", 1)[-1]
        return str(value)

    if v_type == "bnode":
        return f"_:{value}"

    # literal or unknown
    if not isinstance(value, str):
        value = str(value)

    lang = v.get("xml:lang")
    dt = v.get("datatype")
    if lang:
        return f"{value}@{lang}"
    if dt:
        dt_short = str(dt).rsplit("#", 1)[-1].rsplit("/", 1)[-1]
        return f"{value}^^{dt_short}"
    return value


def _sparql_json_to_rows(res: dict) -> tuple[list[str], list[list[str]]]:
    """Konvertiert SPARQL-JSON (head/results) in (headers, rows)."""
    head = (res or {}).get("head") or {}
    headers = head.get("vars") or []

    bindings = (((res or {}).get("results") or {}).get("bindings")) or []

    # Fallback: falls head.vars fehlt, unioniere Keys aus den Bindings.
    if not headers:
        all_keys: set[str] = set()
        for b in bindings:
            if isinstance(b, dict):
                all_keys.update(b.keys())
        headers = sorted(all_keys)

    rows: list[list[str]] = []
    for b in bindings:
        if not isinstance(b, dict):
            continue
        row = [_format_sparql_value(b.get(h)) for h in headers]
        rows.append(row)

    return headers, rows


def print_sparql_result_table(res: dict, *, max_col_width: int = 80) -> None:
    """Druckt das Ergebnis einer SPARQL-SELECT Query als einfache ASCII-Tabelle."""
    headers, rows = _sparql_json_to_rows(res)

    if not headers:
        print("(keine Variablen im Ergebnis)")
        return

    if not rows:
        print("(0 Treffer)")
        return

    # Column widths (capped)
    widths = [len(h) for h in headers]
    for r in rows:
        for i, cell in enumerate(r):
            cell = cell if cell is not None else ""
            widths[i] = min(max(widths[i], len(cell)), max_col_width)

    def clip(s: str, w: int) -> str:
        s = s or ""
        if len(s) <= w:
            return s
        if w <= 1:
            return s[:w]
        return s[: max(0, w - 1)] + "…"

    def fmt_row(r: list[str]) -> str:
        parts = []
        for i, cell in enumerate(r):
            c = clip(str(cell or ""), widths[i])
            parts.append(c.ljust(widths[i]))
        return "| " + " | ".join(parts) + " |"

    sep = "+-" + "-+-".join("-" * w for w in widths) + "-+"

    print(sep)
    print(fmt_row(headers))
    print(sep)
    for r in rows:
        print(fmt_row(r))
    print(sep)
    print(f"({len(rows)} Treffer)")


def load_sparql_query(query_file: str | Path, *, base_dir: str | Path | None = None) -> str:
    """Lädt eine SPARQL-Query aus einer Datei.

    - query_file: Dateiname oder Pfad
    - base_dir: falls gesetzt und query_file relativ ist, wird relativ zu base_dir aufgelöst

    Wir nutzen UTF-8, damit Prefixe/Kommentare etc. sauber funktionieren.
    """
    p = Path(query_file)
    if not p.is_absolute():
        base = Path(base_dir) if base_dir is not None else Path(__file__).resolve().parent
        p = (base / p).resolve()
    return p.read_text(encoding="utf-8")


if __name__ == "__main__":

    client = GraphDBClient(
        base_url="http://137.226.248.187:7200", repository_id="mbe-custom-ruleset"
    )
    client.logger.setLevel(logging.INFO)

    query_text = load_sparql_query("taskC.sparql")

    res = client.execute_sparql_query(query_text)

    print_sparql_result_table(res)
