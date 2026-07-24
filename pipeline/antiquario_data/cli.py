from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Sequence

from .io_utils import load_json
from .catalog_release import compile_catalog_release
from .curation_queue import build_curation_queue
from .official_pdf import process_official_pdf
from .warehouse import build_catalog
from .wikidata import audit_wikidata_properties, audit_wikidata_property_values, sync_wikidata


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
    sync.add_argument(
        "--discovery-country",
        action="append",
        default=[],
        metavar="QID",
        help="QID de país para uma busca factual adicional; pode ser repetido",
    )

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
    curation = commands.add_parser("curation-queue", help="gera rascunhos factuais para curadoria editorial")
    curation.add_argument("--limit", type=int, default=25)
    curation.add_argument("--vault-dir", type=Path, default=Path("knowledge/vault"))
    curation.add_argument("--release-dir", type=Path, default=Path("apps/web/public/catalog"))
    curation.add_argument("--report", type=Path, default=Path("data/curation/curation-queue.json"))
    audit = commands.add_parser("wikidata-audit", help="audita propriedades Wikidata presentes no catálogo factual")
    audit.add_argument("--output", type=Path, default=Path("data/staging/wikidata/property-audit.json"))
    audit.add_argument("--batch-size", type=int, default=100)
    audit.add_argument("--retrieved-at", help="data ISO fixa, útil para auditorias reproduzíveis")
    values_audit = commands.add_parser("wikidata-values-audit", help="audita valores das propriedades semânticas do Wikidata")
    values_audit.add_argument("--output", type=Path, default=Path("data/staging/wikidata/property-values-audit.json"))
    values_audit.add_argument("--property", action="append", default=[], metavar="PID")
    values_audit.add_argument("--batch-size", type=int, default=100)
    values_audit.add_argument("--retrieved-at", help="data ISO fixa, útil para auditorias reproduzíveis")

    official_pdf = commands.add_parser("official-pdf", help="ingere catálogo oficial em PDF e gera staging")
    official_pdf.add_argument("--input", type=Path, required=True, help="caminho do arquivo PDF local")
    official_pdf.add_argument("--brand", required=True, help="marca do catálogo (ex: natura, o-boticario)")
    official_pdf.add_argument("--edition", required=True, help="edição ou ano do catálogo (ex: 2026-ciclo-01)")
    official_pdf.add_argument("--source-id", required=True, help="ID da fonte em data/sources.yml (ex: official_catalog_natura)")
    official_pdf.add_argument("--dry-run", action="store_true", help="executa sem gravar no staging")
    official_pdf.add_argument("--no-inbox", action="store_true", help="não gera rascunhos no vault 00_Inbox")
    official_pdf.add_argument(
        "--generate-review-inbox",
        action="store_true",
        help="gera rascunhos apenas para exceções ambíguas; desativado por padrão",
    )
    commands.add_parser("vtex-enrich", help="enriquece fragrâncias desconectadas via VTEX e DuckDuckGo")
    commands.add_parser("auto-approve", help="avalia réguas de qualidade e aprova automaticamente fragrâncias completas da Inbox")
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
                discovery_countries=args.discovery_country,
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
        elif args.command == "curation-queue":
            result = build_curation_queue(
                data_directory=data_directory,
                vault_directory=args.vault_dir.resolve(),
                release_directory=args.release_dir.resolve(),
                report_path=args.report.resolve(),
                limit=args.limit,
            )
            _print(result.as_dict())
        elif args.command == "wikidata-audit":
            _print(audit_wikidata_properties(
                data_directory,
                output_path=args.output.resolve(),
                batch_size=args.batch_size,
                retrieved_at=args.retrieved_at,
            ))
        elif args.command == "wikidata-values-audit":
            _print(audit_wikidata_property_values(
                data_directory,
                output_path=args.output.resolve(),
                property_ids=args.property or ("P1552", "P2360", "P366", "P4543"),
                batch_size=args.batch_size,
                retrieved_at=args.retrieved_at,
            ))
        elif args.command == "official-pdf":
            _print(process_official_pdf(
                pdf_path=args.input.resolve(),
                brand=args.brand,
                edition=args.edition,
                source_id=args.source_id,
                data_directory=data_directory,
                dry_run=args.dry_run,
                generate_inbox=args.generate_review_inbox and not args.no_inbox,
            ))
        elif args.command == "vtex-enrich":
            from .vtex_enrichment import run_vtex_enrichment
            run_vtex_enrichment()
        elif args.command == "auto-approve":
            from .auto_approve import run_auto_approval
            run_auto_approval()
        return 0

    except (FileNotFoundError, RuntimeError, ValueError) as error:
        print(f"erro: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
