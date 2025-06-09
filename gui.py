import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import sys
from pathlib import Path

# Add src to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

from git_ops.repository_manager import RepositoryManager

class RepositoryManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Code Repository Assistant")
        self.root.geometry("800x600")
        
        self.repo_manager = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # Repository Path
        ttk.Label(self.root, text="Repository Path:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.repo_path_var = tk.StringVar(value=os.getcwd())
        ttk.Entry(self.root, textvariable=self.repo_path_var, width=50).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(self.root, text="Browse", command=self.browse_repo_path).grid(row=0, column=2, padx=10, pady=10)
        
        # Initialize Repository
        ttk.Button(self.root, text="Initialize Repository", command=self.initialize_repository).grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        
        # Branch Management
        ttk.Label(self.root, text="Branch Management").grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        
        ttk.Label(self.root, text="Branch Name:").grid(row=3, column=0, padx=10, pady=10, sticky="w")
        self.branch_name_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.branch_name_var, width=30).grid(row=3, column=1, padx=10, pady=10)
        
        ttk.Button(self.root, text="Create Branch", command=self.create_branch).grid(row=3, column=2, padx=10, pady=10)
        ttk.Button(self.root, text="Merge Branch", command=self.merge_branch).grid(row=3, column=3, padx=10, pady=10)
        ttk.Button(self.root, text="Protect Branch", command=self.protect_branch).grid(row=3, column=4, padx=10, pady=10)
        
        # Workflow Management
        ttk.Label(self.root, text="Workflow Management").grid(row=4, column=0, columnspan=3, padx=10, pady=10, sticky="w")
        
        ttk.Label(self.root, text="Workflow Name:").grid(row=5, column=0, padx=10, pady=10, sticky="w")
        self.workflow_name_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.workflow_name_var, width=30).grid(row=5, column=1, padx=10, pady=10)
        
        ttk.Button(self.root, text="Setup Workflow", command=self.setup_workflow).grid(row=5, column=2, padx=10, pady=10)
        ttk.Button(self.root, text="Run Workflow", command=self.run_workflow).grid(row=5, column=3, padx=10, pady=10)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        ttk.Label(self.root, textvariable=self.status_var).grid(row=6, column=0, columnspan=3, padx=10, pady=10, sticky="w")
    
    def browse_repo_path(self):
        repo_path = filedialog.askdirectory()
        if repo_path:
            self.repo_path_var.set(repo_path)
    
    def initialize_repository(self):
        try:
            repo_path = self.repo_path_var.get()
            if not os.path.exists(repo_path):
                messagebox.showerror("Error", f"Repository path '{repo_path}' does not exist.")
                return
            if not os.path.exists(os.path.join(repo_path, ".git")):
                messagebox.showerror("Error", f"Repository path '{repo_path}' is not a valid Git repository.")
                return
            self.repo_manager = RepositoryManager(repo_path)
            self.status_var.set("Repository initialized successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to initialize repository: {str(e)}")
    
    def create_branch(self):
        if not self.repo_manager:
            messagebox.showerror("Error", "Please initialize the repository first.")
            return
        try:
            success = self.repo_manager.create_and_switch_branch(self.branch_name_var.get())
            if success:
                self.status_var.set(f"Branch '{self.branch_name_var.get()}' created successfully.")
            else:
                messagebox.showerror("Error", f"Failed to create branch '{self.branch_name_var.get()}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create branch: {str(e)}")
    
    def merge_branch(self):
        if not self.repo_manager:
            messagebox.showerror("Error", "Please initialize the repository first.")
            return
        try:
            success = self.repo_manager.merge_branch(self.branch_name_var.get())
            if success:
                self.status_var.set(f"Branch '{self.branch_name_var.get()}' merged successfully.")
            else:
                messagebox.showerror("Error", f"Failed to merge branch '{self.branch_name_var.get()}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to merge branch: {str(e)}")
    
    def protect_branch(self):
        if not self.repo_manager:
            messagebox.showerror("Error", "Please initialize the repository first.")
            return
        try:
            success = self.repo_manager.protect_branch(self.branch_name_var.get())
            if success:
                self.status_var.set(f"Branch '{self.branch_name_var.get()}' protected successfully.")
            else:
                messagebox.showerror("Error", f"Failed to protect branch '{self.branch_name_var.get()}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to protect branch: {str(e)}")
    
    def setup_workflow(self):
        if not self.repo_manager:
            messagebox.showerror("Error", "Please initialize the repository first.")
            return
        try:
            workflow_config = {
                "name": self.workflow_name_var.get(),
                "description": "Test workflow",
                "events": ["push", "pull_request"],
                "steps": [
                    {
                        "name": "test-step",
                        "event": "push",
                        "command": "echo 'Test step'"
                    }
                ]
            }
            success = self.repo_manager.setup_workflow(self.workflow_name_var.get(), workflow_config)
            if success:
                self.status_var.set(f"Workflow '{self.workflow_name_var.get()}' set up successfully.")
            else:
                messagebox.showerror("Error", f"Failed to set up workflow '{self.workflow_name_var.get()}'.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to set up workflow: {str(e)}")
    
    def run_workflow(self):
        if not self.repo_manager:
            messagebox.showerror("Error", "Please initialize the repository first.")
            return
        try:
            workflow_id = self.repo_manager.run_workflow(self.workflow_name_var.get(), "push")
            self.status_var.set(f"Workflow '{self.workflow_name_var.get()}' executed successfully with ID: {workflow_id}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to run workflow: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RepositoryManagerGUI(root)
    root.mainloop() 