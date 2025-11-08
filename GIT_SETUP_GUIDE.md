# GitHub SSH Authentication Setup Guide

## Problem
```
git@github.com: Permission denied (publickey).
fatal: Could not read from remote repository.
```

This means Git can't authenticate with GitHub using SSH.

## Solution Options

### Option 1: Switch to HTTPS (Easiest/Fastest)

```bash
# Check current remote URL
git remote -v

# Change from SSH to HTTPS
git remote set-url origin https://github.com/IGitGotIt/AITextProcessing.git

# Now try pushing
git push origin main
# or
git push origin master
```

**Pros:**
- Quick fix, works immediately
- Uses username/password or personal access token

**Cons:**
- Need to enter credentials each time (unless cached)
- Slightly less secure than SSH

---

### Option 2: Set Up SSH Key (More Secure)

#### Step 1: Check for Existing SSH Keys

```bash
ls -la ~/.ssh
# Look for: id_rsa and id_rsa.pub (or id_ed25519 and id_ed25519.pub)
```

#### Step 2: Generate New SSH Key (if needed)

```bash
# Generate new SSH key
ssh-keygen -t ed25519 -C "your_email@example.com"

# Press Enter to accept default location
# Enter passphrase (optional but recommended)
```

#### Step 3: Start SSH Agent

```bash
# Start the ssh-agent
eval "$(ssh-agent -s)"

# Add your key to the agent
ssh-add ~/.ssh/id_ed25519
```

#### Step 4: Copy Public Key

```bash
# Copy your public key to clipboard
cat ~/.ssh/id_ed25519.pub | pbcopy

# Or just display it
cat ~/.ssh/id_ed25519.pub
```

#### Step 5: Add Key to GitHub

1. Go to GitHub.com
2. Click your profile picture → **Settings**
3. Click **SSH and GPG keys** (left sidebar)
4. Click **New SSH key**
5. Title: "My Mac" (or whatever you want)
6. Paste the key (from Step 4)
7. Click **Add SSH key**

#### Step 6: Test Connection

```bash
# Test SSH connection to GitHub
ssh -T git@github.com

# Expected output:
# Hi IGitGotIt! You've successfully authenticated, but GitHub does not provide shell access.
```

#### Step 7: Configure SSH Config (Optional)

```bash
# Create/edit SSH config
nano ~/.ssh/config

# Add these lines:
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
```

---

### Option 3: Use Personal Access Token (Alternative to SSH)

If you switched to HTTPS (Option 1), you'll need a token instead of password:

#### Step 1: Create Personal Access Token

1. Go to GitHub.com
2. Click profile picture → **Settings**
3. Scroll down → **Developer settings** (bottom left)
4. Click **Personal access tokens** → **Tokens (classic)**
5. Click **Generate new token** → **Generate new token (classic)**
6. Give it a name: "Mac Git Access"
7. Select scopes: Check **repo** (full control of private repositories)
8. Click **Generate token**
9. **COPY THE TOKEN NOW** - you won't see it again!

#### Step 2: Use Token When Pushing

```bash
# When Git asks for password, use the token instead
git push origin main

# Username: IGitGotIt
# Password: <paste your token here>
```

#### Step 3: Cache Credentials (Optional)

```bash
# Cache credentials for 1 hour (3600 seconds)
git config --global credential.helper 'cache --timeout=3600'

# Or store permanently (less secure)
git config --global credential.helper store
```

---

## Quick Fix Commands

### If You Just Want to Push Right Now:

```bash
# 1. Switch to HTTPS
git remote set-url origin https://github.com/IGitGotIt/AITextProcessing.git

# 2. Check if it worked
git remote -v

# 3. Try pushing again
git push origin main
# If no 'main' branch, try:
git push origin master
# Or check your branch:
git branch
```

---

## Verify Your Setup

```bash
# Check remote URL
git remote -v

# Should show one of:
# SSH: git@github.com:IGitGotIt/AITextProcessing.git
# HTTPS: https://github.com/IGitGotIt/AITextProcessing.git

# Check current branch
git branch

# Check git config
git config --list | grep remote
```

---

## Common Issues & Solutions

### Issue 1: "fatal: 'origin' does not appear to be a git repository"

```bash
# Add remote
git remote add origin https://github.com/IGitGotIt/AITextProcessing.git
```

### Issue 2: "Updates were rejected because the remote contains work..."

```bash
# Pull first, then push
git pull origin main --allow-unrelated-histories
git push origin main
```

### Issue 3: "Support for password authentication was removed"

This happens with HTTPS - you MUST use a Personal Access Token instead of password.

### Issue 4: Branch name mismatch

```bash
# Check your local branch name
git branch

# If it's 'master' but remote is 'main':
git branch -M main
git push origin main

# Or vice versa
```

---

## My Recommendation

**For Quick Fix:** Use Option 1 (HTTPS) + Personal Access Token

**For Long Term:** Use Option 2 (SSH Key) - more secure and convenient

---

## Step-by-Step Quick Fix

```bash
# 1. Switch to HTTPS
git remote set-url origin https://github.com/IGitGotIt/AITextProcessing.git

# 2. Verify
git remote -v

# 3. Create Personal Access Token on GitHub
#    (Settings → Developer settings → Personal access tokens → Generate new token)
#    Select 'repo' scope, copy the token

# 4. Try pushing
git push origin main

# 5. When prompted:
#    Username: IGitGotIt
#    Password: <paste your token>

# 6. (Optional) Cache credentials
git config --global credential.helper store
```

---

## Need More Help?

Run these diagnostic commands and share the output:

```bash
# Check remote
git remote -v

# Check branch
git branch

# Check status
git status

# Test GitHub connection
ssh -T git@github.com

# Check SSH keys
ls -la ~/.ssh
```
