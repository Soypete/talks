"""Corrected access-provisioning benchmark; v1 and its results stay unchanged.

All tools here are simulated; connector updates invalidate prior checks.
"""
from dataclasses import replace
from typing import Any

from scenarios.access_provisioning_base import KINDS, ProvisioningWorkspace, make_scenario as make_v1


class RepairableProvisioningWorkspace(ProvisioningWorkspace):
    def run(self, tool: str, args: dict[str, Any]) -> tuple[str, str | None]:
        if tool not in {"list_connectors", "update_connector"}:
            return super().run(tool, args)
        out, error = getattr(self, f"_tool_{tool}")(args)
        if error is None:
            self.steps.append(tool)
        return out, error

    def _tool_list_connectors(self, _args: dict[str, Any]) -> tuple[str, str | None]:
        if not self.connectors:
            return "no connectors", None
        return "\n".join(
            f"{cid}: name {connector['name']}, kind {connector['kind']}"
            for cid, connector in self.connectors.items()
        ), None

    def _tool_update_connector(self, args: dict[str, Any]) -> tuple[str, str | None]:
        cid, kind = self._s(args, "connector_id"), self._s(args, "kind")
        if cid not in self.connectors:
            return "", f"unknown connector_id {cid!r}; use list_connectors to inspect existing connectors"
        if kind not in KINDS:
            return "", f"invalid kind {kind!r}; must be one of {', '.join(KINDS)}"
        self.connectors[cid]["kind"] = kind
        self.version += 1
        return f"updated connector {cid} to kind {kind}; re-run authorization checks", None


def make_scenario(seed: int = 7):
    original = make_v1(seed)
    extras = [
        {"type": "function", "function": {"name": "list_connectors",
         "description": "List existing connectors with their ids, names, and kinds.",
         "parameters": {"type": "object", "properties": {}, "required": []}}},
        {"type": "function", "function": {"name": "update_connector",
         "description": "Change an existing connector's kind; previous authorization checks must be repeated.",
         "parameters": {"type": "object", "properties": {
             "connector_id": {"type": "string", "description": "id from create_connector or list_connectors"},
             "kind": {"type": "string", "description": "http_api, github or google_drive"}},
             "required": ["connector_id", "kind"]}}},
    ]
    return replace(
        original,
        name="access_provisioning_v2",
        task=("Give the data-science group read-only access to the CRM connector named crm "
              "of kind http_api. Add Alice to data-science. Do not add Bob to the group. "
              "Verify: alice can read, alice cannot write, bob cannot read. Then call done."),
        system_prompt=original.system_prompt.replace(
            "no tool looks ids up by name", "list_connectors can inspect connector ids and kinds"),
        tools=[*original.tools, *extras],
        nudges={**original.nudges, "prerequisite": (
            "Before retrying, complete only the missing step listed below using the IDs already returned. "
            "Do not repeat steps that have already succeeded.")},
        new_workspace=lambda: RepairableProvisioningWorkspace(seed),
    )


SCENARIO = make_scenario()
