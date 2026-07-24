import json
import re
import pickle
from pathlib import Path

# Resolve paths relative to this file so CWD doesn't matter
_BASE = Path(__file__).parent.parent  # text-sql/
_SCHEMA_PATH = _BASE / "schema" / "schema.json"
_DATA_DIR = Path(__file__).parent / "data"  # text-sql/backend/data/

with open(_SCHEMA_PATH, "r", encoding="utf-8") as f:
    schema = json.load(f)


def build_search_text(table):
    sections = []
    # Table Information
    sections.append(f"Table:\n{table['table']}")

    # Optional high-level entity
    entity = table.get("entity")
    if entity:
        sections.append(f"Entity:\n{entity}")

    if table.get("description"):
        sections.append(f"Description:\n{table['description']}")

    if table.get("category"):
        sections.append(f"Category:\n{table['category']}")

    # Aliases
    aliases = table.get("aliases", [])
    if aliases:
        sections.append("Aliases:\n" + "\n".join(aliases))

    # Business Keywords
    keywords = table.get("business_keywords", [])
    if keywords:
        sections.append("Business Keywords:\n" + "\n".join(keywords))

    # Business Concepts
    concepts = table.get("business_concepts", [])
    if concepts:
        sections.append("Business Concepts:\n" + "\n".join(concepts))

    # Columns
    column_lines = []
    for col in table.get("columns", []):
        column_lines.append(f"{col['name']} ({col['type']})")
        if col.get("description"):
            column_lines.append(col["description"])
        samples = col.get("sample_values", [])
        if samples:
            column_lines.append("Sample Values:")
            column_lines.extend(samples)
        column_lines.append("")
    if column_lines:
        sections.append("Columns:\n" + "\n".join(column_lines))

    # Primary Keys
    primary_keys = table.get("primary_keys", [])
    if primary_keys:
        sections.append("Primary Keys:\n" + "\n".join(primary_keys))

    # Foreign Keys
    foreign_key_lines = []
    foreign_keys = table.get("foreign_keys", [])
    if foreign_keys:
        for fk in foreign_keys:
            foreign_key_lines.append(
                f"{fk['column']} -> "
                f"{fk['references_table']}."
                f"{fk['references_column']}"
            )
        sections.append("Foreign Keys:\n" + "\n".join(foreign_key_lines))
    else:
        sections.append("Foreign Keys:\nNone")

    # Relationships
    relationship_lines = []
    relationships = table.get("relationships", [])
    if relationships:
        for rel in relationships:
            relationship_lines.append(f"Related Table: {rel['target_table']}")
            relationship_lines.append(f"Relationship Type: {rel['type']}")
            if rel.get("foreign_key"):
                relationship_lines.append(f"Foreign Key: {rel['foreign_key']}")
            if rel.get("description"):
                relationship_lines.append(f"Description: {rel['description']}")
            relationship_lines.append("")
        sections.append("Relationships:\n" + "\n".join(relationship_lines))

    # Connected Tables
    related_tables = {rel["target_table"] for rel in relationships}
    if related_tables:
        sections.append("Connected Tables:\n" + "\n".join(sorted(related_tables)))

    return "\n\n".join(sections)


# Tokenizer
def tokenize(text):
    return re.findall(r"\b\w+\b", text.lower())


# Build documents and table names from schema
documents = []
table_names = []

for table in schema:
    documents.append(build_search_text(table))
    table_names.append(table["table"])

tokenized_documents = [tokenize(doc) for doc in documents]

# Persist artifacts (only when run as a script, not on import)
if __name__ == "__main__":
    _DATA_DIR.mkdir(parents=True, exist_ok=True)

    with open(_DATA_DIR / "table_names.pkl", "wb") as f:
        pickle.dump(table_names, f)

    with open(_DATA_DIR / "tokenized_docs.pkl", "wb") as f:
        pickle.dump(tokenized_documents, f)

    with open(_DATA_DIR / "documents.pkl", "wb") as f:
        pickle.dump(documents, f)

    print(f"Saved {len(table_names)} tables to {_DATA_DIR}")