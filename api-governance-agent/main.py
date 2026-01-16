import argparse
import datetime
from src.graph.workflow import create_governance_graph
from src.graph.state import GovernanceState
from src.utils.git_utils import get_file_content_from_commit, get_changed_files_in_dir
import os
from dotenv import load_dotenv

load_dotenv()

def run_validation_from_git(repo_path: str, old_commit: str, new_commit: str, dir_path: str = "."):
    """
    Fetches code from a specific directory in a Git repository and runs the validation workflow.
    """
    import git
    print("--- Running Validation on Git Changes ---")

    try:
        # Validate that the provided path is a Git repository
        repo = git.Repo(repo_path)
        print(f"Successfully loaded Git repository from: {repo_path}")
    except (git.exc.InvalidGitRepositoryError, git.exc.NoSuchPathError):
        print(f"Error: The provided path '{repo_path}' is not a valid Git repository.")
        return

    # Create a single parent output directory for this run inside the agent's directory
    agent_root = os.path.dirname(__file__) # Root of the agent script
    timestamp = datetime.datetime.now().strftime("%Y%m%d")
    parent_output_dir = os.path.join(agent_root, "output", timestamp)
    os.makedirs(parent_output_dir, exist_ok=True)
    print(f"--- Artifacts will be saved to: {parent_output_dir} ---")

    # Use the provided repo_path and dir_path to find changed files
    # dir_path should be relative to the root of the repository
    print(f"Searching for changed files in directory '{dir_path}'...")
    changed_files = get_changed_files_in_dir(repo.working_dir, dir_path, old_commit, new_commit)

    if not changed_files:
        print("No changed Python files found in the specified directory and commit range.")
        return
    print(f"Found {len(changed_files)} changed files to analyze.")

    # Process each changed file
    for file_path in changed_files:
        print(f"\n--- Analyzing file: {file_path} ---")
        
        # Create a specific subdirectory for this file's artifacts
        # Sanitize file_path to create a valid directory name
        file_specific_dir_name = file_path.replace('/', '_').replace('.', '_')
        file_output_dir = os.path.join(parent_output_dir, file_specific_dir_name)
        
        # Pass the repo_path for context and the relative file_path to git
        old_code = get_file_content_from_commit(repo.working_dir, file_path, old_commit)
        new_code = get_file_content_from_commit(repo.working_dir, file_path, new_commit) or ''

        if old_code is None: # Handle newly added files
             old_code = ''
        
        run_workflow(old_code, new_code, file_output_dir)

def run_validation_from_demo():
    """Runs the validation workflow on hardcoded demo code."""
    print("--- Running Validation on Demo Code ---")
    
    # Create a single parent output directory for this run
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join("output", f"demo_{timestamp}")
    
    OLD_CODE = '''
import Flask
app = Flask(__name__)
# No endpoints defined yet.
if __name__ == "__main__":
    app.run()
'''

    NEW_CODE = '''
import Flask
from flask import jsonify

app = Flask(__name__)

# Endpoint to get user details
@app.route("/user-details/getUser")
def get_user_details():
    # In a real scenario, you'd fetch user data here.
    user_data = { "userId": 123, "fullName": "John Doe" }
    return jsonify(user_data)

if __name__ == "__main__":
    app.run()
'''
    run_workflow(OLD_CODE, NEW_CODE, output_dir)


def run_workflow(old_code: str, new_code: str, output_dir: str):
    """
    Initializes and runs the API governance validation workflow, saving all
    artifacts to the specified output directory.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Save input code to files
    with open(os.path.join(output_dir, "old_code.py"), "w") as f:
        f.write(old_code)
    with open(os.path.join(output_dir, "new_code.py"), "w") as f:
        f.write(new_code)

    # Initialize and Run the Graph
    app = create_governance_graph()

    initial_state: GovernanceState = {
        "old_code": old_code,
        "new_code": new_code,
        "changed_code": "",
        "query": "",
        "relevant_docs": [],
        "validation_results": [],
        "report": "",
        "error": None,
    }

    final_state = app.invoke(initial_state)

    # Save the results from the final state
    with open(os.path.join(output_dir, "changed_snippet.txt"), "w") as f:
        f.write(final_state.get("changed_code", "No changed code detected."))
    
    with open(os.path.join(output_dir, "report.md"), "w") as f:
        f.write(final_state.get("report", "No report was generated."))


    # Display the Final Report
    print("\n--- Governance Report ---")
    if final_state.get("error"):
        print(f"An error occurred: {final_state['error']}")
    else:
        print(final_state.get("report", "No report was generated."))
    print("-------------------------")
    print(f"Full report and artifacts saved in: {output_dir}")


def main():
    # --- Verify API Key ---
    if not os.getenv("OPENAI_API_KEY"):
        print("FATAL: OPENAI_API_KEY is not set.")
        print("Please create a .env file and add your key.")
        return

    parser = argparse.ArgumentParser(description="API Governance Agent powered by LLMs.")
    parser.add_argument(
        '--repo-path', 
        type=str, 
        help="The absolute path to the local Git repository to check."
    )
    parser.add_argument(
        '--dir-path', 
        type=str, 
        default=".", 
        help="Optional: A specific directory path within the repository to analyze. Defaults to the repo root."
    )
    parser.add_argument(
        '--old-commit', 
        type=str, 
        help="The old commit hash or reference (e.g., 'main', 'HEAD~1')."
    )
    parser.add_argument(
        '--new-commit', 
        type=str, 
        help="The new commit hash or reference (e.g., 'HEAD')."
    )
    
    args = parser.parse_args()

    if args.repo_path and args.old_commit and args.new_commit:
        run_validation_from_git(args.repo_path, args.old_commit, args.new_commit, args.dir_path)
    else:
        print("No Git arguments provided (--repo-path, --old-commit, --new-commit are required). Running demo...")
        run_validation_from_demo()


if __name__ == "__main__":
    main()
