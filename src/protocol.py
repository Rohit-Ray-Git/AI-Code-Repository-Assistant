from abc import ABC, abstractmethod

class RepositoryProtocol(ABC):
    @abstractmethod
    def get_branches(self):
        pass

    @abstractmethod
    def get_commit_history(self):
        pass

    @abstractmethod
    def get_workflows(self):
        pass

    @abstractmethod
    def get_stashes(self):
        pass

    @abstractmethod
    def create_branch(self, branch_name):
        pass

    @abstractmethod
    def merge_branch(self, branch_name):
        pass

    @abstractmethod
    def protect_branch(self, branch_name):
        pass

    @abstractmethod
    def setup_workflow(self, workflow_name, workflow_config):
        pass

    @abstractmethod
    def run_workflow(self, workflow_name, event):
        pass

    @abstractmethod
    def create_stash(self, message):
        pass

    @abstractmethod
    def apply_stash(self, stash_index):
        pass

    @abstractmethod
    def drop_stash(self, stash_index):
        pass

    @abstractmethod
    def rebase_branch(self, base_branch):
        pass 