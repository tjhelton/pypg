# Claude Development Guide

This file contains helpful commands and workflows for Claude when working on the py-sc repository.

## ⚠️ CRITICAL: GitHub Contribution Rules

**IMPORTANT**: This repository is PUBLIC with branch protection rules requiring PRs and status checks.

### Git Configuration Requirements
When performing ANY git operations (commits, PRs, etc.), you MUST:
- **NEVER** use Claude Code attribution in commits
- **ALWAYS** use the repository owner's identity:
  - **Username**: `@tjhelton`
  - **Email**: `tjhelton99@gmail.com`
- **NEVER** include Claude attribution in commit messages (no "🤖 Generated with Claude Code" or "Co-Authored-By: Claude")

### Pull Request Requirements
This repository enforces:
- **Branch protection**: Cannot push directly to `main`
- **Required PRs**: All changes must go through pull request workflow
- **Status checks**: GitHub Actions linting must pass before merge
- **Clean history**: All commits must appear as authored by @tjhelton

### Workflow for Changes
1. Create feature branch from `main`
2. Make changes and commit (using tjhelton99@gmail.com)
3. **SECURITY CHECK**: Clear all tokens before commit (see below)
4. Ensure pre-commit hooks are installed (`cd tools/ && make pre-commit`)
5. Push branch to remote (pre-commit hooks will run automatically)
6. Create PR manually via GitHub web UI at the URL provided in push output
7. Wait for status checks to pass
8. Merge only when checks are green

### Commit Strategy
**IMPORTANT**: When working on multiple changes, create separate commits for each logical unit of work.

**Benefits of atomic commits**:
- Clear, detailed git history
- Easier code review
- Better rollback capabilities
- Each commit tells a complete story

**Guidelines**:
- **Group related changes**: Changes to the same feature/file that are interdependent
- **Separate distinct concerns**: Different types of changes should be different commits
- **Examples**:
  - ✅ GOOD: Separate commits for "Add gitignore patterns", "Clear exposed tokens", "Add security docs"
  - ❌ BAD: Single commit "Update security" that does all three
- **Single PR**: All commits go on one feature branch, then create one PR

**Commit message format**:
```
Brief summary of what changed (imperative mood)

- Specific detail about change 1
- Specific detail about change 2
- Why this change was necessary
```

### Creating Pull Requests
**IMPORTANT**: Always use git commands, NEVER use CLI tools like `gh`.
- After pushing branch, git will provide a URL to create the PR
- Visit the URL and create PR manually via GitHub web UI
- Example URL format: `https://github.com/tjhelton/py-sc/pull/new/your-branch-name`
- PR creation via API requires authentication setup

### Pre-Commit Security Checks (MANDATORY)
**CRITICAL**: Before ANY commit or PR, you MUST:

1. **Search for exposed tokens**:
   ```bash
   # Search for TOKEN variables with non-empty values
   grep -r "TOKEN\s*=\s*['\"][^'\"]\+['\"]" --include="*.py" .
   ```

2. **Clear all token values**:
   - Find patterns like: `TOKEN = "scapi_..."`
   - Replace with: `TOKEN = ""`
   - Look for: `API_KEY`, `API_TOKEN`, `SECRET`, `PASSWORD`, etc.
   - Check all script directories, especially new additions

3. **Verify clean state**:
   ```bash
   git diff  # Review all changes for sensitive data
   ```

4. **Common token patterns to check**:
   - `TOKEN = "scapi_..."`
   - `API_KEY = "..."`
   - `API_TOKEN = "..."`
   - `SECRET = "..."`
   - `PASSWORD = "..."`
   - Any bearer tokens or authentication strings

**NEVER commit actual API tokens, keys, or secrets to the repository.**

## 🚀 Quick Commands

### Linting and Code Quality
```bash
# Run from repository root
cd tools/
make lint      # Check code quality
make fix       # Auto-fix formatting issues
make help      # See all available commands
```

### Pre-commit Setup
```bash
cd tools/
make install     # Install development dependencies
make pre-commit  # Set up pre-commit hooks
```

### Testing Linting Before PR
```bash
cd tools/
make lint                    # Check for issues
python3 lint-and-fix.py --fix  # Apply fixes
git status --porcelain       # Verify no changes (should be clean)
```

## 📁 Repository Structure

```
py-sc/
├── archive_templates/              # SafetyCulture template archiver
├── create_groups/                  # Group creation functionality
├── create_sites/                   # SafetyCulture site creator
├── delete_sites/                   # Site deletion functionality
├── export_asset_types/             # Asset types export
├── export_template_access_rules/   # Template access rules export
├── fetch_issues/                   # Issues fetching (advanced async)
├── get_public_issue_links/         # Public issue links retrieval
├── get_sites_without_activity/     # Sites without activity report
├── set_inspection_site/            # Inspection site configuration
├── update_user_sites/              # User sites update functionality
├── tools/                          # 🔧 Development tools
│   ├── CONTRIBUTE.md               # Contribution guidelines
│   ├── Makefile                    # Development commands
│   ├── lint-and-fix.py             # Main linting script
│   ├── pyproject.toml              # Tool configurations
│   ├── .flake8                     # Flake8 configuration
│   ├── .pre-commit-config.yaml     # Pre-commit setup
│   └── requirements-dev.txt        # Development dependencies
├── .github/workflows/pylint.yml    # GitHub Actions CI
├── .gitignore                      # Git ignore rules
├── .vscode/settings.json           # VS Code configuration
├── README.md                       # Main documentation
└── CLAUDE.md                       # This file
```

## 🛠️ Development Workflow

### Making Changes to Scripts
1. Navigate to the specific script directory
2. Make your changes to `main.py`
3. Test the script functionality
4. Run linting from `tools/` directory:
   ```bash
   cd tools/
   make lint
   make fix  # if needed
   ```
5. Commit changes

### Adding New Scripts
1. Create new directory with descriptive name
2. Add `main.py` with the script logic
3. Create `README.md` following the standardized format:
   ```markdown
   # Script Name

   Brief description of what the script does.

   ## Quick Start

   1. **Install dependencies**: `pip install pandas requests`
   2. **Set API token**: Replace `TOKEN = ''` with your SafetyCulture API token
   3. **Prepare input**: Create `input.csv` with required format
   4. **Run script**: `python main.py`

   ## Prerequisites

   - Python 3.8+ and pip
   - Valid SafetyCulture API token
   - Input CSV with required data

   ## Input Format

   Create `input.csv` with:
   ```csv
   column1,column2
   value1,value2
   ```

   ## Output

   Generates `output.csv` with:
   - Column descriptions

   ## API Reference

   - Endpoint: API endpoint used
   - [Documentation](link)

   ## Notes

   - Key points about the script
   ```
4. Update linting configuration in `tools/lint-and-fix.py` to include new directory
5. Update `tools/pyproject.toml` configurations to include new paths
6. Update main `README.md` to include new script in the directory listing

### Repository Configuration Files

#### All linting is handled from `tools/` directory:
- **pyproject.toml**: Black, isort, mypy configuration
- **.flake8**: Flake8 linting rules
- **.pre-commit-config.yaml**: Pre-commit hooks setup
- **lint-and-fix.py**: Main linting script targeting all script directories
- **Makefile**: Development commands

#### Key settings:
- **Line length**: 88 characters (Black standard)
- **String preservation**: `--skip-string-normalization` (keeps API URLs safe)
- **Import sorting**: Conservative mode to preserve functionality
- **Type checking**: Relaxed mypy settings, skipped due to duplicate main.py conflicts

## 📊 Script Patterns

### Standard Authentication
All scripts use the same authentication pattern:
```python
TOKEN = ''  # Set your SafetyCulture API token here
```

### Standard Input/Output
- **Input**: `input.csv` with relevant data
- **Output**: `output.csv` or timestamped directories
- **Progress**: Terminal logging for user feedback

### API Best Practices
- Always use proper headers with Bearer token
- Include error handling and retry logic
- Preserve existing string quotes (API URLs, tokens)
- Use appropriate timeouts and rate limiting

## 🔧 VS Code Integration

The `.vscode/settings.json` provides:
- **Auto-formatting**: Black formatting on save
- **Import sorting**: Automatic isort on save
- **Linting**: Real-time flake8 feedback
- **File exclusions**: Hides cache files and sensitive data
- **88-character ruler**: Visual line length guide

## 🚨 Important Notes

### Security
- Never commit API tokens or sensitive data
- All `*.csv`, `*.json`, `*.xlsx` files are gitignored by default
- Use environment variables for tokens in advanced scripts

### Code Quality
- All linting must be run from `tools/` directory
- GitHub Actions enforces same linting standards
- Pre-commit hooks prevent bad commits
- String preservation protects API URLs from being reformatted

### Testing Changes
Before creating PR:
```bash
cd tools/
make lint     # Should pass completely
git status --porcelain  # Should show no Python file changes after linting
```

## 📚 Common Tasks

### Update script directory targeting
If adding/removing script directories, update these files:
1. `tools/lint-and-fix.py` - script_patterns list
2. `tools/pyproject.toml` - src_paths and files lists
3. `tools/.pre-commit-config.yaml` - files regex pattern
4. Main `README.md` - Available Scripts section

### Fix linting issues
```bash
cd tools/
make fix     # Automatically fixes what it can
make lint    # Check remaining issues
# Manually fix any remaining flake8 issues that can't be auto-fixed
```

### Clean up temporary files
```bash
cd tools/
make clean   # Removes __pycache__, .mypy_cache, *.pyc, etc.
```

This repository is designed for safe, automated SafetyCulture API operations with strong code quality standards and comprehensive documentation.
