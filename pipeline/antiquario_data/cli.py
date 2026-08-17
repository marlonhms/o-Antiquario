from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Sequence

from .io_utils import load_json
from .knowledge_enrichment import build_knowledge_enrichment_plan, promote_knowledge_enrichment_plan
from .catalog_release import compile_catalog_release
from .curation_queue import build_curation_queue
from .official_pdf import process_official_pdf
from .odeuropa_backlog import build_odeuropa_routing_backlog
from .odeuropa import DEFAULT_REF as ODEUROPA_DEFAULT_REF, sync_odeuropa
from .odeuropa_equivalence import resolve_odeuropa_equivalences
from .odeuropa_retrieval import (
    build_odeuropa_retrieval_index,
    expand_odeuropa_query,
    load_latest_odeuropa_retrieval_index,
)
from .odeuropa_demand import build_p4_demand_gate, record_anonymized_query_demand
from .warehouse import build_catalog
from .wikidata import audit_wikidata_properties, audit_wikidata_property_values, sync_wikidata


def _print(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="antiquario-data", description="Pipeline local de dados do Antiquário")
    parser.add_argument("--data-dir", type=Path, default=Path("data"), help="raiz de dados do projeto")
    commands = parser.add_subparsers(dest="command", required=True)

    sync = commands.add_parser("sync", help="sincroniza uma fonte para staging")
    sync.add_argument("source", choices=["wikidata", "odeuropa"])
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
    sync.add_argument("--source-dir", type=Path, help="checkout local da ODEUROPA; omita para baixar do GitHub")
    sync.add_argument("--ref", default=ODEUROPA_DEFAULT_REF, help="commit ou tag fixada da ODEUROPA")
    sync.add_argument(
        "--language",
        action="append",
        choices=["de", "en", "fr", "it"],
        default=[],
        help="idioma ODEUROPA; pode ser repetido (padrão: todos)",
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

    odeuropa_resolve = commands.add_parser(
        "odeuropa-resolve",
        help="resolve pontes lexicais ODEUROPA para a taxonomia canônica",
    )
    odeuropa_resolve.add_argument("--taxonomy", type=Path, help="taxonomia YAML; padrão: data/taxonomy/taxonomy.yml")
    odeuropa_resolve.add_argument("--staging-dir", type=Path, help="snapshot de staging; padrão: latest.json")
    odeuropa_index = commands.add_parser(
        "odeuropa-index",
        help="compila e avalia o índice seguro de expansão de consultas",
    )
    odeuropa_index.add_argument("--equivalence-dir", type=Path, help="diretório de equivalências; padrão: snapshot atual")
    odeuropa_index.add_argument(
        "--gold",
        type=Path,
        default=Path("data/evaluation/odeuropa-retrieval-gold.yml"),
        help="conjunto ouro YAML para avaliação",
    )
    odeuropa_index.add_argument(
        "--knowledge-dir",
        type=Path,
        default=Path("knowledge/compiled"),
        help="Knowledge Core compilado usado para criar rotas de chunks",
    )
    odeuropa_query = commands.add_parser("odeuropa-query", help="testa uma consulta no índice ODEUROPA local")
    odeuropa_query.add_argument("query", help="consulta textual")
    odeuropa_query.add_argument("--language", required=True, choices=["de", "en", "fr", "it", "pt-BR"])
    odeuropa_query.add_argument("--index", type=Path, help="index.json alternativo")
    odeuropa_backlog = commands.add_parser(
        "odeuropa-backlog",
        help="prioriza lacunas de roteamento sem alterar o Knowledge Core",
    )
    odeuropa_backlog.add_argument("--retrieval-dir", type=Path, help="diretório retrieval; padrão: snapshot atual")
    odeuropa_backlog.add_argument(
        "--gold",
        type=Path,
        default=Path("data/evaluation/odeuropa-retrieval-gold.yml"),
        help="conjunto ouro YAML usado como sinal de demanda",
    )
    odeuropa_backlog.add_argument(
        "--knowledge-dir",
        type=Path,
        default=Path("knowledge/compiled"),
        help="Knowledge Core compilado usado como sinal estrutural",
    )
    odeuropa_backlog.add_argument(
        "--catalog",
        type=Path,
        default=Path("apps/web/public/catalog/recommendation-catalog.json"),
        help="catálogo ativo usado como sinal de demanda",
    )
    enrichment_plan = commands.add_parser(
        "odeuropa-enrichment-plan",
        help="gera candidatos factuais auditáveis para documentos P3",
    )
    enrichment_plan.add_argument("--retrieval-dir", type=Path, help="diretório retrieval; padrão: snapshot atual")
    enrichment_plan.add_argument("--knowledge-dir", type=Path, default=Path("knowledge/compiled"))
    enrichment_plan.add_argument("--vault-dir", type=Path, default=Path("knowledge/vault"))
    enrichment_plan.add_argument("--sources", type=Path, default=Path("data/sources.yml"))
    enrichment_promote = commands.add_parser(
        "odeuropa-enrichment-promote",
        help="promove somente candidatos P3 auditados e sem alteração concorrente",
    )
    enrichment_promote.add_argument("--retrieval-dir", type=Path, help="diretório retrieval; padrão: snapshot atual")
    enrichment_promote.add_argument("--vault-dir", type=Path, default=Path("knowledge/vault"))
    enrichment_promote.add_argument("--sources", type=Path, default=Path("data/sources.yml"))
    enrichment_promote.add_argument("--updated-at", help="data ISO da promoção; padrão: data atual")
    demand_record = commands.add_parser(
        "odeuropa-demand-record",
        help="registra somente destinos canônicos de uma consulta, sem guardar o texto bruto",
    )
    demand_record.add_argument("query", help="consulta processada somente em memória")
    demand_record.add_argument("--language", required=True, choices=["de", "en", "fr", "it", "pt-BR"])
    demand_record.add_argument("--events", type=Path, help="arquivo privado JSONL; padrão: data/private/demand")
    demand_record.add_argument("--index", type=Path, help="index.json alternativo")
    demand_record.add_argument("--occurred-on", help="data ISO com precisão de dia; padrão: hoje")
    demand_record.add_argument("--event-id", help="identidade idempotente fornecida pela aplicação")
    demand_gate = commands.add_parser(
        "odeuropa-demand-gate",
        help="classifica itens P4 por demanda sem criar documentos ou fatos",
    )
    demand_gate.add_argument("--retrieval-dir", type=Path, help="diretório retrieval; padrão: snapshot atual")
    demand_gate.add_argument("--events", type=Path, help="arquivo privado JSONL; padrão: data/private/demand")
    demand_gate.add_argument(
        "--catalog",
        type=Path,
        default=Path("apps/web/public/catalog/recommendation-catalog.json"),
        help="catálogo aprovado usado como sinal operacional",
    )
    demand_gate.add_argument(
        "--policy",
        type=Path,
        default=Path("data/evaluation/odeuropa-p4-demand.yml"),
        help="política versionada de limiares e prioridade editorial",
    )
    demand_gate.add_argument("--as-of", help="data ISO de referência; padrão: hoje")

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
            if args.source == "wikidata":
                result = sync_wikidata(
                    data_directory,
                    limit=args.limit,
                    fixture=args.fixture.resolve() if args.fixture else None,
                    retrieved_at=args.retrieved_at,
                    discovery_countries=args.discovery_country,
                )
            else:
                if args.fixture or args.discovery_country:
                    raise ValueError("--fixture e --discovery-country são exclusivos do Wikidata")
                result = sync_odeuropa(
                    data_directory,
                    source_directory=args.source_dir.resolve() if args.source_dir else None,
                    source_ref=args.ref,
                    languages=args.language or None,
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
        elif args.command == "odeuropa-resolve":
            _print(resolve_odeuropa_equivalences(
                data_directory,
                taxonomy_path=args.taxonomy.resolve() if args.taxonomy else None,
                staging_directory=args.staging_dir.resolve() if args.staging_dir else None,
            ).as_dict())
        elif args.command == "odeuropa-index":
            result = build_odeuropa_retrieval_index(
                data_directory,
                equivalence_directory=args.equivalence_dir.resolve() if args.equivalence_dir else None,
                gold_path=args.gold.resolve(),
                knowledge_directory=args.knowledge_dir.resolve(),
            )
            _print(result.as_dict())
            if result.evaluation_passed is False:
                return 1
        elif args.command == "odeuropa-query":
            index = load_json(args.index.resolve()) if args.index else load_latest_odeuropa_retrieval_index(data_directory)
            _print(expand_odeuropa_query(index, args.query, language=args.language))
        elif args.command == "odeuropa-backlog":
            _print(build_odeuropa_routing_backlog(
                data_directory,
                retrieval_directory=args.retrieval_dir.resolve() if args.retrieval_dir else None,
                gold_path=args.gold.resolve(),
                knowledge_directory=args.knowledge_dir.resolve(),
                catalog_path=args.catalog.resolve(),
            ).as_dict())
        elif args.command == "odeuropa-enrichment-plan":
            _print(build_knowledge_enrichment_plan(
                data_directory,
                retrieval_directory=args.retrieval_dir.resolve() if args.retrieval_dir else None,
                knowledge_directory=args.knowledge_dir.resolve(),
                vault_directory=args.vault_dir.resolve(),
                source_manifest_path=args.sources.resolve(),
            ).as_dict())
        elif args.command == "odeuropa-enrichment-promote":
            _print(promote_knowledge_enrichment_plan(
                data_directory,
                retrieval_directory=args.retrieval_dir.resolve() if args.retrieval_dir else None,
                vault_directory=args.vault_dir.resolve(),
                source_manifest_path=args.sources.resolve(),
                updated_at=args.updated_at,
            ).as_dict())
        elif args.command == "odeuropa-demand-record":
            _print(record_anonymized_query_demand(
                data_directory,
                args.query,
                language=args.language,
                events_path=args.events.resolve() if args.events else None,
                index_path=args.index.resolve() if args.index else None,
                occurred_on=args.occurred_on,
                event_id=args.event_id,
            ).as_dict())
        elif args.command == "odeuropa-demand-gate":
            _print(build_p4_demand_gate(
                data_directory,
                retrieval_directory=args.retrieval_dir.resolve() if args.retrieval_dir else None,
                events_path=args.events.resolve() if args.events else None,
                catalog_path=args.catalog.resolve(),
                policy_path=args.policy.resolve(),
                as_of=args.as_of,
            ).as_dict())
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
