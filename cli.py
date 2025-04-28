import argparse
import os
from git_ops.repository_manager import RepositoryManager

def main():
    parser = argparse.ArgumentParser(description="AI Code Repository Assistant CLI")
    parser.add_argument("--repo-path", type=str, default=os.getcwd(), help="Path to the repository")
    parser.add_argument("--action", type=str, required=True, choices=["create-branch", "merge-branch", "protect-branch", "validate-branch-name", "validate-commit-message", "resolve-conflicts", "create-stash", "apply-stash", "drop-stash", "rebase-branch", "setup-conditional-workflow", "run-workflows-in-parallel", "create-workflow-template"], help="Action to perform")
    parser.add_argument("--branch-name", type=str, help="Branch name for branch-related actions")
    parser.add_argument("--base-branch", type=str, help="Base branch for merge or rebase actions")
    parser.add_argument("--workflow-name", type=str, help="Workflow name for workflow-related actions")
    parser.add_argument("--workflow-config", type=str, help="Path to workflow configuration file")
    parser.add_argument("--conditions", type=str, help="Path to conditions configuration file")
    parser.add_argument("--workflow-names", type=str, help="Comma-separated list of workflow names for parallel execution")
    parser.add_argument("--event", type=str, help="Event for workflow-related actions")
    parser.add_argument("--template-name", type=str, help="Template name for template-related actions")
    parser.add_argument("--template-config", type=str, help="Path to template configuration file")
    parser.add_argument("--commit-message", type=str, help="Commit message for validation")
    parser.add_argument("--conflicts", type=str, help="Comma-separated list of conflicted files")
    parser.add_argument("--stash-index", type=int, default=0, help="Stash index for stash-related actions")
    parser.add_argument("--stash-message", type=str, help="Message for stash creation")

    args = parser.parse_args()

    repo_manager = RepositoryManager(args.repo_path)

    if args.action == "create-branch":
        success = repo_manager.create_and_switch_branch(args.branch_name)
        print(f"Create and switch branch: {'Success' if success else 'Failed'}")
    elif args.action == "merge-branch":
        success = repo_manager.merge_branch(args.branch_name, args.base_branch)
        print(f"Merge branch: {'Success' if success else 'Failed'}")
    elif args.action == "protect-branch":
        success = repo_manager.protect_branch(args.branch_name)
        print(f"Protect branch: {'Success' if success else 'Failed'}")
    elif args.action == "validate-branch-name":
        valid = repo_manager.validate_branch_name(args.branch_name)
        print(f"Branch name '{args.branch_name}' is {'valid' if valid else 'invalid'}")
    elif args.action == "validate-commit-message":
        valid = repo_manager.validate_commit_message(args.commit_message)
        print(f"Commit message is {'valid' if valid else 'invalid'}")
    elif args.action == "resolve-conflicts":
        conflicts = args.conflicts.split(",")
        success = repo_manager.resolve_conflicts_interactive(conflicts)
        print(f"Resolve conflicts: {'Success' if success else 'Failed'}")
    elif args.action == "create-stash":
        success = repo_manager.create_stash(args.stash_message)
        print(f"Create stash: {'Success' if success else 'Failed'}")
    elif args.action == "apply-stash":
        success = repo_manager.apply_stash(args.stash_index)
        print(f"Apply stash: {'Success' if success else 'Failed'}")
    elif args.action == "drop-stash":
        success = repo_manager.drop_stash(args.stash_index)
        print(f"Drop stash: {'Success' if success else 'Failed'}")
    elif args.action == "rebase-branch":
        success = repo_manager.rebase_branch(args.base_branch)
        print(f"Rebase branch: {'Success' if success else 'Failed'}")
    elif args.action == "setup-conditional-workflow":
        import json
        with open(args.workflow_config, "r") as f:
            workflow_config = json.load(f)
        with open(args.conditions, "r") as f:
            conditions = json.load(f)
        success = repo_manager.setup_conditional_workflow(args.workflow_name, workflow_config, conditions)
        print(f"Setup conditional workflow: {'Success' if success else 'Failed'}")
    elif args.action == "run-workflows-in-parallel":
        workflow_names = args.workflow_names.split(",")
        workflow_ids = repo_manager.run_workflows_in_parallel(workflow_names, args.event)
        print(f"Run workflows in parallel: {workflow_ids}")
    elif args.action == "create-workflow-template":
        import json
        with open(args.template_config, "r") as f:
            template_config = json.load(f)
        success = repo_manager.create_workflow_template(args.template_name, template_config)
        print(f"Create workflow template: {'Success' if success else 'Failed'}")

if __name__ == "__main__":
    main() 