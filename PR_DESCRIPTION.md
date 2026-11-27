## Summary

Automated Documentation Sync adds a Python CLI that analyzes Python and Robot Framework repositories and produces deterministic `PROJECT_DOCS.md` documentation. It includes local/GitHub pull-request inputs, secret-safe processing, and merge-triggered automation to keep project documentation current.

## Changes Made

- `.githooks/post-merge` — added a hook template to run documentation synchronization after a merge.
- `.github/workflows/doc-sync.yml` — added a workflow that runs only for a closed, merged pull request and commits `PROJECT_DOCS.md` when it changes.
- `pyproject.toml`, `uv.lock` — defined the package, CLI, runtime/development dependencies, and reproducible dependency versions.
- `src/docs_sync/__init__.py`, `src/docs_sync/__main__.py`, `src/docs_sync/cli.py` — exposed the package and Typer CLI entry point, including stable redacted diagnostics and input/output validation.
- `src/docs_sync/config.py`, `src/docs_sync/constants.py`, `src/docs_sync/errors.py`, `src/docs_sync/filesystem.py`, `src/docs_sync/limits.py`, `src/docs_sync/logging.py`, `src/docs_sync/models.py`, `src/docs_sync/pipeline.py` — added shared configuration, typed data models and errors, bounded repository inventory, safe logging, and end-to-end orchestration.
- `src/docs_sync/parsers/__init__.py`, `src/docs_sync/parsers/python_config.py`, `src/docs_sync/parsers/python_parser.py`, `src/docs_sync/parsers/python_routes.py`, `src/docs_sync/parsers/robot_parser.py`, `src/docs_sync/parsers/worker.py` — added bounded static parsing of Python metadata/routes and Robot Framework files without executing source code.
- `src/docs_sync/renderer/__init__.py`, `src/docs_sync/renderer/markdown.py`, `src/docs_sync/renderer/normalizer.py`, `src/docs_sync/renderer/timestamps.py`, `src/docs_sync/renderer/writer.py` — added stable Markdown generation, normalization, IST timestamp handling, and safe atomic output.
- `src/docs_sync/resolver/__init__.py`, `src/docs_sync/resolver/base.py`, `src/docs_sync/resolver/credentials.py`, `src/docs_sync/resolver/git_client.py`, `src/docs_sync/resolver/github.py`, `src/docs_sync/resolver/github_url.py`, `src/docs_sync/resolver/local.py`, `src/docs_sync/resolver/pull_request.py`, `src/docs_sync/resolver/rate_limit.py`, `src/docs_sync/resolver/workspace.py` — added validated local/GitHub input handling, credential management, pull-request merge-commit selection, bounded rate-limit handling, and temporary workspace lifecycle.
- `src/docs_sync/security/__init__.py`, `src/docs_sync/security/env_sanitizer.py`, `src/docs_sync/security/path_policy.py`, `src/docs_sync/security/redactor.py`, `src/docs_sync/security/secret_patterns.py` — added environment inventory/sanitization, path controls, and registered/built-in secret redaction.
- `tests/conftest.py`, `tests/unit/test_cli.py`, `tests/unit/test_config.py`, `tests/unit/test_errors.py`, `tests/unit/test_filesystem.py`, `tests/unit/test_models.py`, `tests/unit/test_pipeline.py`, `tests/unit/test_python_parser.py`, `tests/unit/test_redactor.py`, `tests/unit/test_renderer.py`, `tests/unit/test_robot_parser.py`, `tests/unit/test_writer.py`, `tests/unit/resolver/test_github_resolver.py`, `tests/unit/resolver/test_input_resolver.py`, `tests/unit/resolver/test_local_resolver.py`, `tests/unit/security/test_env_sanitizer.py` — added focused coverage for CLI behavior, repository handling, parsing, security, rendering, and writing.
- `tests/e2e/test_cli_end_to_end.py` — added end-to-end checks for Python/Robot input, secret non-disclosure, missing metadata, IST timestamps, deterministic output, source preservation, and the exact empty-repository error.
- `e2e-verification-pytest.txt` — saved the complete verbose end-to-end verification run.
- `requirements.md`, `architecture.md`, `design-review.md`, `impl-plan.md`, `README.md`, `code-review-report.md` — documented requirements, architecture, approved design mitigations, implementation sequencing, usage, and review outcomes.
- `CHANGELOG.md` — documented the v0.1.0 release.
- `PR_DESCRIPTION.md` — prepared this pull-request description.

## Test Evidence

`pytest -v` verification output:

```text
============================= test session starts =============================
platform win32 -- Python 3.13.3, pytest-9.2.0, pluggy-1.7.0 -- C:\Users\KavithaElumalai\Documents\Github_Copilot_Auto_Doc_Sync\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\Users\KavithaElumalai\Documents\Github_Copilot_Auto_Doc_Sync
configfile: pyproject.toml
testpaths: tests
collecting ... collected 92 items

tests/e2e/test_cli_end_to_end.py::test_cli_generates_safe_deterministic_python_and_robot_document PASSED [  1%]
tests/e2e/test_cli_end_to_end.py::test_cli_reports_exact_error_for_empty_repository PASSED [  2%]
tests/unit/resolver/test_github_resolver.py::test_github_url_parser_rejects_embedded_credentials PASSED [  3%]
tests/unit/resolver/test_github_resolver.py::test_supported_github_url_forms[https://github.com/acme/project] PASSED [  4%]
tests/unit/resolver/test_github_resolver.py::test_supported_github_url_forms[https://github.com/acme/project.git] PASSED [  5%]
tests/unit/resolver/test_github_resolver.py::test_supported_github_url_forms[git@github.com:acme/project.git] PASSED [  6%]
tests/unit/resolver/test_github_resolver.py::test_supported_github_url_forms[ssh://git@github.com/acme/project.git] PASSED [  7%]
tests/unit/resolver/test_github_resolver.py::test_pull_request_event_requires_closed_merged_correct_repository PASSED [  8%]
tests/unit/resolver/test_github_resolver.py::test_github_resolver_uses_merge_sha_and_cleans_temporary_workspace PASSED [  9%]
tests/unit/resolver/test_github_resolver.py::test_rate_limit_retry_is_bounded_and_reports_safe_failure PASSED [ 10%]
tests/unit/resolver/test_github_resolver.py::test_archive_keeps_environment_values_out_of_temporary_files PASSED [ 11%]
tests/unit/resolver/test_github_resolver.py::test_merged_event_resolves_only_validated_merge_commit PASSED [ 13%]
tests/unit/resolver/test_github_resolver.py::test_archive_download_does_not_forward_api_authorization PASSED [ 14%]
tests/unit/resolver/test_github_resolver.py::test_archive_rejects_path_traversal PASSED [ 15%]
tests/unit/resolver/test_github_resolver.py::test_explicit_environment_path_is_validated PASSED [ 16%]
tests/unit/resolver/test_input_resolver.py::test_input_resolver_dispatches_local_and_github_inputs PASSED [ 17%]
tests/unit/resolver/test_input_resolver.py::test_local_source_cannot_request_github_pull_request PASSED [ 18%]
tests/unit/resolver/test_input_resolver.py::test_environment_credentials_follow_priority_and_hide_repr PASSED [ 19%]
tests/unit/resolver/test_local_resolver.py::test_commit_resolution_materializes_snapshot_without_changing_source PASSED [ 20%]
tests/unit/resolver/test_local_resolver.py::test_working_tree_records_dirty_state_and_includes_untracked_file PASSED [ 21%]
tests/unit/resolver/test_local_resolver.py::test_empty_repository_has_safe_resolution_error PASSED [ 22%]
tests/unit/resolver/test_local_resolver.py::test_uncommitted_working_tree_without_head_can_be_scanned PASSED [ 23%]
tests/unit/resolver/test_local_resolver.py::test_request_rejects_ambiguous_reference_modes PASSED [ 25%]
tests/unit/security/test_env_sanitizer.py::test_environment_sanitizer_returns_names_and_registers_secret_values PASSED [ 26%]
tests/unit/security/test_env_sanitizer.py::test_configured_environment_file_and_empty_fallback PASSED [ 27%]
tests/unit/security/test_env_sanitizer.py::test_oversized_environment_file_fails_closed PASSED [ 28%]
tests/unit/security/test_env_sanitizer.py::test_comment_assignment_values_are_never_returned PASSED [ 29%]
tests/unit/security/test_env_sanitizer.py::test_sanitizer_reuses_inventory_budget PASSED [ 30%]
tests/unit/test_cli.py::test_cli_help_documents_modes_and_output PASSED  [ 31%]
tests/unit/test_cli.py::test_cli_invokes_pipeline_and_reports_changed_output PASSED [ 32%]
tests/unit/test_cli.py::test_cli_maps_typed_errors_to_stable_exit_codes_and_safe_messages PASSED [ 33%]
tests/unit/test_cli.py::test_cli_requires_output_path_for_github_source PASSED [ 34%]
tests/unit/test_cli.py::test_cli_rejects_conflicting_pull_request_modes_without_echoing_values PASSED [ 35%]
tests/unit/test_cli.py::test_cli_generates_document_from_local_git_working_tree PASSED [ 36%]
tests/unit/test_config.py::test_default_settings_match_architecture_limits PASSED [ 38%]
tests/unit/test_config.py::test_settings_reject_non_positive_limits PASSED [ 39%]
tests/unit/test_config.py::test_settings_reject_empty_exclusion_policy PASSED [ 40%]
tests/unit/test_errors.py::test_typed_error_exposes_stable_safe_envelope PASSED [ 41%]
tests/unit/test_errors.py::test_untrusted_exception_text_is_suppressed_without_redactor PASSED [ 42%]
tests/unit/test_errors.py::test_error_raises_typed_security_error_when_redaction_fails PASSED [ 43%]
tests/unit/test_errors.py::test_non_exception_cause_is_redacted_by_builtin_patterns PASSED [ 44%]
tests/unit/test_filesystem.py::test_inventory_classifies_binary_lfs_and_skips_generated_document PASSED [ 45%]
tests/unit/test_filesystem.py::test_optional_oversized_file_is_skipped_but_required_file_fails PASSED [ 46%]
tests/unit/test_filesystem.py::test_path_policy_rejects_symlink_traversal SKIPPED [ 47%]
tests/unit/test_models.py::test_repository_snapshot_normalizes_inventory_and_timestamp PASSED [ 48%]
tests/unit/test_models.py::test_repository_snapshot_rejects_naive_timestamp PASSED [ 50%]
tests/unit/test_models.py::test_metadata_defaults_to_not_found_and_sorts_values PASSED [ 51%]
tests/unit/test_models.py::test_environment_variable_rejects_invalid_name PASSED [ 52%]
tests/unit/test_models.py::test_parser_result_deduplicates_and_sorts_paths PASSED [ 53%]
tests/unit/test_pipeline.py::test_pipeline_merges_parser_results_and_writes_only_project_docs PASSED [ 54%]
tests/unit/test_pipeline.py::test_remote_pipeline_requires_and_preserves_explicit_output PASSED [ 55%]
tests/unit/test_pipeline.py::test_remote_pipeline_rejects_missing_output_before_resolving PASSED [ 56%]
tests/unit/test_python_parser.py::test_python_parser_extracts_static_metadata_symbols_and_routes PASSED [ 57%]
tests/unit/test_python_parser.py::test_python_parser_uses_literal_setup_py_and_requirements_fallback PASSED [ 58%]
tests/unit/test_python_parser.py::test_python_parser_uses_requirements_then_pipfile_for_dependencies PASSED [ 59%]
tests/unit/test_python_parser.py::test_python_parser_redacts_metadata_and_rejects_ast_limit PASSED [ 60%]
tests/unit/test_python_parser.py::test_python_parser_returns_not_found_for_empty_repository PASSED [ 61%]
tests/unit/test_python_parser.py::test_python_parser_error_does_not_expose_source_text PASSED [ 63%]
tests/unit/test_python_parser.py::test_python_parser_timeout_stops_worker_and_reports_safe_path PASSED [ 64%]
tests/unit/test_redactor.py::test_builtin_patterns_redact_common_credential_shapes[password=super-secret-value-super-secret-value] PASSED [ 65%]
tests/unit/test_redactor.py::test_builtin_patterns_redact_common_credential_shapes[{"api_key": "long-secret-value"}-long-secret-value] PASSED [ 66%]
tests/unit/test_redactor.py::test_builtin_patterns_redact_common_credential_shapes[Authorization: Bearer opaque-token-value-opaque-token-value] PASSED [ 67%]
tests/unit/test_redactor.py::test_builtin_patterns_redact_common_credential_shapes[Cookie: session=private-cookie-value-private-cookie-value] PASSED [ 68%]
tests/unit/test_redactor.py::test_builtin_patterns_redact_common_credential_shapes[Set-Cookie: auth=private-cookie-value-private-cookie-value] PASSED [ 69%]
tests/unit/test_redactor.py::test_builtin_patterns_redact_common_credential_shapes[https://user:pass@github.example/org/repo-user:pass] PASSED [ 70%]
tests/unit/test_redactor.py::test_builtin_patterns_redact_common_credential_shapes[https://opaque-token@github.example/org/repo-opaque-token] PASSED [ 71%]
tests/unit/test_redactor.py::test_builtin_patterns_redact_common_credential_shapes[https://example.test/?access_token=query-secret-query-secret] PASSED [ 72%]
tests/unit/test_redactor.py::test_builtin_patterns_redact_common_credential_shapes[-----BEGIN OPENSSH PRIVATE KEY-----\nprivate-data\n-----END OPENSSH PRIVATE KEY------private-data] PASSED [ 73%]
tests/unit/test_redactor.py::test_builtin_patterns_redact_common_credential_shapes[ghp_abcdefghijklmnopqrstuvwxyz0123456789-ghp_abcdefghijklmnopqrstuvwxyz0123456789] PASSED [ 75%]
tests/unit/test_redactor.py::test_registered_secret_is_redacted_from_arbitrary_text PASSED [ 76%]
tests/unit/test_redactor.py::test_invalid_redaction_input_fails_without_echoing_input PASSED [ 77%]
tests/unit/test_redactor.py::test_redaction_failure_is_fail_closed PASSED [ 78%]
tests/unit/test_redactor.py::test_logging_filter_redacts_message_and_traceback PASSED [ 79%]
tests/unit/test_redactor.py::test_configured_package_logger_does_not_propagate PASSED [ 80%]
tests/unit/test_redactor.py::test_logging_filter_redacts_stack_information PASSED [ 81%]
tests/unit/test_renderer.py::test_timestamp_uses_commit_committer_time_converted_to_ist PASSED [ 82%]
tests/unit/test_renderer.py::test_working_tree_timestamp_uses_wall_clock_and_requires_timezone PASSED [ 83%]
tests/unit/test_renderer.py::test_normalizer_sorts_redacts_and_removes_absolute_paths_outside_root PASSED [ 84%]
tests/unit/test_renderer.py::test_markdown_is_deterministic_escaped_and_uses_not_found PASSED [ 85%]
tests/unit/test_renderer.py::test_renderer_fails_when_rendered_markdown_exceeds_limit PASSED [ 86%]
tests/unit/test_renderer.py::test_renderer_redacts_registered_values_before_returning_markdown PASSED [ 88%]
tests/unit/test_robot_parser.py::test_robot_parser_extracts_metadata_without_importing_libraries PASSED [ 89%]
tests/unit/test_robot_parser.py::test_robot_parser_reports_sanitized_syntax_errors PASSED [ 90%]
tests/unit/test_robot_parser.py::test_robot_parser_returns_not_found_for_empty_repository PASSED [ 91%]
tests/unit/test_robot_parser.py::test_robot_parser_enforces_model_node_limit PASSED [ 92%]
tests/unit/test_robot_parser.py::test_robot_parser_timeout_stops_worker_and_reports_safe_path PASSED [ 93%]
tests/unit/test_writer.py::test_writer_atomically_writes_and_skips_identical_content PASSED [ 94%]
tests/unit/test_writer.py::test_writer_redacts_output_before_persisting PASSED [ 95%]
tests/unit/test_writer.py::test_writer_preserves_existing_document_when_size_check_fails PASSED [ 96%]
tests/unit/test_writer.py::test_writer_times_out_on_existing_lock_without_replacing_output PASSED [ 97%]
tests/unit/test_writer.py::test_writer_fails_closed_when_redaction_fails PASSED [ 98%]
tests/unit/test_writer.py::test_writer_removes_temporary_file_and_lock_after_replace_failure PASSED [100%]

=========================== short test summary info ===========================
SKIPPED [1] tests\unit\test_filesystem.py:67: Symlink creation is not supported in this environment.
======================= 91 passed, 1 skipped in 25.73s ========================
```

`uv build` previously completed successfully for both the source distribution and wheel. A fresh build could not be run in the current workspace because `pyproject.toml` and `uv.lock` are not present there.

## Known Limitations

- Metadata that cannot be found in statically inspected files is reported as `Not Found`.
- Human translation into multiple languages and dynamic runtime route evaluation are out of scope.
- The symlink traversal test was skipped because symlink creation is unsupported in this environment.

## Reviewer Checklist

- [ ] Correctness: requirements, edge cases, and exact empty-repository error are covered.
- [ ] Secret redaction: no `.env` secret values appear in generated documentation, logs, or errors.
- [ ] Timestamps: generated timestamps use the required IST format.
- [ ] `PROJECT_DOCS.md`: verify the generated content and confirm repeated runs on the same commit are byte-identical.
