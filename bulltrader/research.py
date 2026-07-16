from __future__ import annotations

import fcntl
import hashlib
import json
import os
import re
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class ResearchError(RuntimeError):
    pass


AGENTS = {"bull", "aggro"}
ROUTINES = {"premarket", "weekly-review", "monthly-review", "knowledge-import"}
SOURCE_TYPES = {
    "regulatory_filing",
    "company_release",
    "exchange_market_data",
    "government",
    "academic",
    "source_code",
    "reputable_secondary",
    "other",
}
PRIMARY_CANDIDATE_SOURCE_TYPES = {
    "regulatory_filing",
    "company_release",
    "exchange_market_data",
    "government",
}
CLAIM_STANCES = {"supports", "opposes", "context"}
CONFIDENCE = {"low", "medium", "high"}
INFERENCE_KINDS = {
    "macro",
    "sector",
    "company",
    "valuation",
    "risk",
    "liquidity",
    "technical",
    "methodology",
}
HORIZONS = {"intraday", "days", "weeks", "months", "multi-year"}
ASSESSMENTS = {"candidate", "hold", "avoid", "watch"}
ID_RE = re.compile(r"^[a-z0-9][a-z0-9._:-]{2,127}$")
SYMBOL_RE = re.compile(r"^[A-Z][A-Z0-9.-]{0,9}$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
RFC3339_RE = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?(?:Z|[+-]\d{2}:\d{2})$"
)
MAX_PACKET_BYTES = 32_000
MAX_FUTURE_SKEW = timedelta(minutes=5)
DEFAULT_CANDIDATE_MAX_AGE_MINUTES = 240
DEFAULT_MARKET_SOURCE_MAX_AGE_MINUTES = 120
# Schema-v1 historical validation is immutable. Human policy may impose a
# tighter limit when a packet is appended or used, but cannot rewrite whether
# an already-accepted append-only row remains structurally valid.
SCHEMA_MARKET_SOURCE_MAX_AGE_MINUTES = 24 * 60
TRACKING_QUERY_KEYS = {
    "fbclid",
    "gclid",
    "mc_cid",
    "mc_eid",
    "ref",
    "source",
}


def _error(context: str, message: str) -> None:
    raise ResearchError(f"{context}: {message}")


def _mapping(value: Any, context: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        _error(context, "must be an object")
    return value


def _list(value: Any, context: str) -> list[Any]:
    if not isinstance(value, list):
        _error(context, "must be an array")
    return value


def _exact(value: dict[str, Any], fields: set[str], context: str) -> None:
    missing = sorted(fields - set(value))
    extra = sorted(set(value) - fields)
    if missing:
        _error(context, f"missing fields: {', '.join(missing)}")
    if extra:
        _error(context, f"unknown fields: {', '.join(extra)}")


def _text(value: Any, context: str, *, minimum: int = 1, maximum: int = 4_000) -> str:
    if not isinstance(value, str):
        _error(context, "must be text")
    result = value.strip()
    if not minimum <= len(result) <= maximum:
        _error(context, f"length must be between {minimum} and {maximum}")
    return result


def _string_list(
    value: Any,
    context: str,
    *,
    minimum_items: int = 0,
    maximum_items: int = 50,
) -> list[str]:
    values = _list(value, context)
    if not minimum_items <= len(values) <= maximum_items:
        _error(context, f"item count must be between {minimum_items} and {maximum_items}")
    result = [_text(item, f"{context}[{index}]", maximum=1_000) for index, item in enumerate(values)]
    if len(result) != len(set(result)):
        _error(context, "must not contain duplicates")
    return result


def _identifier_list(
    value: Any,
    context: str,
    *,
    minimum_items: int = 0,
    maximum_items: int = 50,
) -> list[str]:
    values = _list(value, context)
    if not minimum_items <= len(values) <= maximum_items:
        _error(context, f"item count must be between {minimum_items} and {maximum_items}")
    result = [_identifier(item, f"{context}[{index}]") for index, item in enumerate(values)]
    if len(result) != len(set(result)):
        _error(context, "must not contain duplicates")
    return result


def _timestamp(value: Any, context: str) -> datetime:
    if not isinstance(value, str) or value != value.strip() or not RFC3339_RE.fullmatch(value):
        _error(context, "must be a canonical RFC-3339 timestamp")
    if value.endswith("-00:00"):
        _error(context, "must use a known UTC offset; -00:00 is not allowed")
    text = value
    try:
        parsed = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ResearchError(f"{context}: must be an ISO-8601 timestamp") from exc
    if parsed.tzinfo is None or parsed.utcoffset() is None:
        _error(context, "must include a timezone")
    return parsed


def _calendar_date(value: Any, context: str) -> date:
    if not isinstance(value, str) or value != value.strip():
        _error(context, "must be a canonical YYYY-MM-DD date")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ResearchError(f"{context}: must be a canonical YYYY-MM-DD date") from exc
    if parsed.isoformat() != value:
        _error(context, "must be a canonical YYYY-MM-DD date")
    return parsed


def _positive_minutes(value: Any, context: str) -> timedelta:
    if type(value) is not int or value <= 0:
        _error(context, "must be a positive integer number of minutes")
    return timedelta(minutes=value)


def _optional_timestamp(value: Any, context: str) -> datetime | None:
    if value is None:
        return None
    return _timestamp(value, context)


def _identifier(value: Any, context: str) -> str:
    if not isinstance(value, str) or value != value.strip():
        _error(context, "must not contain surrounding whitespace")
    result = _text(value, context, maximum=128)
    if not ID_RE.fullmatch(result):
        _error(context, "must use lowercase letters, digits, dot, colon, underscore, or hyphen")
    return result


def canonical_url(value: Any, context: str = "url") -> str:
    raw = _text(value, context, maximum=2_048)
    try:
        parsed = urlsplit(raw)
        port_number = parsed.port
    except ValueError as exc:
        raise ResearchError(f"{context}: malformed URL") from exc
    if parsed.scheme.lower() != "https" or not parsed.netloc or parsed.username or parsed.password:
        _error(context, "must be an https URL without embedded credentials")
    if not parsed.hostname:
        _error(context, "must include a valid hostname")
    try:
        host = parsed.hostname.rstrip(".").encode("idna").decode("ascii").lower()
    except UnicodeError as exc:
        raise ResearchError(f"{context}: malformed hostname") from exc
    if not host:
        _error(context, "must include a valid hostname")
    if ":" in host:
        host = f"[{host}]"
    port = f":{port_number}" if port_number and port_number != 443 else ""
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    if path != "/":
        path = path.rstrip("/")
    query = [
        (key, val)
        for key, val in parse_qsl(parsed.query, keep_blank_values=True)
        if not key.lower().startswith("utm_") and key.lower() not in TRACKING_QUERY_KEYS
    ]
    return urlunsplit(("https", f"{host}{port}", path, urlencode(sorted(query)), ""))


def _enum(value: Any, allowed: set[str], context: str) -> str:
    if not isinstance(value, str) or value != value.strip():
        _error(context, "must not contain surrounding whitespace")
    result = _text(value, context, maximum=100)
    if result not in allowed:
        _error(context, f"must be one of: {', '.join(sorted(allowed))}")
    return result


def _symbol_list(
    value: Any,
    context: str,
    *,
    minimum_items: int = 0,
    maximum_items: int = 50,
) -> list[str]:
    values = _list(value, context)
    if not minimum_items <= len(values) <= maximum_items:
        _error(context, f"item count must be between {minimum_items} and {maximum_items}")
    result: list[str] = []
    for index, symbol in enumerate(values):
        item_context = f"{context}[{index}]"
        if not isinstance(symbol, str) or symbol != symbol.strip():
            _error(item_context, "must be a canonical uppercase ticker")
        if not SYMBOL_RE.fullmatch(symbol):
            _error(item_context, "must be a canonical uppercase ticker")
        result.append(symbol)
    if len(result) != len(set(result)):
        _error(context, "must not contain duplicates")
    return result


def validate_packet(
    packet: Any,
    expected_agent: str | None = None,
    *,
    market_source_max_age_minutes: int = SCHEMA_MARKET_SOURCE_MAX_AGE_MINUTES,
) -> dict[str, Any]:
    packet = _mapping(packet, "packet")
    market_source_max_age = _positive_minutes(
        market_source_max_age_minutes, "market_source_max_age_minutes"
    )
    if len(json.dumps(packet, separators=(",", ":"), ensure_ascii=False).encode("utf-8")) > MAX_PACKET_BYTES:
        _error("packet", f"serialized size cannot exceed {MAX_PACKET_BYTES} bytes")
    _exact(
        packet,
        {
            "schema_version",
            "packet_id",
            "agent",
            "routine",
            "decision_time",
            "market_data_cutoff",
            "window",
            "sources",
            "claims",
            "inferences",
            "decision_support",
            "untrusted_instructions_detected",
            "packet_limitations",
        },
        "packet",
    )
    if type(packet["schema_version"]) is not int or packet["schema_version"] != 1:
        _error("packet.schema_version", "must equal 1")
    packet_id = _identifier(packet["packet_id"], "packet.packet_id")
    agent = _enum(packet["agent"], AGENTS, "packet.agent")
    if expected_agent is not None and agent != expected_agent:
        _error("packet.agent", f"expected {expected_agent}")
    if not packet_id.startswith(f"{agent}:"):
        _error("packet.packet_id", f"must begin with {agent}:")
    _enum(packet["routine"], ROUTINES, "packet.routine")
    decision_time = _timestamp(packet["decision_time"], "packet.decision_time")
    market_cutoff = _timestamp(packet["market_data_cutoff"], "packet.market_data_cutoff")
    if market_cutoff > decision_time:
        _error("packet.market_data_cutoff", "cannot be after decision_time")
    if not isinstance(packet["untrusted_instructions_detected"], bool):
        _error("packet.untrusted_instructions_detected", "must be boolean")
    packet_limitations = _string_list(
        packet["packet_limitations"], "packet.packet_limitations"
    )
    if packet["untrusted_instructions_detected"] and not packet_limitations:
        _error(
            "packet.packet_limitations",
            "must explain how detected untrusted instructions were handled",
        )

    window = _mapping(packet["window"], "packet.window")
    _exact(window, {"start", "end", "complete", "failures", "limitations"}, "packet.window")
    start = _timestamp(window["start"], "packet.window.start")
    end = _timestamp(window["end"], "packet.window.end")
    if start >= end:
        _error("packet.window", "start must be before end")
    if end > decision_time:
        _error("packet.window.end", "cannot be after decision_time")
    if not isinstance(window["complete"], bool):
        _error("packet.window.complete", "must be boolean")
    failures = _list(window["failures"], "packet.window.failures")
    if len(failures) > 50:
        _error("packet.window.failures", "cannot exceed 50 records")
    for index, failure_value in enumerate(failures):
        context = f"packet.window.failures[{index}]"
        failure = _mapping(failure_value, context)
        _exact(failure, {"stage", "source", "error"}, context)
        for field in ("stage", "source", "error"):
            _text(failure[field], f"{context}.{field}", maximum=1_000)
    limitations = _string_list(window["limitations"], "packet.window.limitations")
    if window["complete"] and failures:
        _error("packet.window", "a complete window cannot contain collection failures")
    if not window["complete"] and not failures and not limitations:
        _error("packet.window", "an incomplete window must explain failures or limitations")

    source_rows = _list(packet["sources"], "packet.sources")
    if not 1 <= len(source_rows) <= 100:
        _error("packet.sources", "must contain between 1 and 100 sources")
    sources: dict[str, dict[str, Any]] = {}
    source_hosts: dict[str, str] = {}
    source_as_of: dict[str, datetime] = {}
    canonical_urls: set[str] = set()
    captured_hashes: set[str] = set()
    for index, source_value in enumerate(source_rows):
        context = f"packet.sources[{index}]"
        source = _mapping(source_value, context)
        _exact(
            source,
            {
                "source_id",
                "source_type",
                "tier",
                "url",
                "publisher",
                "published_at",
                "fetched_at",
                "as_of",
                "content_sha256",
                "hash_status",
                "locator",
                "limitations",
            },
            context,
        )
        source_id = _identifier(source["source_id"], f"{context}.source_id")
        if source_id in sources:
            _error(f"{context}.source_id", "duplicates another source_id")
        source_type = _enum(
            source["source_type"], SOURCE_TYPES, f"{context}.source_type"
        )
        if isinstance(source["tier"], bool) or source["tier"] not in {1, 2, 3}:
            _error(f"{context}.tier", "must be integer 1, 2, or 3")
        tier = source["tier"]
        if source_type in PRIMARY_CANDIDATE_SOURCE_TYPES | {"source_code"} and tier != 1:
            _error(f"{context}.tier", f"{source_type} must use tier 1")
        if source_type == "reputable_secondary" and tier == 1:
            _error(f"{context}.tier", "reputable_secondary cannot use tier 1")
        if source_type == "other" and tier != 3:
            _error(f"{context}.tier", "other sources must use tier 3")
        url = canonical_url(source["url"], f"{context}.url")
        if url in canonical_urls:
            _error(f"{context}.url", "duplicates a canonical URL in this packet")
        canonical_urls.add(url)
        _text(source["publisher"], f"{context}.publisher", maximum=200)
        published = _optional_timestamp(source["published_at"], f"{context}.published_at")
        fetched = _timestamp(source["fetched_at"], f"{context}.fetched_at")
        as_of = _timestamp(source["as_of"], f"{context}.as_of")
        if fetched < start or fetched >= end:
            _error(
                f"{context}.fetched_at",
                "must fall inside the declared half-open research window",
            )
        if fetched > decision_time:
            _error(f"{context}.fetched_at", "cannot be after decision_time")
        if published is not None and published > fetched:
            _error(f"{context}.published_at", "cannot be after fetched_at")
        if as_of > decision_time:
            _error(f"{context}.as_of", "cannot be after decision_time")
        if as_of > market_cutoff:
            _error(f"{context}.as_of", "cannot be after market_data_cutoff")
        if as_of > fetched:
            _error(f"{context}.as_of", "cannot be after fetched_at")
        hash_status = _enum(source["hash_status"], {"captured", "not_captured"}, f"{context}.hash_status")
        content_hash = source["content_sha256"]
        if hash_status == "captured":
            if not isinstance(content_hash, str) or not SHA256_RE.fullmatch(content_hash):
                _error(f"{context}.content_sha256", "must be a lowercase sha256 when captured")
            if content_hash in captured_hashes:
                _error(
                    f"{context}.content_sha256",
                    "duplicates captured content from another source",
                )
            captured_hashes.add(content_hash)
        elif content_hash is not None:
            _error(f"{context}.content_sha256", "must be null when hash_status is not_captured")
        _text(source["locator"], f"{context}.locator", maximum=500)
        _string_list(source["limitations"], f"{context}.limitations")
        source["url"] = url
        sources[source_id] = source
        source_hosts[source_id] = urlsplit(url).hostname or ""
        source_as_of[source_id] = as_of

    claim_rows = _list(packet["claims"], "packet.claims")
    if not 1 <= len(claim_rows) <= 200:
        _error("packet.claims", "must contain between 1 and 200 claims")
    claims: dict[str, dict[str, Any]] = {}
    claim_sources: dict[str, list[str]] = {}
    claim_symbols: dict[str, list[str]] = {}
    for index, claim_value in enumerate(claim_rows):
        context = f"packet.claims[{index}]"
        claim = _mapping(claim_value, context)
        _exact(
            claim,
            {
                "claim_id",
                "text",
                "symbols",
                "source_ids",
                "as_of",
                "stance",
                "confidence",
                "limitations",
            },
            context,
        )
        claim_id = _identifier(claim["claim_id"], f"{context}.claim_id")
        if claim_id in claims:
            _error(f"{context}.claim_id", "duplicates another claim_id")
        _text(claim["text"], f"{context}.text", minimum=15, maximum=2_000)
        symbols = _symbol_list(claim["symbols"], f"{context}.symbols")
        source_ids = _identifier_list(
            claim["source_ids"], f"{context}.source_ids", minimum_items=1, maximum_items=20
        )
        undefined = [value for value in source_ids if value not in sources]
        if undefined:
            _error(f"{context}.source_ids", f"undefined source IDs: {', '.join(undefined)}")
        claim_as_of = _timestamp(claim["as_of"], f"{context}.as_of")
        if claim_as_of > decision_time:
            _error(f"{context}.as_of", "cannot be after decision_time")
        if claim_as_of > market_cutoff:
            _error(f"{context}.as_of", "cannot be after market_data_cutoff")
        _enum(claim["stance"], CLAIM_STANCES, f"{context}.stance")
        _enum(claim["confidence"], CONFIDENCE, f"{context}.confidence")
        _string_list(claim["limitations"], f"{context}.limitations")
        claims[claim_id] = claim
        claim_sources[claim_id] = source_ids
        claim_symbols[claim_id] = symbols

    inference_rows = _list(packet["inferences"], "packet.inferences")
    if not 1 <= len(inference_rows) <= 100:
        _error("packet.inferences", "must contain between 1 and 100 inferences")
    inferences: dict[str, dict[str, Any]] = {}
    inference_claims: dict[str, list[str]] = {}
    inference_symbols: dict[str, list[str]] = {}
    for index, inference_value in enumerate(inference_rows):
        context = f"packet.inferences[{index}]"
        inference = _mapping(inference_value, context)
        _exact(
            inference,
            {
                "inference_id",
                "text",
                "symbols",
                "claim_ids",
                "kind",
                "horizon",
                "confidence",
                "falsifier",
                "limitations",
            },
            context,
        )
        inference_id = _identifier(inference["inference_id"], f"{context}.inference_id")
        if inference_id in inferences:
            _error(f"{context}.inference_id", "duplicates another inference_id")
        _text(inference["text"], f"{context}.text", minimum=20, maximum=2_000)
        symbols = _symbol_list(inference["symbols"], f"{context}.symbols")
        claim_ids = _identifier_list(
            inference["claim_ids"], f"{context}.claim_ids", minimum_items=1, maximum_items=30
        )
        undefined = [value for value in claim_ids if value not in claims]
        if undefined:
            _error(f"{context}.claim_ids", f"undefined claim IDs: {', '.join(undefined)}")
        _enum(inference["kind"], INFERENCE_KINDS, f"{context}.kind")
        _enum(inference["horizon"], HORIZONS, f"{context}.horizon")
        _enum(inference["confidence"], CONFIDENCE, f"{context}.confidence")
        _text(inference["falsifier"], f"{context}.falsifier", minimum=10, maximum=1_000)
        _string_list(inference["limitations"], f"{context}.limitations")
        inferences[inference_id] = inference
        inference_claims[inference_id] = claim_ids
        inference_symbols[inference_id] = symbols

    decision_rows = _list(packet["decision_support"], "packet.decision_support")
    if len(decision_rows) > 50:
        _error("packet.decision_support", "cannot exceed 50 records")
    decision_symbols: set[str] = set()
    for index, decision_value in enumerate(decision_rows):
        context = f"packet.decision_support[{index}]"
        decision = _mapping(decision_value, context)
        _exact(
            decision,
            {
                "symbol",
                "assessment",
                "supporting_inference_ids",
                "opposing_claim_ids",
                "strongest_counterargument",
                "critical_unknowns",
                "thesis",
                "invalidation",
                "review_by",
                "status",
            },
            context,
        )
        if not isinstance(decision["symbol"], str) or decision["symbol"] != decision["symbol"].strip():
            _error(f"{context}.symbol", "must be a canonical uppercase ticker")
        symbol = _text(decision["symbol"], f"{context}.symbol", maximum=10)
        if not SYMBOL_RE.fullmatch(symbol):
            _error(f"{context}.symbol", "must be a canonical uppercase ticker")
        if symbol in decision_symbols:
            _error(f"{context}.symbol", "duplicates another decision-support record")
        decision_symbols.add(symbol)
        assessment = _enum(decision["assessment"], ASSESSMENTS, f"{context}.assessment")
        supporting = _identifier_list(
            decision["supporting_inference_ids"],
            f"{context}.supporting_inference_ids",
            minimum_items=1,
            maximum_items=20,
        )
        undefined_inferences = [value for value in supporting if value not in inferences]
        if undefined_inferences:
            _error(
                f"{context}.supporting_inference_ids",
                f"undefined inference IDs: {', '.join(undefined_inferences)}",
            )
        opposing = _identifier_list(
            decision["opposing_claim_ids"],
            f"{context}.opposing_claim_ids",
            minimum_items=1,
            maximum_items=20,
        )
        undefined_claims = [value for value in opposing if value not in claims]
        if undefined_claims:
            _error(f"{context}.opposing_claim_ids", f"undefined claim IDs: {', '.join(undefined_claims)}")
        if any(claims[value]["stance"] != "opposes" for value in opposing):
            _error(f"{context}.opposing_claim_ids", "every referenced claim must use stance=opposes")
        if any(symbol not in claim_symbols[value] for value in opposing):
            _error(
                f"{context}.opposing_claim_ids",
                f"every referenced claim must be scoped to {symbol}",
            )
        _text(decision["strongest_counterargument"], f"{context}.strongest_counterargument", minimum=15)
        critical_unknowns = _string_list(decision["critical_unknowns"], f"{context}.critical_unknowns")
        thesis = _text(decision["thesis"], f"{context}.thesis", minimum=20, maximum=2_000)
        invalidation = _text(
            decision["invalidation"], f"{context}.invalidation", minimum=10, maximum=1_000
        )
        review_by = _calendar_date(decision["review_by"], f"{context}.review_by")
        if decision["thesis"] != thesis or decision["invalidation"] != invalidation:
            _error(context, "thesis and invalidation cannot contain surrounding whitespace")
        if review_by < decision_time.date():
            _error(f"{context}.review_by", "cannot be before the decision date")
        if decision["status"] != "research_only":
            _error(f"{context}.status", "must equal research_only")

        if assessment == "candidate":
            if packet["untrusted_instructions_detected"]:
                _error(context, "candidate assessment cannot use a packet with detected instructions")
            if not window["complete"]:
                _error(context, "candidate assessment requires a complete requested research window")
            if limitations or packet_limitations:
                _error(
                    context,
                    "candidate assessment cannot retain window or packet-level limitations",
                )
            if critical_unknowns:
                _error(context, "candidate assessment cannot retain critical unknowns")
            if any(symbol not in inference_symbols[value] for value in supporting):
                _error(
                    f"{context}.supporting_inference_ids",
                    f"every referenced inference must be scoped to {symbol}",
                )
            supporting_claims = {
                claim_id
                for inference_id in supporting
                for claim_id in inference_claims[inference_id]
                if claims[claim_id]["stance"] == "supports"
                and symbol in claim_symbols[claim_id]
            }
            if not supporting_claims:
                _error(context, "candidate assessment requires symbol-scoped stance=supports claims")
            traced_sources = {
                source_id
                for claim_id in supporting_claims
                for source_id in claim_sources[claim_id]
            }
            publishers = {str(sources[value]["publisher"]).strip().lower() for value in traced_sources}
            hosts = {source_hosts[value] for value in traced_sources}
            if len(traced_sources) < 2 or len(publishers) < 2 or len(hosts) < 2:
                _error(
                    context,
                    "candidate assessment requires at least two distinct declared sources/publishers/hosts",
                )
            if not any(
                sources[value]["source_type"] in PRIMARY_CANDIDATE_SOURCE_TYPES
                for value in traced_sources
            ):
                _error(
                    context,
                    "candidate assessment requires at least one tier-1 primary market source",
                )
            current_market_sources = {
                value
                for value in traced_sources
                if sources[value]["source_type"] == "exchange_market_data"
                and timedelta(0)
                <= decision_time - source_as_of[value]
                <= market_source_max_age
                and not sources[value]["limitations"]
            }
            current_market_claims = {
                claim_id
                for claim_id in supporting_claims
                if not claims[claim_id]["limitations"]
                and current_market_sources.intersection(claim_sources[claim_id])
            }
            if not current_market_sources or not current_market_claims:
                _error(
                    context,
                    "candidate assessment requires current unqualified traced exchange market data",
                )

    packet["packet_id"] = packet_id
    return packet


def validate_ledger(
    path: Path,
    expected_agent: str,
) -> list[dict[str, Any]]:
    if expected_agent not in AGENTS:
        raise ResearchError("expected_agent must be bull or aggro")
    if path.is_symlink():
        raise ResearchError(f"research ledger cannot be a symlink: {path}")
    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as exc:
        raise ResearchError(f"cannot read research ledger {path}: {exc}") from exc
    return _validate_ledger_lines(lines, path, expected_agent)


def _validate_ledger_lines(
    lines: list[str],
    path: Path,
    expected_agent: str,
) -> list[dict[str, Any]]:
    packets: list[dict[str, Any]] = []
    packet_ids: set[str] = set()
    previous_time: datetime | None = None
    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        try:
            raw = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ResearchError(
                f"{path}:{line_number}: malformed JSON: {exc.msg}"
            ) from exc
        try:
            packet = validate_packet(
                raw,
                expected_agent,
                market_source_max_age_minutes=SCHEMA_MARKET_SOURCE_MAX_AGE_MINUTES,
            )
        except ResearchError as exc:
            raise ResearchError(f"{path}:{line_number}: {exc}") from exc
        packet_id = packet["packet_id"]
        if packet_id in packet_ids:
            raise ResearchError(f"{path}:{line_number}: duplicate packet_id {packet_id}")
        decision_time = _timestamp(packet["decision_time"], "packet.decision_time")
        if previous_time is not None and decision_time <= previous_time:
            raise ResearchError(
                f"{path}:{line_number}: decision_time must be strictly later than the prior packet"
            )
        packet_ids.add(packet_id)
        packets.append(packet)
        previous_time = decision_time
    return packets


def ledger_path(root: Path, agent: str) -> Path:
    if agent not in AGENTS:
        raise ResearchError("agent must be bull or aggro")
    if agent == "aggro":
        return root / "memory" / "aggressive" / "research-evidence.jsonl"
    return root / "memory" / "research-evidence.jsonl"


def pending_path(root: Path, agent: str) -> Path:
    if agent not in AGENTS:
        raise ResearchError("agent must be bull or aggro")
    if agent == "aggro":
        return root / "memory" / "aggressive" / "research-packet.pending.json"
    return root / "memory" / "research-packet.pending.json"


def _packet_json(packet: dict[str, Any]) -> str:
    return json.dumps(packet, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def packet_identity(packet: dict[str, Any]) -> dict[str, str]:
    canonical = _packet_json(packet)
    return {
        "packet_id": packet["packet_id"],
        "packet_sha256": hashlib.sha256(canonical.encode("utf-8")).hexdigest(),
    }


def _fsync_directory(directory: Path, context: str) -> None:
    try:
        directory_fd = os.open(directory, os.O_RDONLY)
        try:
            os.fsync(directory_fd)
        finally:
            os.close(directory_fd)
    except OSError as exc:
        raise ResearchError(f"{context}: could not sync directory metadata: {exc}") from exc


def _claim_pending_packet(pending: Path) -> Path:
    """Atomically move the fixed handoff slot to a unique in-flight path."""
    if pending.is_symlink():
        raise ResearchError("research pending packet must be a regular file")
    claimed = pending.with_name(
        f".research-packet.claimed-{os.getpid()}-{time.time_ns()}.json"
    )
    try:
        pending.rename(claimed)
    except OSError as exc:
        raise ResearchError(f"cannot claim pending research packet {pending}: {exc}") from exc
    _fsync_directory(pending.parent, "pending packet claim")
    if claimed.is_symlink() or not claimed.is_file():
        raise ResearchError(
            f"claimed research packet is not a regular file; retained at {claimed}"
        )
    return claimed


def _restore_claimed_packet(claimed: Path, pending: Path) -> bool:
    """Restore a failed claim while retaining its audit link."""
    try:
        os.link(claimed, pending)
    except FileExistsError:
        return False
    except OSError as exc:
        raise ResearchError(
            f"could not restore claimed packet; retained at {claimed}: {exc}"
        ) from exc
    _fsync_directory(pending.parent, "pending packet restore")
    return True


def _remove_replayed_claim_links(claimed: Path) -> None:
    """Remove only older claim names that reference this successfully consumed inode."""
    removed = False
    for other in claimed.parent.glob(".research-packet.claimed-*.json"):
        if other == claimed:
            continue
        try:
            if other.is_file() and claimed.samefile(other):
                other.unlink()
                removed = True
        except OSError as exc:
            raise ResearchError(
                f"packet appended but a replayed claim could not be removed: {other}: {exc}"
            ) from exc
    if removed:
        _fsync_directory(claimed.parent, "replayed claim cleanup")


def append_pending_packet(
    root: Path,
    agent: str,
    *,
    now: datetime | None = None,
    market_source_max_age_minutes: int = DEFAULT_MARKET_SOURCE_MAX_AGE_MINUTES,
    allow_candidates: bool = True,
) -> dict[str, Any]:
    """Claim, validate, and atomically append one profile-bound pending packet."""
    configured_market_age = _positive_minutes(
        market_source_max_age_minutes, "market_source_max_age_minutes"
    )
    if configured_market_age > timedelta(
        minutes=SCHEMA_MARKET_SOURCE_MAX_AGE_MINUTES
    ):
        raise ResearchError(
            "market_source_max_age_minutes cannot exceed the schema-v1 ceiling"
        )
    if type(allow_candidates) is not bool:
        raise ResearchError("allow_candidates must be boolean")
    pending = pending_path(root, agent)
    ledger = ledger_path(root, agent)
    if ledger.is_symlink():
        raise ResearchError("research ledger must be a regular file")
    claimed = _claim_pending_packet(pending)
    try:
        packet = _append_claimed_packet(
            ledger,
            claimed,
            agent,
            now=now,
            market_source_max_age_minutes=market_source_max_age_minutes,
            allow_candidates=allow_candidates,
        )
    except Exception as exc:
        try:
            restored = _restore_claimed_packet(claimed, pending)
        except ResearchError as restore_exc:
            raise ResearchError(f"{exc}; {restore_exc}") from exc
        if not restored:
            raise ResearchError(
                f"{exc}; a newer pending packet exists and the failed claim was retained at "
                f"{claimed}"
            ) from exc
        raise ResearchError(
            f"{exc}; failed claim retained for audit at {claimed}"
        ) from exc
    _remove_replayed_claim_links(claimed)
    try:
        claimed.unlink()
        _fsync_directory(claimed.parent, "consumed claim cleanup")
    except OSError as exc:
        raise ResearchError(
            f"packet appended but claimed packet was retained at {claimed}: {exc}"
        ) from exc
    return packet


def _append_claimed_packet(
    ledger: Path,
    claimed: Path,
    agent: str,
    *,
    now: datetime | None,
    market_source_max_age_minutes: int,
    allow_candidates: bool,
) -> dict[str, Any]:
    try:
        pending_bytes = claimed.read_bytes()
    except OSError as exc:
        raise ResearchError(f"cannot read claimed research packet {claimed}: {exc}") from exc
    if len(pending_bytes) > MAX_PACKET_BYTES:
        raise ResearchError(f"pending research packet exceeds {MAX_PACKET_BYTES} bytes")
    try:
        raw = json.loads(pending_bytes.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ResearchError(f"pending research packet is malformed JSON: {exc}") from exc
    trusted_now = now or datetime.now(timezone.utc)
    if trusted_now.tzinfo is None or trusted_now.utcoffset() is None:
        raise ResearchError("trusted now must include a timezone")
    raw_packet = _mapping(raw, "packet")
    if "decision_time" in raw_packet:
        untrusted_packet_time = _timestamp(
            raw_packet["decision_time"], "packet.decision_time"
        )
        if untrusted_packet_time > trusted_now + MAX_FUTURE_SKEW:
            raise ResearchError("packet.decision_time is too far in the future")
    packet = validate_packet(
        raw,
        agent,
        market_source_max_age_minutes=SCHEMA_MARKET_SOURCE_MAX_AGE_MINUTES,
    )
    packet_time = _timestamp(packet["decision_time"], "packet.decision_time")

    ledger.parent.mkdir(parents=True, exist_ok=True)
    canonical = _packet_json(packet)
    try:
        with ledger.open("a+", encoding="utf-8") as handle:
            try:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                raise ResearchError("research ledger is locked by another writer") from exc
            handle.seek(0)
            existing = handle.read()
            if existing and not existing.endswith("\n"):
                raise ResearchError("research ledger must end with a newline before append")
            packets = _validate_ledger_lines(existing.splitlines(), ledger, agent)
            for old_packet in packets:
                if old_packet["packet_id"] == packet["packet_id"]:
                    if _packet_json(old_packet) != canonical:
                        raise ResearchError(
                            f"packet_id {packet['packet_id']} already exists with different content"
                        )
                    return packet
            packet = validate_packet(
                packet,
                agent,
                market_source_max_age_minutes=market_source_max_age_minutes,
            )
            if not allow_candidates and any(
                item["assessment"] == "candidate"
                for item in packet["decision_support"]
            ):
                raise ResearchError(
                    "discovery-only runner cannot append candidate research because trusted "
                    "source retrieval is unavailable"
                )
            canonical = _packet_json(packet)
            if packets:
                latest = _timestamp(packets[-1]["decision_time"], "packet.decision_time")
                if packet_time <= latest:
                    raise ResearchError(
                        "packet.decision_time must be strictly later than the current ledger tail"
                    )
            handle.seek(0, os.SEEK_END)
            handle.write(canonical + "\n")
            handle.flush()
            os.fsync(handle.fileno())
            fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
    except OSError as exc:
        raise ResearchError(f"cannot append research ledger {ledger}: {exc}") from exc
    return packet


def require_current_candidate(
    root: Path,
    agent: str,
    symbol: str,
    now: datetime,
    timezone_name: str,
    *,
    thesis: str,
    invalidation: str,
    review_by: date,
    candidate_max_age_minutes: int = DEFAULT_CANDIDATE_MAX_AGE_MINUTES,
    market_source_max_age_minutes: int = DEFAULT_MARKET_SOURCE_MAX_AGE_MINUTES,
) -> dict[str, str]:
    """Return immutable evidence identity for the latest same-session candidate."""
    if now.tzinfo is None or now.utcoffset() is None:
        raise ResearchError("trusted now must include a timezone")
    if not SYMBOL_RE.fullmatch(symbol):
        raise ResearchError("symbol must be a canonical uppercase ticker")
    try:
        local_zone = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as exc:
        raise ResearchError(f"unknown policy timezone {timezone_name}") from exc
    candidate_max_age = _positive_minutes(
        candidate_max_age_minutes, "candidate_max_age_minutes"
    )
    market_source_max_age = _positive_minutes(
        market_source_max_age_minutes, "market_source_max_age_minutes"
    )
    packets = validate_ledger(ledger_path(root, agent), agent)
    today = now.astimezone(local_zone).date()
    current = [
        packet
        for packet in packets
        if packet["routine"] == "premarket"
        and _timestamp(packet["decision_time"], "packet.decision_time")
        .astimezone(local_zone)
        .date()
        == today
    ]
    if not current:
        raise ResearchError("no validated same-session premarket research packet")
    packet = current[-1]
    decision_time = _timestamp(packet["decision_time"], "packet.decision_time")
    if decision_time > now:
        raise ResearchError("latest same-session premarket packet is future-dated")
    if now - decision_time > candidate_max_age:
        raise ResearchError("latest same-session premarket packet is stale")
    market_cutoff = _timestamp(
        packet["market_data_cutoff"], "packet.market_data_cutoff"
    )
    if (
        market_cutoff > now
        or market_cutoff.astimezone(local_zone).date() != today
        or now - market_cutoff > candidate_max_age
    ):
        raise ResearchError("latest premarket market_data_cutoff is stale or future-dated")
    matches = [
        item
        for item in packet["decision_support"]
        if item["symbol"] == symbol and item["assessment"] == "candidate"
    ]
    if len(matches) != 1:
        raise ResearchError(
            f"latest same-session premarket packet does not contain one candidate for {symbol}"
        )
    decision = matches[0]
    source_by_id = {item["source_id"]: item for item in packet["sources"]}
    claim_by_id = {item["claim_id"]: item for item in packet["claims"]}
    inference_by_id = {
        item["inference_id"]: item for item in packet["inferences"]
    }
    supporting_claim_ids = {
        claim_id
        for inference_id in decision["supporting_inference_ids"]
        for claim_id in inference_by_id[inference_id]["claim_ids"]
        if claim_by_id[claim_id]["stance"] == "supports"
        and symbol in claim_by_id[claim_id]["symbols"]
        and not claim_by_id[claim_id]["limitations"]
    }
    execution_current_market_sources = {
        source_id
        for claim_id in supporting_claim_ids
        for source_id in claim_by_id[claim_id]["source_ids"]
        if source_by_id[source_id]["source_type"] == "exchange_market_data"
        and not source_by_id[source_id]["limitations"]
        and timedelta(0)
        <= now - _timestamp(source_by_id[source_id]["as_of"], "source.as_of")
        <= market_source_max_age
    }
    if not execution_current_market_sources:
        raise ResearchError(
            "latest candidate exchange-market evidence is stale at execution time"
        )
    if (
        decision["thesis"] != thesis
        or decision["invalidation"] != invalidation
        or decision["review_by"] != review_by.isoformat()
    ):
        raise ResearchError(
            "latest candidate thesis, invalidation, or review date does not match the planned buy"
        )
    return packet_identity(packet)
