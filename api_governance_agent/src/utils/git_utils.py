import git
from typing import Optional
import os

def get_file_content_from_commit(repo_path: str, file_path: str, commit_ref: str) -> Optional[str]:
    """
    Retrieves the content of a file from a specific commit in a Git repository.

    Args:
        repo_path (str): The path to the local Git repository.
        file_path (str): The path to the file within the repository.
        commit_ref (str): The commit hash, branch name, or tag (e.g., 'main', 'HEAD~1').

    Returns:
        Optional[str]: The content of the file as a string, or None if the file
                       could not be found at that commit.
    """
    try:
        # Initialize the repository object
        repo = git.Repo(repo_path, search_parent_directories=True)
        
        # Get the specified commit
        commit = repo.commit(commit_ref)
        
        # Find the file (blob) in the commit's tree
        blob = commit.tree / file_path
        
        # Read and decode the file content
        return blob.data_stream.read().decode('utf-8')
        
    except (git.exc.GitCommandError, KeyError, ValueError) as e:
        print(f"Error accessing file '{file_path}' at commit '{commit_ref}': {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

def get_changed_files_in_dir(repo_path: str, dir_path: str, old_commit_ref: str, new_commit_ref: str) -> list[str]:
    """
    Retrieves a list of changed Python files within a specific directory between two commits.

    Args:
        repo_path (str): The path to the local Git repository.
        dir_path (str): The specific directory to check for changes.
        old_commit_ref (str): The old commit hash or reference.
        new_commit_ref (str): The new commit hash or reference.

    Returns:
        list[str]: A list of file paths relative to the repo root that have changed.
    """
    changed_files = []
    try:
        repo = git.Repo(repo_path, search_parent_directories=True)
        old_commit = repo.commit(old_commit_ref)
        new_commit = repo.commit(new_commit_ref)

         # Handle the case where the directory is the repo root ('.').
        # A file path like 'src/main.py' does not start with '.', so the check would fail.
        # By using an empty string, the startswith check will pass for any file path.
        effective_dir_path = '' if dir_path == '.' else dir_path
        diff_index = old_commit.diff(new_commit)

        print ("diff_index: ",diff_index)
        for diff_item in diff_index:
            # Check for added (A) or modified (M) files
            if diff_item.change_type in ('A', 'M'):
                file_path = diff_item.a_path
                print("file_path: ",file_path)
                # Check if the file is a Python file and is within the specified directory
                if file_path.endswith('.py') and file_path.startswith(effective_dir_path):
                    changed_files.append(file_path)
                    
    except Exception as e:
        print(f"An error occurred while detecting changed files: {e}")

    return changed_files

if __name__ == '__main__':
    # Example usage:
    # This assumes you are running this from a directory within a git repository.
    # For example, to get the content of this file from the latest commit:
    print("--- Testing Git Utils ---")
    try:
        repo_root = git.Repo(search_parent_directories=True).git.rev_parse("--show-toplevel")
        this_file_path = os.path.relpath(__file__, repo_root)
        
        print(f"Repo path: {repo_root}")
        print(f"File path: {this_file_path}")

        content = get_file_content_from_commit(
            repo_path=repo_root, 
            file_path=this_file_path, 
            commit_ref='HEAD'
        )

        if content:
            print(f"\nSuccessfully retrieved content for {this_file_path} at HEAD:")
            print("-" * 20)
            print(content.split('\n')[0] + "...") # Print first line
            print("-" * 20)
        else:
            print("\nFailed to retrieve content.")

    except Exception as e:
        print(f"Test failed: {e}")