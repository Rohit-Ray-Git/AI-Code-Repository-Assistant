from model import RepositoryModel

class RepositoryContext:
    def __init__(self, repo_path):
        self.model = RepositoryModel(repo_path)

    def get_branches(self):
        return self.model.get_branches()

    def get_commit_history(self):
        return self.model.get_commit_history()

    def get_workflows(self):
        return self.model.get_workflows()

    def get_stashes(self):
        return self.model.get_stashes()

    def create_branch(self, branch_name):
        return self.model.create_branch(branch_name)

    def merge_branch(self, branch_name):
        return self.model.merge_branch(branch_name)

    def protect_branch(self, branch_name):
        return self.model.protect_branch(branch_name)

    def setup_workflow(self, workflow_name, workflow_config):
        return self.model.setup_workflow(workflow_name, workflow_config)

    def run_workflow(self, workflow_name, event):
        return self.model.run_workflow(workflow_name, event)

    def create_stash(self, message):
        return self.model.create_stash(message)

    def apply_stash(self, stash_index):
        return self.model.apply_stash(stash_index)

    def drop_stash(self, stash_index):
        return self.model.drop_stash(stash_index)

    def rebase_branch(self, base_branch):
        return self.model.rebase_branch(base_branch) 