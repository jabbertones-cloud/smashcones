"""Prevent a public handoff from using paid/private runners or deploying."""
from pathlib import Path
import re
import unittest

WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "deploy.yml"


def check_contract(source: str) -> None:
    runs = re.findall(r"^\s*runs-on: (.+)$", source, re.M)
    if runs != ["ubuntu-24.04"]:
        raise AssertionError("handoff must use exactly one free standard public Ubuntu runner")
    if re.search(r"runs-on:.*(?:self-hosted|xlarge|large)", source, re.I):
        raise AssertionError("no persistent or larger billed runner")
    for proof in ("RUNNER_ENVIRONMENT:-}", "github-hosted", "RUNNER_OS:-}", "Linux", "RUNNER_ARCH:-}", "X64"):
        if proof not in source:
            raise AssertionError("missing early isolated VM contract "+proof)
    if source.index("Require isolated free GitHub standard runner") > source.index("actions/checkout@v4"):
        raise AssertionError("runner check must precede checkout")
    if "github.event_name == 'workflow_dispatch'" not in source:
        raise AssertionError("release handoff must not claim to run for PRs")
    if "This job does not deploy or assert production acceptance." not in source:
        raise AssertionError("handoff must explicitly disclaim deployment")
    if "Production deploy authority: M2 Cloudflare OAuth" not in source:
        raise AssertionError("must retain M2 deployment authority")
    if re.search(r"uses:.*wrangler|run:.*\bwrangler (?:deploy|pages deploy)|secrets\.CLOUDFLARE|wrangler-action@", source, re.I):
        raise AssertionError("handoff cannot silently become a deployment job")
    if "pull_request:" not in source or "workflow_dispatch:" not in source:
        raise AssertionError("require exact-head PR contract proof and manual handoff")


class HandoffPolicyTests(unittest.TestCase):
    def test_standard_public_runner_with_no_deploy(self):
        check_contract(WORKFLOW.read_text())

    def test_reject_persistent_or_larger_runner(self):
        source = WORKFLOW.read_text()
        for label in ["[self-hosted, macOS, ARM64, smat-m1]", "macos-15-xlarge", "ubuntu-latest"]:
            with self.subTest(label=label):
                with self.assertRaises(AssertionError):
                    check_contract(source.replace("runs-on: ubuntu-24.04", "runs-on: "+label))

    def test_reject_missing_isolation_or_readded_deployment(self):
        source = WORKFLOW.read_text()
        with self.assertRaises(AssertionError):
            check_contract(source.replace("RUNNER_ENVIRONMENT:-}", "UNKNOWN_ENVIRONMENT:-}"))
        with self.assertRaises(AssertionError):
            check_contract(source + "\n      - run: npx wrangler deploy")


if __name__=="__main__":
    unittest.main()
