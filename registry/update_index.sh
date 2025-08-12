#!/usr/bin/env bash
#
# Crawl public GitHub for AgentProfile docs, validate them, and
# assemble a lightweight index (name, skills, safety_grade, URL).

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCHEMA="$ROOT_DIR/agent_profile_v1.0.json"
INDEX="$ROOT_DIR/registry/profiles_index.json"
TMP=$(mktemp)
> "$TMP"

echo "📁  Adding local example profiles…"
# Add local examples first
for example_file in "$ROOT_DIR"/examples/*.json; do
  if [[ -f "$example_file" ]]; then
    echo "- Processing $(basename "$example_file")"
    if ajv validate -c ajv-formats -s "$SCHEMA" -d "$example_file" &>/dev/null; then
      echo "  ✅ Valid example - adding to registry"
      # Create a URL for the example file in the GitHub repo
      example_url="https://raw.githubusercontent.com/cialint/agent-profile-schema/main/examples/$(basename "$example_file")"
      jq '{url: $URL, name, skills, safety_grade, endpoint_url, cost_per_call_usd, average_latency_ms, evals, publisher} | .url=$URL' \
         --arg URL "$example_url" "$example_file" >> "$TMP"
    else
      echo "  ❌ Invalid example - skipping"
    fi
  fi
done

echo "🔎  Searching GitHub repositories for agent profiles…"
# Search repositories by topic, then check each for agent profile files
topics=("ai-agent" "autonomous-agent" "llm-agent" "agent-profile")

for topic in "${topics[@]}"; do
  echo "- Searching repos with topic: $topic"
  gh api "/search/repositories?q=topic:$topic" --jq '.items[].full_name' |
  while read -r repo_name; do
    echo "  - Checking $repo_name"
    
    # Check for both v1.0 and v0.1 files (during transition period)
    found_profile=false
    
    # Try v1.0 first
    if download_url=$(gh api "/repos/$repo_name/contents/agent_profile_v1.0.json" --jq '.download_url' 2>/dev/null) && [[ "$download_url" != "null" ]]; then
      schema_file="$ROOT_DIR/agent_profile_v1.0.json"
      found_profile=true
    # Fall back to v0.1
    elif download_url=$(gh api "/repos/$repo_name/contents/agent_profile_v0.1.json" --jq '.download_url' 2>/dev/null) && [[ "$download_url" != "null" ]]; then
      schema_file="$ROOT_DIR/agent_profile_v0.1.json"
      found_profile=true
    fi
    
    if [ "$found_profile" = true ]; then
      echo "    ✅ Found profile at $download_url"
      
      # Download and validate the profile
      curl -sL "$download_url" -o profile.json
      
      if ajv validate -c ajv-formats -s "$schema_file" -d profile.json &>/dev/null; then
        echo "    ✅ Valid profile - adding to registry"
        jq '{url: $URL, name, skills, safety_grade, endpoint_url, cost_per_call_usd, average_latency_ms, evals, publisher} | .url=$URL' \
           --arg URL "$download_url" profile.json >> "$TMP"
      else
        echo "    ❌ Invalid JSON—skipping"
      fi
    fi
  done
done

# Build array JSON
jq -s '.' "$TMP" > "$INDEX"
rm "$TMP"
echo "✅  Wrote $(jq '. | length' "$INDEX") valid profiles to $INDEX"
