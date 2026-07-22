from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Sequence

from .io_utils import load_json
from .catalog_release import compile_catalog_release
from .warehouse import build_catalog
from .wikidata import sync_wikidata


def _print(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="antiquario-data", description="Pipeline local de dados do Antiquário")
    parser.add_argument("--data-dir", type=Path, default=Path("data"), help="raiz de dados do projeto")
    commands = parser.add_subparsers(dest="command", required=True)

    sync = commands.add_parser("sync", help="sincroniza uma fonte para staging")
    sync.add_argument("source", choices=["wikidata"])
    sync.add_argument("--limit", type=int, default=500)
    sync.add_argument("--fixture", type=Path)
    sync.add_argument("--retrieved-at", help="data ISO fixa, útil para fixtures reproduzíveis")

    build = commands.add_parser("build", help="publica o catálogo DuckDB e Parquet")
    build.set_defaults(command="build")

    all_command = commands.add_parser("all", help="sincroniza Wikidata e publica o catálogo")
    all_command.add_argument("--limit", type=int, default=500)
    all_command.add_argument("--fixture", type=Path)
    all_command.add_argument("--retrieved-at")

    commands.add_parser("status", help="exibe o manifesto do catálogo publicado")
    release = commands.add_parser("release", help="compila o catálogo compacto para a PWA")
    release.add_argument("--knowledge-dir", type=Path, default=Path("knowledge/compiled"))
    release.add_argument("--releases-dir", type=Path, default=Path("data/releases"))
    release.add_argument("--public-dir", type=Path, default=Path("apps/web/public/catalog"))
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = create_parser().parse_args(argv)
    data_directory: Path = args.data_dir.resolve()
    try:
        if args.command == "sync":
            result = sync_wikidata(
                data_directory,
                limit=args.limit,
                fixture=args.fixture.resolve() if args.fixture else None,
                retrieved_at=args.retrieved_at,
            )
            _print(result.as_dict())
        elif args.command == "build":
            _print(build_catalog(data_directory))
        elif args.command == "all":
            sync_result = sync_wikidata(
                data_directory,
                limit=args.limit,
                fixture=args.fixture.resolve() if args.fixture else None,
                retrieved_at=args.retrieved_at,
            )
            _print({"sync": sync_result.as_dict(), "catalog": build_catalog(data_directory)})
        elif args.command == "status":
            manifest_path = data_directory / "catalog" / "catalog-manifest.json"
            if not manifest_path.exists():
                raise FileNotFoundError("Catálogo ainda não foi publicado")
            _print(load_json(manifest_path))
        elif args.command == "release":
            result = compile_catalog_release(
                data_directory=data_directory,
                knowledge_directory=args.knowledge_dir.resolve(),
                releases_directory=args.releases_dir.resolve(),
                public_directory=args.public_dir.resolve(),
            )
            _print(result.as_dict())
        return 0
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        print(f"erro: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
