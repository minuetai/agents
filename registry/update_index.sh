#!/usr/bin/env bash
#
# Crawl public GitHub for AgentProfile docs, validate them, and
# assemble a lightweight index (name, skills, safety_grade, URL).

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCHEMA="$ROOT_DIR/agent_profile_v0.1.json"
INDEX="$ROOT_DIR/registry/profiles_index.json"
TMP=$(mktemp)
> "$TMP"

echo "🔎  Searching GitHub code for agent profiles…"
# Uses the GitHub Search API via gh CLI. Requires GH_TOKEN or GITHUB_TOKEN in CI.
gh api search/code -f q='filename:agent_profile_v0.1.json' --jq '.items[].url' |
while read -r api_url; do
  raw_url="${api_url/github.com/raw.githubusercontent.com}"
  raw_url="${raw_url/\/blob\//\/}"
  echo "- Fetching $raw_url"
  curl -sL "$raw_url" -o profile.json

  if ajv validate -s "$SCHEMA" -d profile.json &>/dev/null; then
    jq '{url: $URL, name, skills, safety_grade, endpoint_url} | .url=$URL' \
       --arg URL "$raw_url" profile.json >> "$TMP"
  else
    echo "  ❌ invalid JSON—skipping"
  fi
done

# Build array JSON
jq -s '.' "$TMP" > "$INDEX"
rm "$TMP"
echo "✅  Wrote $(jq '. | length' "$INDEX") valid profiles to $INDEX"
