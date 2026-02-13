# Pull Request and Deployment Guide

## Pull Request Process

### Creating a Pull Request

1. **Create a feature branch** from `develop` or `main`:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and commit them:
   ```bash
   git add .
   git commit -m "Description of your changes"
   git push origin feature/your-feature-name
   ```

3. **Open a Pull Request** on GitHub:
   - Go to the repository on GitHub
   - Click "New Pull Request"
   - Select your feature branch
   - Fill in the PR description with:
     - What changes were made
     - Why the changes were needed
     - How to test the changes

### PR Approval Requirements

For branches targeting `main`:
- ✅ All CI tests must pass
- ✅ PR checks must pass
- ✅ Code review approval required (recommended)
- ✅ No merge conflicts

For branches targeting `develop`:
- ✅ All CI tests must pass
- ✅ PR checks must pass

### Required Status Checks

The following checks must pass before merging:
1. **Test Application** - Runs pytest, generates demo data, verifies syntax
2. **PR Validation** - Validates PR structure and commits

## Deployment Process

### Automatic Deployment

The application automatically deploys to Render when:
- Changes are merged to the `main` branch
- All tests pass
- Docker build succeeds

### Deployment Configuration

The deployment is configured via `render.yaml`:
- **Service Type**: Web service
- **Runtime**: Docker
- **Branch**: main (auto-deploy enabled)
- **Health Check**: `/_stcore/health`
- **Port**: Configured via Render's `PORT` environment variable

### Manual Deployment

To manually deploy:
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Find the `oppstarter` service
3. Click "Manual Deploy" → "Deploy latest commit"

### Environment Variables

Configure in Render Dashboard:
- `AI_ENABLED`: Set to `true` for production
- `GEMINI_API_KEY`: Your Google Gemini API key (keep secret!)

### Deployment Verification

After deployment:
1. Visit your Render URL
2. Check the health endpoint: `https://your-app.onrender.com/_stcore/health`
3. Verify the application loads correctly
4. Test key functionality

## Branch Protection Rules (Recommended)

To configure branch protection for `main`:

1. Go to Settings → Branches → Add rule
2. Branch name pattern: `main`
3. Enable:
   - ☑️ Require a pull request before merging
   - ☑️ Require approvals (1 reviewer recommended)
   - ☑️ Require status checks to pass before merging
     - Select: `Test Application`
     - Select: `PR Validation`
   - ☑️ Require branches to be up to date before merging
   - ☑️ Do not allow bypassing the above settings

## Workflow Details

### CI/CD Pipeline (`ci.yml`)

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main` or `develop`
- Manual workflow dispatch

**Jobs:**
1. **test** - Runs on all triggers
   - Installs dependencies
   - Runs pytest
   - Generates demo data
   - Verifies Python syntax

2. **build** - Runs on main branch pushes
   - Builds Docker image
   - Uses BuildKit caching
   - Tests image build

3. **deploy** - Runs on main branch pushes after build
   - Notifies about Render deployment
   - Provides deployment information

### PR Checks (`pr-checks.yml`)

**Triggers:**
- Pull request opened, synchronized, reopened, or marked ready for review
- Targets `main` or `develop` branches

**Jobs:**
1. **pr-validation**
   - Validates PR structure
   - Checks for description
   - Validates commits
   - Marks PR ready for review

## Troubleshooting

### Tests Failing
- Check pytest output in Actions tab
- Run tests locally: `cd opportunity-engine && pytest -v`

### Deployment Failed
- Check Render logs in dashboard
- Verify environment variables are set
- Check health endpoint

### Merge Conflicts
- Rebase your branch on latest main/develop
- Resolve conflicts locally
- Push changes (if needed): `git push --force-with-lease`
  - ⚠️ **Warning**: Only use force push on your own feature branches
  - Never force push to shared branches (main, develop)
  - Use `--force-with-lease` instead of `--force` for safety

## Best Practices

1. **Keep PRs small** - Easier to review and merge
2. **Write tests** - Maintain code quality
3. **Update documentation** - Keep README and docs current
4. **Test locally** - Before pushing changes
5. **Descriptive commits** - Clear commit messages
6. **Review before merging** - Have another developer review your code
