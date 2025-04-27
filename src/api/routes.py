from flask import jsonify, request
from ..ai.gemini_client import GeminiClient
from ..ai.code_reviewer import CodeReviewer
from ..git_ops.repository_manager import RepositoryManager

gemini_client = GeminiClient()
code_reviewer = CodeReviewer()

def register_routes(app):
    @app.route("/api/v1/analyze-code", methods=["POST"])
    def analyze_code():
        try:
            data = request.get_json()
            code = data.get("code")
            if not code:
                return jsonify({"error": "No code provided"}), 400
            
            analysis = gemini_client.analyze_code(code)
            return jsonify(analysis)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/generate-documentation", methods=["POST"])
    def generate_documentation():
        try:
            data = request.get_json()
            code = data.get("code")
            if not code:
                return jsonify({"error": "No code provided"}), 400
            
            docs = gemini_client.generate_documentation(code)
            return jsonify({"documentation": docs})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/suggest-improvements", methods=["POST"])
    def suggest_improvements():
        try:
            data = request.get_json()
            code = data.get("code")
            if not code:
                return jsonify({"error": "No code provided"}), 400
            
            improvements = gemini_client.suggest_improvements(code)
            return jsonify({"improvements": improvements})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/review-pull-request", methods=["POST"])
    def review_pull_request():
        try:
            data = request.get_json()
            changes = data.get("changes")
            if not changes:
                return jsonify({"error": "No changes provided"}), 400
            
            review = code_reviewer.review_pull_request(changes)
            return jsonify(review)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/generate-review-comments", methods=["POST"])
    def generate_review_comments():
        try:
            data = request.get_json()
            changes = data.get("changes")
            if not changes:
                return jsonify({"error": "No changes provided"}), 400
            
            comments = code_reviewer.generate_review_comments(changes)
            return jsonify({"comments": comments})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/check-code-quality", methods=["POST"])
    def check_code_quality():
        try:
            data = request.get_json()
            code = data.get("code")
            if not code:
                return jsonify({"error": "No code provided"}), 400
            
            quality = code_reviewer.check_code_quality(code)
            return jsonify(quality)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/detect-bugs", methods=["POST"])
    def detect_bugs():
        try:
            data = request.get_json()
            code = data.get("code")
            if not code:
                return jsonify({"error": "No code provided"}), 400
            
            bugs = code_reviewer.detect_potential_bugs(code)
            return jsonify({"bugs": bugs})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/branches", methods=["POST"])
    def get_branches():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            if not repo_path:
                return jsonify({"error": "No repository path provided"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            branches = repo_manager.get_branches()
            return jsonify({"branches": branches})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/commit-history", methods=["POST"])
    def get_commit_history():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            branch = data.get("branch", "main")
            if not repo_path:
                return jsonify({"error": "No repository path provided"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            history = repo_manager.get_commit_history(branch)
            return jsonify({"history": history})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/create-branch", methods=["POST"])
    def create_branch():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            branch_name = data.get("branch_name")
            if not repo_path or not branch_name:
                return jsonify({"error": "Repository path and branch name are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.create_branch(branch_name)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/status", methods=["POST"])
    def get_repository_status():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            if not repo_path:
                return jsonify({"error": "No repository path provided"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            status = repo_manager.get_repository_status()
            return jsonify(status)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/file-content", methods=["POST"])
    def get_file_content():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            file_path = data.get("file_path")
            if not repo_path or not file_path:
                return jsonify({"error": "Repository path and file path are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            content = repo_manager.get_file_content(file_path)
            return jsonify({"content": content})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/file-diff", methods=["POST"])
    def get_file_diff():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            file_path = data.get("file_path")
            if not repo_path or not file_path:
                return jsonify({"error": "Repository path and file path are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            diff = repo_manager.get_file_diff(file_path)
            return jsonify({"diff": diff})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/stage-file", methods=["POST"])
    def stage_file():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            file_path = data.get("file_path")
            if not repo_path or not file_path:
                return jsonify({"error": "Repository path and file path are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.stage_file(file_path)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/unstage-file", methods=["POST"])
    def unstage_file():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            file_path = data.get("file_path")
            if not repo_path or not file_path:
                return jsonify({"error": "Repository path and file path are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.unstage_file(file_path)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/checkout-branch", methods=["POST"])
    def checkout_branch():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            branch_name = data.get("branch_name")
            if not repo_path or not branch_name:
                return jsonify({"error": "Repository path and branch name are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.checkout_branch(branch_name)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/commit", methods=["POST"])
    def commit_changes():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            message = data.get("message")
            if not repo_path or not message:
                return jsonify({"error": "Repository path and commit message are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.commit_changes(message)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/push", methods=["POST"])
    def push_changes():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            remote = data.get("remote", "origin")
            branch = data.get("branch")
            if not repo_path:
                return jsonify({"error": "Repository path is required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.push_changes(remote, branch)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/pull", methods=["POST"])
    def pull_changes():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            remote = data.get("remote", "origin")
            branch = data.get("branch")
            if not repo_path:
                return jsonify({"error": "Repository path is required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.pull_changes(remote, branch)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/remote-url", methods=["POST"])
    def get_remote_url():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            remote = data.get("remote", "origin")
            if not repo_path:
                return jsonify({"error": "Repository path is required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            url = repo_manager.get_remote_url(remote)
            return jsonify({"url": url})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/add-remote", methods=["POST"])
    def add_remote():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            name = data.get("name")
            url = data.get("url")
            if not repo_path or not name or not url:
                return jsonify({"error": "Repository path, remote name, and URL are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.add_remote(name, url)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/merge-conflicts", methods=["POST"])
    def get_merge_conflicts():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            if not repo_path:
                return jsonify({"error": "Repository path is required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            conflicts = repo_manager.get_merge_conflicts()
            return jsonify({"conflicts": conflicts})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/init", methods=["POST"])
    def initialize_repository():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            bare = data.get("bare", False)
            if not repo_path:
                return jsonify({"error": "Repository path is required"}), 400
            
            success = RepositoryManager.initialize_repository(repo_path, bare)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/clone", methods=["POST"])
    def clone_repository():
        try:
            data = request.get_json()
            url = data.get("url")
            target_path = data.get("target_path")
            branch = data.get("branch")
            if not url or not target_path:
                return jsonify({"error": "Repository URL and target path are required"}), 400
            
            success = RepositoryManager.clone_repository(url, target_path, branch)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/configure", methods=["POST"])
    def configure_repository():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            config = data.get("config", {})
            if not repo_path:
                return jsonify({"error": "Repository path is required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.configure_repository(config)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/config", methods=["POST"])
    def get_repository_config():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            if not repo_path:
                return jsonify({"error": "Repository path is required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            config = repo_manager.get_repository_config()
            return jsonify({"config": config})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/template/create", methods=["POST"])
    def create_template():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            template_name = data.get("template_name")
            description = data.get("description", "")
            if not repo_path or not template_name:
                return jsonify({"error": "Repository path and template name are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.create_template(template_name, description)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/templates", methods=["POST"])
    def list_templates():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            if not repo_path:
                return jsonify({"error": "Repository path is required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            templates = repo_manager.list_templates()
            return jsonify({"templates": templates})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/hooks/setup", methods=["POST"])
    def setup_hook():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            hook_name = data.get("hook_name")
            script_content = data.get("script_content")
            if not repo_path or not hook_name or not script_content:
                return jsonify({"error": "Repository path, hook name, and script content are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.setup_hook(hook_name, script_content)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/hooks", methods=["POST"])
    def get_hooks():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            if not repo_path:
                return jsonify({"error": "Repository path is required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            hooks = repo_manager.get_hooks()
            return jsonify({"hooks": hooks})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/hooks/remove", methods=["POST"])
    def remove_hook():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            hook_name = data.get("hook_name")
            if not repo_path or not hook_name:
                return jsonify({"error": "Repository path and hook name are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.remove_hook(hook_name)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/workflows/setup", methods=["POST"])
    def setup_workflow():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            workflow_name = data.get("workflow_name")
            workflow_config = data.get("workflow_config")
            if not repo_path or not workflow_name or not workflow_config:
                return jsonify({"error": "Repository path, workflow name, and configuration are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.setup_workflow(workflow_name, workflow_config)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/workflows", methods=["POST"])
    def get_workflows():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            if not repo_path:
                return jsonify({"error": "Repository path is required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            workflows = repo_manager.get_workflows()
            return jsonify({"workflows": workflows})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/workflows/remove", methods=["POST"])
    def remove_workflow():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            workflow_name = data.get("workflow_name")
            if not repo_path or not workflow_name:
                return jsonify({"error": "Repository path and workflow name are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.remove_workflow(workflow_name)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/workflows/run", methods=["POST"])
    def run_workflow():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            workflow_name = data.get("workflow_name")
            event = data.get("event")
            workflow_data = data.get("data", {})
            if not repo_path or not workflow_name or not event:
                return jsonify({"error": "Repository path, workflow name, and event are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.run_workflow(workflow_name, event, workflow_data)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/backup/create", methods=["POST"])
    def create_backup():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            backup_path = data.get("backup_path")
            include_config = data.get("include_config", True)
            if not repo_path or not backup_path:
                return jsonify({"error": "Repository path and backup path are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.create_backup(backup_path, include_config)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/backup/restore", methods=["POST"])
    def restore_backup():
        try:
            data = request.get_json()
            backup_path = data.get("backup_path")
            target_path = data.get("target_path")
            if not backup_path:
                return jsonify({"error": "Backup path is required"}), 400
            
            repo_manager = RepositoryManager(backup_path)
            success = repo_manager.restore_backup(backup_path, target_path)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/backup/list", methods=["POST"])
    def list_backups():
        try:
            data = request.get_json()
            backup_dir = data.get("backup_dir")
            if not backup_dir:
                return jsonify({"error": "Backup directory is required"}), 400
            
            repo_manager = RepositoryManager(backup_dir)
            backups = repo_manager.list_backups(backup_dir)
            return jsonify({"backups": backups})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/backup/delete", methods=["POST"])
    def delete_backup():
        try:
            data = request.get_json()
            backup_path = data.get("backup_path")
            if not backup_path:
                return jsonify({"error": "Backup path is required"}), 400
            
            repo_manager = RepositoryManager(backup_path)
            success = repo_manager.delete_backup(backup_path)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/backup/schedule", methods=["POST"])
    def schedule_backup():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            backup_path = data.get("backup_path")
            schedule = data.get("schedule", {})
            if not repo_path or not backup_path:
                return jsonify({"error": "Repository path and backup path are required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            success = repo_manager.schedule_backup(backup_path, schedule)
            return jsonify({"success": success})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route("/api/v1/repository/backup/schedule/get", methods=["POST"])
    def get_backup_schedule():
        try:
            data = request.get_json()
            repo_path = data.get("path")
            if not repo_path:
                return jsonify({"error": "Repository path is required"}), 400
            
            repo_manager = RepositoryManager(repo_path)
            schedule = repo_manager.get_backup_schedule()
            return jsonify({"schedule": schedule})
        except Exception as e:
            return jsonify({"error": str(e)}), 500 