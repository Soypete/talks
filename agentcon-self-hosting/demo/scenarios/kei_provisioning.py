"""Scenario: provision read-only CRM access against an in-memory mock (a simulation, not the real Kei API).

Every step needs an opaque id returned by the previous one, so calls cannot be batched or guessed.
"""

from __future__ import annotations

import random
import string
from typing import Any

from scenario import Scenario

TASK = (
    "Give the data-science group read-only access to the CRM connector. Alice is in data-science, "
    "Bob is not. Verify: alice can read, alice cannot write, bob cannot read. Then call done."
)

SYSTEM_PROMPT = """You are an access-provisioning assistant working against a mock admin API.
Ids (grp_..., con_..., pol_...) are opaque and come ONLY from earlier tool results; never invent or
guess one, and no tool looks ids up by name. Call exactly one tool at a time and wait for its result
before the next call. Respond only with tool calls, never plain text. Verify with authorize before
you call done; if you change anything after verifying, verify again."""

REQUIRED_STEPS = ["create_group", "add_member", "create_connector", "create_policy", "authorize"]
TERMINAL_TOOL = "done"

NUDGES = {
    "retry": "That was not a valid tool call. Respond with exactly one tool call from the allowed tools.",
    "step_blocked": "You cannot finish yet. Create, provision and verify first, then call done.",
    "prerequisite": "A step was skipped. Order: create_group, add_member, create_connector, create_policy, authorize, done.",
    "fatal": "Too many invalid responses.",
}

KINDS = ("http_api", "github", "google_drive")
ACTIONS = ("read", "write")
CHECKS = (("alice", "read"), ("alice", "write"), ("bob", "read"))
EXPECTED = ("allow", "deny", "deny")


def tool_schemas() -> list[dict[str, Any]]:
    def fn(tool: str, desc: str, /, **props: str) -> dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": tool,
                "description": desc,
                "parameters": {
                    "type": "object",
                    "properties": {k: {"type": "string", "description": v} for k, v in props.items()},
                    "required": list(props),
                },
            },
        }

    return [
        fn("create_group", "Create a group. Returns its group id.", name="group name"),
        fn("add_member", "Add a user to a group.", group_id="id from create_group", user="user name"),
        fn(
            "create_connector",
            "Create a data connector. Returns its connector id.",
            name="connector name",
            kind="http_api, github or google_drive",
        ),
        fn(
            "create_policy",
            "Grant a group actions on a connector. Returns its policy id.",
            group_id="id from create_group",
            connector_id="id from create_connector",
            actions="comma-separated: read and/or write",
        ),
        fn("list_policies", "List existing policies with their ids."),
        fn(
            "authorize",
            "Check whether a user may perform an action on a connector. Returns allow or deny.",
            user="user name",
            connector_id="id from create_connector",
            action="read or write",
        ),
        fn("done", "Finish the task with a short summary.", summary="what was provisioned and verified"),
    ]


class ProvisioningWorkspace:
    """Mock admin API state. Ids are seeded: same seed, same ids; unguessable from the task text."""

    def __init__(self, seed: int = 7) -> None:
        self._rngs = {p: random.Random(f"{seed}:{p}") for p in ("grp", "con", "pol")}
        self.groups: dict[str, dict[str, Any]] = {}
        self.connectors: dict[str, dict[str, str]] = {}
        self.policies: dict[str, dict[str, Any]] = {}
        self.checks: dict[tuple[str, str, str], tuple[str, int]] = {}  # (user, con, action) -> (outcome, version)
        self.version = 0
        self.steps: list[str] = []
        self.final: str | None = None

    def _new_id(self, prefix: str) -> str:
        alphabet = string.ascii_lowercase + string.digits
        return f"{prefix}_" + "".join(self._rngs[prefix].choice(alphabet) for _ in range(6))

    def run(self, tool: str, args: dict[str, Any]) -> tuple[str, str | None]:
        if tool not in {t["function"]["name"] for t in tool_schemas()}:
            return "", f"unknown tool {tool!r}"
        output, error = getattr(self, f"_tool_{tool}")(args)
        if error is None:
            self.steps.append(tool)
        return output, error

    @staticmethod
    def _s(args: dict[str, Any], key: str) -> str:
        return str(args.get(key, "")).strip()

    def _tool_create_group(self, args: dict[str, Any]) -> tuple[str, str | None]:
        name = self._s(args, "name")
        if not name:
            return "", "create_group requires a non-empty 'name'"
        if any(g["name"] == name for g in self.groups.values()):
            return "", f"group {name!r} already exists"
        gid = self._new_id("grp")
        self.groups[gid] = {"name": name, "members": set()}
        self.version += 1
        return f"created group {name!r} with id {gid}", None

    def _tool_add_member(self, args: dict[str, Any]) -> tuple[str, str | None]:
        gid, user = self._s(args, "group_id"), self._s(args, "user").lower()
        if gid not in self.groups:
            return "", f"unknown group_id {gid!r}; use the id returned by create_group"
        if not user:
            return "", "add_member requires a non-empty 'user'"
        self.groups[gid]["members"].add(user)
        self.version += 1
        return f"added {user} to {self.groups[gid]['name']} ({gid})", None

    def _tool_create_connector(self, args: dict[str, Any]) -> tuple[str, str | None]:
        name, kind = self._s(args, "name"), self._s(args, "kind")
        if kind not in KINDS:
            return "", f"invalid kind {kind!r}; must be one of {', '.join(KINDS)}"
        if not name:
            return "", "create_connector requires a non-empty 'name'"
        if any(c["name"] == name for c in self.connectors.values()):
            return "", f"connector {name!r} already exists"
        cid = self._new_id("con")
        self.connectors[cid] = {"name": name, "kind": kind}
        self.version += 1
        return f"created {kind} connector {name!r} with id {cid}", None

    def _tool_create_policy(self, args: dict[str, Any]) -> tuple[str, str | None]:
        gid, cid = self._s(args, "group_id"), self._s(args, "connector_id")
        if gid not in self.groups:
            return "", f"unknown group_id {gid!r}; use the id returned by create_group"
        if cid not in self.connectors:
            return "", f"unknown connector_id {cid!r}; use the id returned by create_connector"
        parts = [a.strip().lower() for a in self._s(args, "actions").split(",") if a.strip()]
        if not parts or any(a not in ACTIONS for a in parts):
            return "", "invalid actions; use a comma-separated list of read and/or write"
        pid = self._new_id("pol")
        self.policies[pid] = {"group_id": gid, "connector_id": cid, "actions": frozenset(parts)}
        self.version += 1
        return f"created policy with id {pid}", None

    def _tool_list_policies(self, _args: dict[str, Any]) -> tuple[str, str | None]:
        if not self.policies:
            return "no policies", None
        return "\n".join(
            f"{pid}: group {p['group_id']} connector {p['connector_id']} actions {','.join(sorted(p['actions']))}"
            for pid, p in self.policies.items()
        ), None

    def _decide(self, user: str, cid: str, action: str) -> str:
        granting = [p for p in self.policies.values() if p["connector_id"] == cid]
        mine = [p for p in granting if user in self.groups[p["group_id"]]["members"]]
        if not mine:
            return f"deny: {user} is not in any group with a policy on {cid}"
        if not any(action in p["actions"] for p in mine):
            return f"deny: no policy grants {action} on {cid} to {user}"
        return "allow"

    def _tool_authorize(self, args: dict[str, Any]) -> tuple[str, str | None]:
        user, cid, action = self._s(args, "user").lower(), self._s(args, "connector_id"), self._s(args, "action").lower()
        if cid not in self.connectors:
            return "", f"unknown connector_id {cid!r}; use the id returned by create_connector"
        if action not in ACTIONS:
            return "", "invalid action; must be read or write"
        outcome = self._decide(user, cid, action)
        self.checks[(user, cid, action)] = (outcome, self.version)
        return outcome, None

    def _tool_done(self, args: dict[str, Any]) -> tuple[str, str | None]:
        if not self.policies:
            return "", "missing_steps: create_policy"
        summary = self._s(args, "summary")
        if not summary:
            return "", "done requires a non-empty 'summary'"
        crm = self._crm()
        if crm is None:
            return "", "unverified: no connector named crm of kind http_api exists; the task needs one"
        stale = [
            f"{u} {a}"
            for u, a in CHECKS
            if self.checks.get((u, crm, a), ("", -1))[1] != self.version
        ]
        if stale:
            return "", "unverified: run authorize again (after your last change) for " + ", ".join(stale)
        self.final = summary
        return "accepted", None

    def _crm(self) -> str | None:
        for cid, c in self.connectors.items():
            if c["name"].strip().lower() == "crm" and c["kind"] == "http_api":
                return cid
        return None

    def score(self) -> float:
        groups = [(gid, g) for gid, g in self.groups.items() if g["name"] == "data-science"]
        crm = self._crm()
        a = len(groups) == 1 and "alice" in groups[0][1]["members"] and "bob" not in groups[0][1]["members"]
        c = False
        if len(groups) == 1 and crm is not None:
            linked = [p for p in self.policies.values() if p["group_id"] == groups[0][0] and p["connector_id"] == crm]
            c = len(linked) == 1 and linked[0]["actions"] == frozenset({"read"})
        d = crm is not None and tuple(self.checks.get((u, crm, act), ("", 0))[0].split(":")[0] for u, act in CHECKS) == EXPECTED
        return 0.25 * (a + (crm is not None) + c + d)


def make_scenario(seed: int = 7) -> Scenario:
    return Scenario(
        name="kei_provisioning",
        system_prompt=SYSTEM_PROMPT,
        task=TASK,
        tools=tool_schemas(),
        new_workspace=lambda: ProvisioningWorkspace(seed),
        required_steps=REQUIRED_STEPS,
        terminal_tool=TERMINAL_TOOL,
        prerequisites=[
            {"tool": "add_member", "requires": "create_group"},
            {"tool": "create_policy", "requires": "create_connector"},
            {"tool": "create_policy", "requires": "add_member"},
            {"tool": "authorize", "requires": "create_policy"},
        ],
        nudges=NUDGES,
    )


def solve_script(seed: int = 7) -> list[tuple[str, dict[str, Any]]]:
    """A correct call sequence; ids are learned by running a throwaway workspace."""
    ws = ProvisioningWorkspace(seed)
    script: list[tuple[str, dict[str, Any]]] = []

    def step(tool: str, **args: str) -> str:
        out, err = ws.run(tool, args)
        assert err is None, err
        script.append((tool, args))
        return out.rsplit(" ", 1)[-1] if tool.startswith("create_") else out

    gid = step("create_group", name="data-science")
    step("add_member", group_id=gid, user="alice")
    cid = step("create_connector", name="crm", kind="http_api")
    step("create_policy", group_id=gid, connector_id=cid, actions="read")
    for user, action in CHECKS:
        step("authorize", user=user, connector_id=cid, action=action)
    step("done", summary="data-science has read-only access to crm; alice read allowed, alice write and bob read denied")
    return script


SCENARIO = make_scenario()
