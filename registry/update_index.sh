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

echo "📁  Adding local example profiles…"
# Add local examples first
for example_file in "$ROOT_DIR"/examples/*.json; do
  if [[ -f "$example_file" ]]; then
    echo "- Processing $(basename "$example_file")"
    if ajv validate -c ajv-formats -s "$SCHEMA" -d "$example_file" &>/dev/null; then
      echo "  ✅ Valid example - adding to registry"
      # Create a URL for the example file in the GitHub repo
      example_url="https://raw.githubusercontent.com/minuetai/agent-profile-schema/main/examples/$(basename "$example_file")"
      jq '{url: $URL, name, skills, safety_grade, endpoint_url} | .url=$URL' \
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
    
    # Check if repo has agent_profile_v0.1.json file
    if gh api "/repos/$repo_name/contents/agent_profile_v0.1.json" --jq '.download_url' 2>/dev/null; then
      download_url=$(gh api "/repos/$repo_name/contents/agent_profile_v0.1.json" --jq '.download_url' 2>/dev/null)
      echo "    ✅ Found profile at $download_url"
      
      # Download and validate the profile
      curl -sL "$download_url" -o profile.json
      
      if ajv validate -c ajv-formats -s "$SCHEMA" -d profile.json &>/dev/null; then
        echo "    ✅ Valid profile - adding to registry"
        jq '{url: $URL, name, skills, safety_grade, endpoint_url} | .url=$URL' \
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
