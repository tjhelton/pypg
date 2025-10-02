# py-sc

A collection of Python automation scripts for SafetyCulture API operations. Provides tools for bulk management of templates, sites, issues, and other SafetyCulture resources.

## 🚀 Quick Start

```bash
# Clone the repository
git clone https://github.com/your-username/py-sc.git
cd py-sc

# Install dependencies
pip install -r requirements.txt

# Set up development environment (optional)
cd contribution_tools/
make install
make pre-commit

# Run any script
cd ../archive_templates/
# Set your API token in main.py
python main.py
```

## 📁 Available Scripts

> **💡 Each script has its own README with detailed setup instructions, input formats, and usage examples. Click any script link below to view its complete documentation.**

### Template Management
- **[archive_templates/](archive_templates/)** - Archive SafetyCulture templates in bulk
- **[export_template_access_rules/](export_template_access_rules/)** - Export template permission matrices

### Site Management
- **[create_groups/](create_groups/)** - Create SafetyCulture groups
- **[create_sites/](create_sites/)** - Create SafetyCulture sites with hierarchy support
- **[delete_sites/](delete_sites/)** - Delete SafetyCulture sites in bulk
- **[get_sites_without_activity/](get_sites_without_activity/)** - Identify inactive sites
- **[set_inspection_site/](set_inspection_site/)** - Configure audit-site relationships
- **[update_user_sites/](update_user_sites/)** - Bulk update user site assignments

### Issues, Actions & Assets
- **[delete_actions/](delete_actions/)** - Delete SafetyCulture actions in bulk (batches of 300)
- **[delete_assets/](delete_assets/)** - Archive SafetyCulture assets with detailed logging
- **[export_asset_types/](export_asset_types/)** - Export asset type definitions
- **[fetch_issues/](fetch_issues/)** - Extract all issues with detailed tracking data
- **[get_public_issue_links/](get_public_issue_links/)** - Generate public sharing links

## 🛠️ Development

### Code Quality
This project uses automated linting and formatting tools. **All linting commands must be run from the `contribution_tools/` directory**:

```bash
cd contribution_tools/
make lint      # Check code quality
make fix       # Auto-fix formatting issues
make help      # See all available commands
```

### Pre-commit Hooks
Automatically format and lint code before commits:

```bash
cd contribution_tools/
make pre-commit
```

### GitHub Actions
- Automated code quality checks on all pull requests
- Linting and formatting validation
- Ensures consistent code standards

## 📋 Prerequisites

- **Python 3.8+** with pip
- **SafetyCulture API Token** - [Get yours here](https://developer.safetyculture.com/reference/getting-started)
- **API Access** - Appropriate permissions for your use case

## 🔧 Dependencies

Install all required dependencies for the scripts:
```bash
pip install -r requirements.txt
```

This installs:
- **pandas** - CSV data processing and manipulation
- **requests** - HTTP requests to SafetyCulture API
- **aiohttp** - Async HTTP requests (for concurrent processing scripts)

## 📖 Usage Patterns

### Standard Workflow
1. Install dependencies: `pip install -r requirements.txt`
2. Navigate to desired script directory
3. Set API token in `main.py` or environment variable
4. Prepare `input.csv` (if required)
5. Run `python main.py`
6. Check output files

### Authentication Methods
- **Token in script**: `TOKEN = 'your-token-here'` (most scripts)
- **Environment variable**: `export SC_API_TOKEN="your-token-here"` (advanced scripts)

## 📊 Input/Output Formats

### Standard Input
Most scripts expect `input.csv` with relevant IDs or parameters. See individual script READMEs for specific formats.

### Standard Output
- CSV files with processing results
- Timestamped output directories (for complex scripts)
- Terminal progress logging

## ⚠️ Important Notes

- **Security**: Never commit API tokens or sensitive data
- **Testing**: Always test with small datasets first
- **Irreversible**: Many operations (delete, archive) cannot be undone
- **Rate Limits**: Scripts include appropriate delays and retry logic

## 📚 API Documentation

- [SafetyCulture API Reference](https://developer.safetyculture.com/reference/)
- [Getting Started Guide](https://developer.safetyculture.com/reference/getting-started)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Follow our [contribution guide](contribution_tools/CONTRIBUTE.md)
4. Run `make lint` before committing
5. Submit a pull request

## 📄 License

This project is provided as-is for SafetyCulture API automation. Use responsibly and in accordance with SafetyCulture's terms of service.
