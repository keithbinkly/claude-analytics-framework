#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

ok() {
  echo "[OK] $1"
}

warn() {
  echo "[WARN] $1"
}

fail() {
  echo "[FAIL] $1"
}

check_file() {
  local path="$1"
  local label="$2"
  if [[ -f "${ROOT_DIR}/${path}" ]]; then
    ok "${label}: ${path}"
  else
    fail "${label}: missing ${path}"
  fi
}

check_dir() {
  local path="$1"
  local label="$2"
  if [[ -d "${ROOT_DIR}/${path}" ]]; then
    ok "${label}: ${path}"
  else
    fail "${label}: missing ${path}"
  fi
}

echo "CAF workspace readiness check"
echo

check_file "AGENT_ENTRYPOINT.md" "Agent-neutral bootstrap"
check_file "README.md" "Root README"
check_file "CLAUDE.md" "Claude workspace contract"
check_file ".claude/manifests/workspace-manifest.yaml" "Workspace manifest"
check_file ".claude/manifests/repo-adapters.yaml" "Repo adapters"
check_file ".claude/manifests/workflow-contracts.yaml" "Workflow contracts"
check_file ".claude/manifests/ccv3-dependencies.yaml" "CCV3 dependency manifest"
check_file "knowledge/platform/planning/shared-agent-platform-monorepo-plan.md" "Migration plan"
check_dir "knowledge/domains" "Domain knowledge root"
check_file "repos/README.md" "Linked repos guide"

echo
echo "Linked repo visibility"

for repo_name in dbt-enterprise dbt-agent data-centered; do
  repo_path="${ROOT_DIR}/repos/${repo_name}"
  if [[ -L "${repo_path}" || -d "${repo_path}" ]]; then
    ok "Local convenience entry present: repos/${repo_name}"
  else
    warn "Local convenience entry missing: repos/${repo_name} (run ./scripts/bootstrap-linked-repos.sh if desired)"
  fi
done

echo
echo "MCP readiness hints"

if [[ -f "${ROOT_DIR}/.env" ]]; then
  env_var_count="$(grep -E '^[A-Za-z0-9_]+=' "${ROOT_DIR}/.env" | wc -l | tr -d ' ')"
  ok ".env present with ${env_var_count} configured variable lines"
else
  warn ".env not found (copy .env.example to .env if this workspace needs dbt MCP locally)"
fi

if [[ -f "${ROOT_DIR}/.claude/settings.json" ]]; then
  if grep -q 'dbt@dbt-agent-marketplace' "${ROOT_DIR}/.claude/settings.json"; then
    ok "dbt MCP plugin reference found in .claude/settings.json"
  else
    warn "dbt MCP plugin reference not found in .claude/settings.json"
  fi
else
  warn ".claude/settings.json not found"
fi

echo
echo "Notes"
echo "- CAF is the shared control plane."
echo "- dbt CLI should run from dbt-enterprise, not CAF root."
echo "- dbt-agent remains the intact fallback reference during migration."
