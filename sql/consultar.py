"""Executa as cinco consultas do EP sobre o SQLite local, somente para leitura."""
import argparse
import sqlite3
from pathlib import Path

SQL_DIR = Path(__file__).resolve().parent


def execute_all(database):
    connection = sqlite3.connect(f"{Path(database).resolve().as_uri()}?mode=ro", uri=True)
    try:
        for path in sorted(SQL_DIR.glob("*.sql")):
            sql = path.read_text(encoding="utf-8")
            cursor = connection.execute(sql)
            yield path.stem, sql, [column[0] for column in cursor.description], cursor.fetchall()
    finally:
        connection.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database", nargs="?", default=SQL_DIR.parent / "db.sqlite3")
    args = parser.parse_args()
    for name, sql, headers, rows in execute_all(args.database):
        print(f"\n{name}\n{sql.strip()}")
        print(" | ".join(headers))
        for row in rows:
            print(" | ".join(str(value) for value in row))
        print(f"{len(rows)} registro(s)")
