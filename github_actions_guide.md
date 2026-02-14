# How to Push from Repo A to Repo B in GitHub Actions

To allow your solver (Repo A) to update your video list (Repo B), follow these steps:

## 1. Create a GitHub Personal Access Token (PAT)
You need a token that gives the solver permission to write to the other repository.
1.  Go to **GitHub Settings** > **Developer Settings** > **Personal Access Tokens** > **Tokens (classic)**.
2.  Generate a new token with the `repo` scope.
3.  Copy this token.

## 2. Add the Token as a Secret in Repo A
1.  Go to the **Settings** of your `quor-dle-video` repository on GitHub.
2.  Go to **Secrets and variables** > **Actions**.
3.  Create a **New repository secret**:
    - **Name**: `VIDEO_REPO_PAT`
    - **Value**: (Paste your PAT here)

## 3. Update the Sync Script for URL with Token
Modified `update_repo.py` should use the token in the URL for authentication in Actions.
I will handle this in the code logic if `VIDEO_REPO_PAT` is found in the environment.

## 4. GitHub Actions Workflow (Example)
Add these steps to your `.github/workflows/daily_solve.yml`:

```yaml
- name: Run Solver and Sync
  env:
    YOUTUBE_CLIENT_SECRET: ${{ secrets.YOUTUBE_CLIENT_SECRET }}
    VIDEO_REPO_PAT: ${{ secrets.VIDEO_REPO_PAT }}
  run: |
    # Your solver run command here
    python quor-dle-video/solver.py
```

## Why your manual commands failed:
1.  `git add README.md`: You didn't have a `README.md` file in the folder.
2.  `git commit`: You hadn't "staged" (added) any files first.
3.  `git push`: You can't push an empty repository. You must have at least one commit.
