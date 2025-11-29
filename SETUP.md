# 🚀 Pre-Phase 1 Setup Instructions

**Complete these steps before proceeding to Phase 1 implementation**

---

## ✅ Step 1: Verify Python Version

Ensure you have Python 3.10 or higher installed:

```bash
python --version
# Should show: Python 3.10.x or higher
```

If not, install Python 3.10+ from [python.org](https://www.python.org/downloads/)

---

## ✅ Step 2: Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
# venv\Scripts\activate

# Verify activation (you should see (venv) in your prompt)
which python  # Should point to venv/bin/python
```

---

## ✅ Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# This will install:
# - Core: numpy, pandas, faiss-cpu
# - LLM: google-generativeai
# - UI: streamlit
# - Physics: uproot, awkward, vector, coffea
# - Viz: matplotlib, mplhep
# - Utils: python-dotenv, tqdm, requests
# - Notebooks: jupyter, notebook, ipywidgets
# - Dev: pytest, pytest-cov, black, flake8, mypy

# Expected install time: 3-5 minutes
```

**Note**: If you encounter any installation errors:
- For FAISS: Make sure you have a C++ compiler installed
- For awkward/vector: These may take longer to compile on first install
- If a package fails, try installing it individually: `pip install package-name`

---

## ✅ Step 4: Get Gemini API Key

### 4a. Create API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click **"Get API key"** or **"Create API key"**
4. Copy the generated API key (starts with `AIza...`)

**Important**: Keep this key secure! Don't commit it to Git.

### 4b. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Open .env in your editor
nano .env  # or use your preferred editor: code .env, vim .env, etc.
```

### 4c. Update .env File

Edit `.env` and replace `your_api_key_here` with your actual Gemini API key:

```bash
# Before:
GEMINI_API_KEY=your_api_key_here

# After:
GEMINI_API_KEY=AIzaSyABC123...your_actual_key_here

# Keep other settings as default for now:
GEMINI_MODEL=gemini-2.0-flash-exp
GEMINI_EMBEDDING_MODEL=models/embedding-001
INDEX_PATH=./data/faiss_index
CORPUS_PATH=./src/rag/dataset/sample_corpus
CHUNK_SIZE=512
CHUNK_OVERLAP=50
```

Save and close the file.

### 4d. Verify API Key Works (Optional but Recommended)

Create a test script to verify your API key:

```bash
# Create test file
cat > test_gemini.py << 'EOF'
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

if not api_key or api_key == 'your_api_key_here':
    print("❌ ERROR: GEMINI_API_KEY not set in .env file!")
    exit(1)

print(f"✅ API Key found: {api_key[:20]}...")

try:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    
    # Test with a simple generation
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
    response = model.generate_content("Say 'API key works!'")
    print(f"✅ Gemini API test successful!")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ API test failed: {e}")
    print("Please check your API key and internet connection")
EOF

# Run the test
python test_gemini.py

# Clean up
rm test_gemini.py
```

Expected output:
```
✅ API Key found: AIzaSyABC123...
✅ Gemini API test successful!
Response: API key works!
```

---

## ✅ Step 5: Verify Installation

Run these commands to verify everything is installed correctly:

```bash
# 1. Check Python imports work
python -c "import numpy, pandas, faiss, streamlit, uproot, awkward; print('✅ All core packages imported successfully')"

# 2. Check Gemini package
python -c "import google.generativeai as genai; print('✅ Gemini package imported successfully')"

# 3. Verify project structure
ls -la src/
# Should show: main.py, physics/, rag/, ui/

# 4. Test that main.py runs
python src/main.py --help
# Should show CLI help without errors

# 5. Check Makefile commands
make help
# Should show all available make targets
```

---

## ✅ Step 6: Create Data Directory

The data directory will store the FAISS index and metadata:

```bash
# Create data directory (will be used in Phase 3)
mkdir -p data

# Verify .gitignore excludes it
cat .gitignore | grep "data/"
# Should show: data/
```

---

## ✅ Step 7: Test Development Tools (Optional)

```bash
# Test code formatter
make format
# Should format all Python files

# Test linter (may show some warnings - that's OK for now)
make lint

# Test that you can run tests (will show 0 tests for now)
make test
# Should show: "collected 0 items"
```

---

## ✅ Step 8: Verify Git Setup

```bash
# Check current branch
git branch
# Should show: * farouk/initial_setup

# Check status
git status
# Should show:
# - Modified: README.md
# - Modified: requirements.txt (if you edited it)
# - Untracked: All the new files from Phase 0

# Stage all Phase 0 files
git add .

# Commit Phase 0
git commit -m "Phase 0: Complete repository skeleton and foundation

- Add configuration files (LICENSE, Makefile, Dockerfile, .env.example)
- Create directory structure (src/rag, src/physics, src/ui, docs, tests, examples)
- Add placeholder Python modules with type hints and docstrings
- Create comprehensive documentation (architecture, chunking, retrieval)
- Set up development automation via Makefile
- Configure dependencies in requirements.txt"

# Verify commit
git log --oneline -1
# Should show your commit message
```

---

## ✅ Step 9: Final Verification Checklist

Before proceeding to Phase 1, ensure:

- [ ] ✅ Python 3.10+ is installed
- [ ] ✅ Virtual environment is created and activated
- [ ] ✅ All dependencies from requirements.txt are installed
- [ ] ✅ Gemini API key is obtained and configured in `.env`
- [ ] ✅ API key test passed (optional but recommended)
- [ ] ✅ All Python imports work without errors
- [ ] ✅ Project structure is verified
- [ ] ✅ Data directory is created
- [ ] ✅ Phase 0 changes are committed to Git

---

## 🎯 You're Ready for Phase 1 When...

All checkboxes above are ticked ✅

Once complete, simply tell the assistant:
```
"Ready for Phase 1"
```

And Phase 1 (Dataset Ingestion Module) will begin!

---

## 🆘 Troubleshooting

### Problem: FAISS installation fails

**Solution:**
```bash
# Try installing with conda instead
conda install -c conda-forge faiss-cpu

# Or use the GPU version if you have CUDA
pip install faiss-gpu
```

### Problem: awkward/vector compilation errors

**Solution:**
```bash
# Install build tools
# Ubuntu/Debian:
sudo apt-get install build-essential python3-dev

# macOS:
xcode-select --install

# Then retry:
pip install awkward vector
```

### Problem: "API key invalid" error

**Solution:**
- Double-check you copied the entire key (starts with `AIza`)
- Ensure no extra spaces in `.env` file
- Verify key is enabled at [Google AI Studio](https://makersuite.google.com/app/apikey)
- Check billing is enabled if using a paid tier

### Problem: Import errors after installation

**Solution:**
```bash
# Ensure virtual environment is activated
which python  # Should point to venv/bin/python

# If not, reactivate:
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Try reinstalling the problematic package:
pip install --force-reinstall package-name
```

### Problem: Permission denied errors

**Solution:**
```bash
# Don't use sudo with pip in a venv
# Instead, check venv is activated and retry

# If still failing, check directory permissions:
ls -la venv/
```

---

## 📞 Need Help?

If you encounter issues not covered here:
1. Check the error message carefully
2. Search for the error on Stack Overflow
3. Check package-specific documentation
4. Ask the assistant for help with the specific error

---

**Once all steps are complete, you're ready for Phase 1!** 🚀
