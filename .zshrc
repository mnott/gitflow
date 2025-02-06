# Git worktree navigation
function cdworktree() {
    local branch="$1"
    if [[ -z "$branch" ]]; then
        echo "Usage: cdworktree <branch-name>"
        return 1
    fi

    # Get all output first to avoid multiple calls
    local all_output=$(gf ls --format plain 2>/dev/null)

    # First try to find a worktree for the requested branch
    local line=$(echo "$all_output" | grep -F "$branch" | head -n1)
    local worktree_path=$(echo "$line" | grep -o '<[^>]*>' | sed 's/^<\(.*\)>$/\1/')

    if [[ -n "$worktree_path" && -d "$worktree_path" ]]; then
        cd "$worktree_path"
        return
    fi

    # If no worktree found for the branch, try to find the main repository
    # Look for the current branch's worktree
    local current_branch=$(git rev-parse --abbrev-ref HEAD 2>/dev/null)
    local main_repo=$(echo "$all_output" | grep -F "$current_branch" | grep -o '<[^>]*>' | sed 's/^<\(.*\)>$/\1/')

    # Verify the branch exists
    if git rev-parse --verify "$branch" >/dev/null 2>&1; then
        if [[ -n "$main_repo" && -d "$main_repo" ]]; then
            if [[ "$PWD" != "$main_repo" ]]; then
                cd "$main_repo"
                echo "Note: '$branch' is not in a worktree, changing to main repository at $main_repo"
            fi
        else
            echo "Could not determine main repository location"
            return 1
        fi
    else
        echo "No worktree or branch found for '$branch'"
        return 1
    fi
}