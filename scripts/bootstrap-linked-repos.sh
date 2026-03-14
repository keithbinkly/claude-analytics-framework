#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPOS_DIR="${ROOT_DIR}/repos"

DBT_ENTERPRISE_SRC="/Users/kbinkly/git-repos/dbt_projects/dbt-enterprise"
DBT_AGENT_SRC="/Users/kbinkly/git-repos/dbt-agent"
DATA_CENTERED_SRC="/Users/kbinkly/git-repos/data-centered"

mkdir -p "${REPOS_DIR}"

link_repo() {
  local source_path="$1"
  local link_name="$2"
  local target_path="${REPOS_DIR}/${link_name}"

  if [[ ! -e "${source_path}" ]]; then
    echo "Skipping ${link_name}: source not found at ${source_path}"
    return 0
  fi

  ln -sfn "${source_path}" "${target_path}"
  echo "Linked ${link_name} -> ${source_path}"
}

echo "Creating CAF linked-repo convenience symlinks..."

link_repo "${DBT_ENTERPRISE_SRC}" "dbt-enterprise"
link_repo "${DBT_AGENT_SRC}" "dbt-agent"
link_repo "${DATA_CENTERED_SRC}" "data-centered"

echo
echo "Done."
echo "These symlinks are a local convenience layer only."
echo "Canonical routing still lives in:"
echo "  - AGENT_ENTRYPOINT.md"
echo "  - .claude/manifests/workspace-manifest.yaml"
echo "  - .claude/manifests/repo-adapters.yaml"
