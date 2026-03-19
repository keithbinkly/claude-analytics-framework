#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
REPOS_DIR="${ROOT_DIR}/repos"

# Load optional local overrides before setting defaults
if [[ -f "${ROOT_DIR}/.env.local" ]]; then
  # shellcheck disable=SC1091
  source "${ROOT_DIR}/.env.local"
fi

# Default: check nested first (inside workspace), then sibling directories
if [[ -z "${DBT_ENTERPRISE_SRC:-}" ]]; then
  if [[ -d "${ROOT_DIR}/dbt-enterprise" ]]; then
    DBT_ENTERPRISE_SRC="${ROOT_DIR}/dbt-enterprise"
  else
    DBT_ENTERPRISE_SRC="$(cd "${ROOT_DIR}/.." 2>/dev/null && pwd)/dbt-enterprise"
  fi
fi

if [[ -z "${DBT_AGENT_SRC:-}" ]]; then
  if [[ -d "${ROOT_DIR}/dbt-agent" ]]; then
    DBT_AGENT_SRC="${ROOT_DIR}/dbt-agent"
  else
    DBT_AGENT_SRC="$(cd "${ROOT_DIR}/.." 2>/dev/null && pwd)/dbt-agent"
  fi
fi

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

echo "Creating analytics-workspace linked-repo convenience symlinks..."

link_repo "${DBT_ENTERPRISE_SRC}" "dbt-enterprise"
link_repo "${DBT_AGENT_SRC}" "dbt-agent"

# Optional: link data-centered if DATA_CENTERED_SRC is set in .env.local
if [[ -n "${DATA_CENTERED_SRC:-}" ]]; then
  link_repo "${DATA_CENTERED_SRC}" "data-centered"
fi

echo
echo "Done."
echo "These symlinks are a local convenience layer only."
echo "Canonical routing still lives in:"
echo "  - AGENT_ENTRYPOINT.md"
echo "  - .claude/manifests/workspace-manifest.yaml"
echo "  - .claude/manifests/repo-adapters.yaml"
