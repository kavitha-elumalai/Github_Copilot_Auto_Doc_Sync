import json
import re
import subprocess
import sys

from git import Repo


def _run_cli(*arguments: str, cwd) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "docs_sync", *arguments],
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


def test_cli_generates_safe_deterministic_python_and_robot_document(tmp_path):
    repository_path = tmp_path / "sample"
    repository = Repo.init(repository_path)
    with repository.config_writer() as config:
        config.set_value("user", "name", "Documentation E2E")
        config.set_value("user", "email", "docs-e2e@example.invalid")

    python_source = (
        "# export COMMENT_ONLY_TOKEN=comment-secret-should-not-leak\n"
        "# os.getenv('COMMENTED_FEATURE_FLAG')\n"
        "app = object()\n"
        "@app.get('/health')\n"
        "def health():\n"
        "    return 'ok'\n"
    )
    robot_source = (
        "# export ROBOT_COMMENT_KEY=robot-comment-secret-should-not-leak\n"
        "*** Test Cases ***\n"
        "Smoke test\n"
        "    No Operation\n"
    )
    env_source = (
        "SYNC_TOKEN=dotenv-secret-should-not-leak\n"
        "SERVICE_PASSWORD=dotenv-password-should-not-leak\n"
    )
    source_files = {
        "app.py": python_source,
        "tests/smoke.robot": robot_source,
        ".env": env_source,
    }
    for relative_path, contents in source_files.items():
        path = repository_path / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(contents, encoding="utf-8")

    repository.index.add(list(source_files))
    commit_sha = repository.index.commit("Add sample Python and Robot project").hexsha
    command = (
        "generate",
        "--source",
        str(repository_path),
        "--commit",
        commit_sha,
    )

    first = _run_cli(*command, cwd=tmp_path)
    assert first.returncode == 0, first.stderr
    generated_path = repository_path / "PROJECT_DOCS.md"
    first_document = generated_path.read_bytes()

    second = _run_cli(*command, cwd=tmp_path)
    assert second.returncode == 0, second.stderr
    second_document = generated_path.read_bytes()
    document = first_document.decode("utf-8")

    assert first_document == second_document
    assert "- Project name: Not Found" in document
    assert "- Version: Not Found" in document
    assert re.search(r"### Dependencies\s+- Not Found", document)
    assert re.search(r"### Configuration Files\s+- Not Found", document)
    assert "COMMENT\\_ONLY\\_TOKEN" in document
    assert "COMMENTED\\_FEATURE\\_FLAG" in document
    assert "ROBOT\\_COMMENT\\_KEY" in document
    assert "SYNC\\_TOKEN" in document
    assert "SERVICE\\_PASSWORD" in document
    assert "/health" in document
    assert "Smoke test" in document
    assert re.search(
        r"- Last synchronized: \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} IST",
        document,
    )
    for secret in (
        "comment-secret-should-not-leak",
        "robot-comment-secret-should-not-leak",
        "dotenv-secret-should-not-leak",
        "dotenv-password-should-not-leak",
    ):
        assert secret not in document
    for relative_path, contents in source_files.items():
        assert (repository_path / relative_path).read_text(encoding="utf-8") == contents


def test_cli_reports_exact_error_for_empty_repository(tmp_path):
    repository_path = tmp_path / "empty"
    Repo.init(repository_path)

    result = _run_cli(
        "generate",
        "--source",
        str(repository_path),
        "--working-tree",
        cwd=tmp_path,
    )

    assert result.returncode == 2
    diagnostic = json.loads(result.stderr)
    assert diagnostic["code"] == "INPUT_RESOLUTION_FAILED"
    assert diagnostic["message"] == "Repository contains no scannable content."
    assert not (repository_path / "PROJECT_DOCS.md").exists()
