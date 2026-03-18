"""
ToolGuard Decorators

Enforce prerequisite completion before tool execution.
Converts "should" recommendations into "must" requirements.

Usage:
    @require_context
    def my_tool():
        ...  # Will fail if context not retrieved

    @require_compile
    def run_model():
        ...  # Will fail if compile not done first
"""

import functools
from typing import Callable, Any, Optional
from .session import load_session, save_session


class ToolGuardError(Exception):
    """Raised when a tool prerequisite is not met."""

    def __init__(self, message: str, missing_step: str, remediation: str):
        self.message = message
        self.missing_step = missing_step
        self.remediation = remediation
        super().__init__(self.format_error())

    def format_error(self) -> str:
        return f"""
🚫 TOOL GUARD: {self.message}

Missing Step: {self.missing_step}
Remediation: {self.remediation}

This is a mechanical enforcement of the tool invocation contract.
Complete the required step before proceeding.
"""


def require_context(func: Callable) -> Callable:
    """
    Decorator: Tool fails if context not retrieved.

    Ensures get_context() was called before any action tool.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        session = load_session()

        if not session.state.context_retrieved:
            raise ToolGuardError(
                message="Context not retrieved",
                missing_step="get_context()",
                remediation="Call get_context(query) to retrieve context before taking action.",
            )

        # Log tool invocation
        session.log_tool_event(func.__name__, success=True, details={"guard": "context"})
        save_session(session)

        return func(*args, **kwargs)

    return wrapper


def require_preflight(func: Callable) -> Callable:
    """
    Decorator: Tool fails if preflight checklist not complete.

    For migration tasks, ensures Phase 1-3 artifacts exist.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        session = load_session()

        # Only enforce for migration tasks
        if session.task_type == "migration" and not session.state.preflight_complete:
            raise ToolGuardError(
                message="Pre-flight checklist not complete",
                missing_step="Pre-flight validation",
                remediation="""Complete the pre-flight checklist:
1. Load migration-quick-reference.md
2. Load canonical-models-registry.md
3. Load folder-structure-and-naming.md
4. Load qa-validation-checklist.md
5. Mark preflight complete: session.state.preflight_complete = True""",
            )

        session.log_tool_event(func.__name__, success=True, details={"guard": "preflight"})
        save_session(session)

        return func(*args, **kwargs)

    return wrapper


def require_canonical_check(func: Callable) -> Callable:
    """
    Decorator: Tool fails if canonical model check not done.

    Ensures get_related_models() was called before building new models.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        session = load_session()

        # Enforce for migration and architecture tasks
        if session.task_type in ["migration", "architecture"] and not session.state.canonical_checked:
            raise ToolGuardError(
                message="Canonical model check not performed",
                missing_step="get_related_models()",
                remediation="""Check for existing canonical models before building new:
1. Call get_related_models(domain) via MCP
2. Review existing models for reuse (target: 75-90%)
3. Mark complete: session.state.canonical_checked = True""",
            )

        session.log_tool_event(func.__name__, success=True, details={"guard": "canonical_check"})
        save_session(session)

        return func(*args, **kwargs)

    return wrapper


def require_compile(func: Callable) -> Callable:
    """
    Decorator: Tool fails if compile not done before run.

    Ensures dbt compile succeeds before dbt run.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        session = load_session()

        if not session.state.compiled:
            raise ToolGuardError(
                message="Model not compiled",
                missing_step="dbt compile",
                remediation="""Compile before run:
1. Run: dbt compile --select <model>
2. Verify SQL is valid
3. Mark complete: session.state.compiled = True""",
            )

        session.log_tool_event(func.__name__, success=True, details={"guard": "compile"})
        save_session(session)

        return func(*args, **kwargs)

    return wrapper


def require_verification(func: Callable) -> Callable:
    """
    Decorator: Tool fails if verification not done.

    For QA tasks, ensures validation queries were run.
    """

    @functools.wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        session = load_session()

        if session.task_type == "qa" and not session.state.verified:
            raise ToolGuardError(
                message="Verification not complete",
                missing_step="QA validation",
                remediation="""Run QA validation:
1. Execute Template 1 (Granular Variance)
2. Verify variance < 0.1%
3. Mark complete: session.state.verified = True""",
            )

        session.log_tool_event(func.__name__, success=True, details={"guard": "verification"})
        save_session(session)

        return func(*args, **kwargs)

    return wrapper


# Convenience: mark state transitions
def mark_context_retrieved() -> None:
    """Mark that context has been retrieved."""
    session = load_session()
    session.state.context_retrieved = True
    session.log_tool_event("get_context", success=True)
    save_session(session)


def mark_preflight_complete() -> None:
    """Mark that preflight checklist is complete."""
    session = load_session()
    session.state.preflight_complete = True
    session.log_tool_event("preflight", success=True)
    save_session(session)


def mark_canonical_checked() -> None:
    """Mark that canonical models were checked."""
    session = load_session()
    session.state.canonical_checked = True
    session.log_tool_event("canonical_check", success=True)
    save_session(session)


def mark_compiled() -> None:
    """Mark that model was compiled successfully."""
    session = load_session()
    session.state.compiled = True
    session.log_tool_event("compile", success=True)
    save_session(session)


def mark_verified() -> None:
    """Mark that verification/QA is complete."""
    session = load_session()
    session.state.verified = True
    session.log_tool_event("verify", success=True)
    save_session(session)
