#!/usr/bin/env python3
"""Programmatic loaders for public fluid-dynamics reference datasets.

Unblocks the DNS/RANS/ROM roadmap items that were previously gated on
email-request-only data (see docs/lectures/06_feasibility_balasubramanian.md).
All downloaded data lands in data/public_datasets/ (gitignored).

Honesty note on access mechanisms (verified live, not guessed):

  * Vreman channel-flow DNS  -- REAL, zero-auth, plain HTTP GET. Verified live.
  * Zenodo beta-VAE ROM data -- REAL, zero-auth public REST API + HTTP GET.
    Verified live. Files are large (211 MB / 31.7 GB); the CLI --verify check
    only confirms metadata reachability, it does not bulk-download by default.
  * JHTDB (Johns Hopkins Turbulence DB) -- the historical Python client
    (pyJHTDB) is ARCHIVED/DEPRECATED upstream ("no longer maintained, should
    not be used"). Its replacement (`giverny`) is designed for the SciServer
    cloud environment and effectively requires a free SciServer account/auth
    token -- this is NOT a clean zero-signup path. This module exposes a
    loader that requires JHTDB_AUTH_TOKEN and fails with a clear, actionable
    message (never silently) if it is unset, rather than pretending JHTDB is
    fully open like the other two.
  * KTH FLOW database -- the historical index page
    (flow.kth.se/flow-database/simulation-data-1.791810/) lists case
    descriptions only; no direct per-file download URL was found on that page,
    and it states the database relocated to www.lstm.tf.fau.de. No file URL is
    fabricated here -- this loader returns the verified case index and the
    (documented) relocated host for manual follow-up, and is intentionally NOT
    wired into automated download.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = REPO_ROOT / "data" / "public_datasets"
TIMEOUT = 20


@dataclass
class FetchResult:
    source: str
    ok: bool
    detail: str


def _http_head(url: str, timeout: int = TIMEOUT) -> tuple[int, dict]:
    req = urllib.request.Request(url, method="HEAD")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.status, dict(resp.headers)


def _http_download(url: str, dest: Path, timeout: int = TIMEOUT) -> int:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=timeout) as resp, open(dest, "wb") as f:
        total = 0
        while chunk := resp.read(1 << 16):
            f.write(chunk)
            total += len(chunk)
    return total


# --------------------------------------------------------------------------- #
# 1. Vreman channel-flow DNS -- verified, zero-auth, direct HTTP
# --------------------------------------------------------------------------- #
class VremanChannelDNS:
    """Direct-download helper for the Vreman & Kuerten channel-flow DNS statistics.

    Source: http://www.vremanresearch.nl/channel.html (Re_tau = 180, 590).
    No authentication required; files are plain-text statistics or a small
    zip bundle -- confirmed reachable via HTTP HEAD.
    """

    BASE_URL = "http://www.vremanresearch.nl"
    # A small, self-contained bundle (~0.3 MB) suitable for a quick smoke check.
    SAMPLE_BUNDLE = "Chan180_S2a_all.zip"
    SPECTRUM_FILE = "Chan180_S2_specx_u.txt"
    # Individual statistic files (basic velocity/pressure moments at Re_tau=180).
    SAMPLE_FILES = (
        "Chan180_S2a_basic_mean.txt",
        "Chan180_S2a_basic_rms.txt",
    )

    def __init__(self, dest_dir: Path = DATA_ROOT / "vreman_channel_dns") -> None:
        self.dest_dir = dest_dir

    def verify(self) -> FetchResult:
        try:
            status, headers = _http_head(f"{self.BASE_URL}/{self.SAMPLE_BUNDLE}")
            size = headers.get("Content-Length", "?")
            return FetchResult("vreman", status == 200, f"HTTP {status}, {size} bytes")
        except (urllib.error.URLError, TimeoutError) as e:
            return FetchResult("vreman", False, f"unreachable: {e}")

    def fetch_sample(self) -> Path:
        """Download the small statistics bundle for Re_tau=180 (S2a case)."""
        dest = self.dest_dir / self.SAMPLE_BUNDLE
        n = _http_download(f"{self.BASE_URL}/{self.SAMPLE_BUNDLE}", dest)
        print(f"  downloaded {dest} ({n} bytes)")
        return dest

    def fetch_file(self, filename: str) -> Path:
        """Download a named Vreman file (e.g., spectra/statistics text files)."""
        if not filename or "/" in filename or "\\" in filename:
            raise ValueError("filename must be a base name with no path separators")
        dest = self.dest_dir / filename
        n = _http_download(f"{self.BASE_URL}/{filename}", dest)
        print(f"  downloaded {dest} ({n} bytes)")
        return dest


# --------------------------------------------------------------------------- #
# 2. Zenodo beta-VAE ROM dataset -- verified, zero-auth, public REST API
# --------------------------------------------------------------------------- #
class ZenodoROMDataset:
    """Loader for the beta-VAE + transformer ROM dataset (Solera-Rico et al., 2024).

    Source: https://zenodo.org/records/10501216 (DOI 10.5281/zenodo.10501216).
    Zenodo's REST API (https://zenodo.org/api/records/<id>) is public and
    requires no authentication for metadata or file download.
    """

    RECORD_ID = "10501216"
    API_URL = f"https://zenodo.org/api/records/{RECORD_ID}"

    def __init__(self, dest_dir: Path = DATA_ROOT / "zenodo_beta_vae_rom") -> None:
        self.dest_dir = dest_dir

    def _metadata(self) -> dict:
        req = urllib.request.Request(self.API_URL)
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            return json.load(resp)

    def verify(self) -> FetchResult:
        try:
            meta = self._metadata()
            files = meta.get("files", [])
            listing = ", ".join(f"{f['key']} ({f['size']:,}B)" for f in files)
            return FetchResult("zenodo_rom", bool(files), listing or "no files listed")
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as e:
            return FetchResult("zenodo_rom", False, f"unreachable: {e}")

    def list_files(self) -> list[dict]:
        return self._metadata().get("files", [])

    def fetch_file(self, key: str) -> Path:
        """Download one named file from the record (files are large: 211 MB-31.7 GB)."""
        for f in self.list_files():
            if f["key"] == key:
                url = f["links"]["self"]
                dest = self.dest_dir / key
                n = _http_download(url, dest)
                print(f"  downloaded {dest} ({n} bytes)")
                return dest
        raise LookupError(f"'{key}' not found in Zenodo record {self.RECORD_ID}")


# --------------------------------------------------------------------------- #
# 3. JHTDB -- requires a free auth token; NOT zero-signup, fails loudly
# --------------------------------------------------------------------------- #
class JHTDBLoader:
    """Loader for the Johns Hopkins Turbulence Database.

    IMPORTANT: pyJHTDB (the historical client) is archived/deprecated
    upstream. Its replacement, `giverny` (github.com/sciserver/giverny), is
    built around the SciServer cloud environment and requires a free
    SciServer account / auth token. This is NOT a clean zero-signup path --
    unlike Vreman and Zenodo above, this loader cannot verify data access
    without a token you must obtain yourself, and it will not pretend
    otherwise. Get a token at: http://turbulence.pha.jhu.edu/help/authtoken.aspx
    """

    TOKEN_ENV_VAR = "JHTDB_AUTH_TOKEN"

    def verify(self) -> FetchResult:
        token = os.environ.get(self.TOKEN_ENV_VAR)
        if not token:
            return FetchResult(
                "jhtdb", False,
                f"SKIPPED -- requires a free auth token in ${self.TOKEN_ENV_VAR} "
                "(pyJHTDB is deprecated; migrate to 'giverny' + a SciServer "
                "account: http://turbulence.pha.jhu.edu/help/authtoken.aspx)",
            )
        # A token is present, but we do not fabricate a query here -- the
        # giverny/pyJHTDB client libraries own the actual protocol.
        return FetchResult("jhtdb", True, "token present (client library not vendored)")


# --------------------------------------------------------------------------- #
# 4. KTH FLOW database -- no verified direct file URL; index-only, no fetch
# --------------------------------------------------------------------------- #
class KTHFlowIndex:
    """Documented pointer to the KTH FLOW simulation database.

    IMPORTANT: the historical index page lists case descriptions but exposes
    no direct per-file download URL, and states the database has relocated.
    This loader intentionally does NOT fabricate a download link -- it
    returns the verified index/redirect information for manual follow-up.
    """

    LEGACY_INDEX_URL = "https://www.flow.kth.se/flow-database/simulation-data-1.791810/"
    RELOCATED_HOST = "https://www.lstm.tf.fau.de/database/simulation-database/"
    KNOWN_CASES = (
        "Turbulent boundary layers up to Re_theta=4300 (DNS) / 8300 (LES)",
        "Turbulent boundary layers with pressure gradients (Bobke et al. 2017)",
        "Turbulent pipe flow, Re_tau=180,360,550,1000 (El Khoury et al. 2013)",
        "LES of turbulent flow around a NACA4412/NACA0012 wing section",
    )

    def verify(self) -> FetchResult:
        try:
            status, _ = _http_head(self.LEGACY_INDEX_URL)
        except (urllib.error.URLError, TimeoutError) as e:
            return FetchResult("kth_flow", False, f"unreachable: {e}")
        return FetchResult(
            "kth_flow", False,  # False: no automated data fetch is available
            f"index reachable (HTTP {status}) but no direct file URL published; "
            f"relocated to {self.RELOCATED_HOST} -- manual follow-up required",
        )


# --------------------------------------------------------------------------- #
# CLI
# --------------------------------------------------------------------------- #
def _print_result(r: FetchResult) -> None:
    tag = "OK  " if r.ok else "WARN"
    print(f"  [{tag}] {r.source:12s} {r.detail}")


def verify_all() -> int:
    print("Verifying public dataset access (no downloads, metadata/reachability only)...")
    results = [
        VremanChannelDNS().verify(),
        ZenodoROMDataset().verify(),
        JHTDBLoader().verify(),
        KTHFlowIndex().verify(),
    ]
    for r in results:
        _print_result(r)

    hard_sources = {"vreman", "zenodo_rom"}  # the two zero-auth, fully-verified sources
    hard_ok = all(r.ok for r in results if r.source in hard_sources)
    print()
    if hard_ok:
        print("Zero-auth sources (Vreman DNS, Zenodo ROM) are reachable. JHTDB/KTH require")
        print("manual follow-up (token / relocated host) -- see WARN details above.")
    else:
        print("One or more zero-auth sources failed -- check network connectivity.")
    return 0 if hard_ok else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Fetch public fluid-dynamics reference datasets.")
    parser.add_argument("--verify", action="store_true", help="Check reachability of all sources (no bulk download).")
    parser.add_argument("--fetch-vreman-sample", action="store_true", help="Download the small Vreman Re_tau=180 bundle.")
    parser.add_argument("--fetch-vreman-file", metavar="NAME", help="Download a named Vreman file (e.g., Chan180_S2_specx_u.txt).")
    parser.add_argument("--fetch-zenodo-file", metavar="KEY", help="Download a named file from the Zenodo ROM record.")
    args = parser.parse_args()

    if args.verify or not any(vars(args).values()):
        return verify_all()
    if args.fetch_vreman_sample:
        VremanChannelDNS().fetch_sample()
    if args.fetch_vreman_file:
        VremanChannelDNS().fetch_file(args.fetch_vreman_file)
    if args.fetch_zenodo_file:
        ZenodoROMDataset().fetch_file(args.fetch_zenodo_file)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
