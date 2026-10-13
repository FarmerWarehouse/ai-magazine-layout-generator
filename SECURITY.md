# Security Policy

## Supported versions

| Version | Supported |
|---------|-----------|
| 0.4.x   | yes       |
| 0.3.x   | security fixes only |
| < 0.3   | no        |

## Reporting a vulnerability

Email `security@ai-magazine-layout-generator.dev` with:

- A description of the issue.
- Steps to reproduce (a minimal issue JSON is ideal).
- Impact: does it allow arbitrary file write via a malicious preset?
  Does the font downloader fetch from an untrusted mirror? Does the
  LLM layout advisor leak issue content to a third-party endpoint?

We aim to acknowledge within 72 hours and patch critical issues within
14 days.

## Threat model

This tool parses user-supplied issue JSON, preset JSON, and font files.
The main risks are:

1. **Preset injection** — a malicious preset that escapes the config
   directory. The loader validates paths against `config/presets/` root.
2. **Font parsing** — TTF/OTF parsing is delegated to `fontTools`. Keep it
   updated. We never execute font hinting bytecode.
3. **LLM advisor egress** — the advisor is opt-in. When enabled, issue
   text is sent to the configured endpoint. Users are warned in the UI.
4. **Export path traversal** — output paths are resolved and checked
   against the chosen output root before writing.

## Out of scope

- Denial of service from absurdly large issue JSON (we cap at 64MB).
- Vulnerabilities in third-party PDF backends (report upstream).