# scripts/setup_project.py

import os
import shutil
from pathlib import Path
import json
from datetime import datetime
import subprocess

class ProjectSetup:
    """Setup the project directory structure and initial files"""
    
    def __init__(self, project_name="legal-tax-llm", root_dir=None):
        self.project_name = project_name
        self.root_dir = Path(root_dir or Path.cwd()) / project_name
        self.created_dirs = []
        self.created_files = []
        
    def create_directory_structure(self):
        """Create all required directories"""
        
        directories = [
            # Data directories
            "data/raw/nta",
            "data/raw/ntaa",
            "data/interim/extracted/nta",
            "data/interim/extracted/ntaa",
            "data/interim/ocr_outputs/nta",
            "data/interim/ocr_outputs/ntaa",
            "data/interim/inspections",
            "data/processed/nta/cleaned",
            "data/processed/nta/structured",
            "data/processed/nta/chunked",
            "data/processed/ntaa/cleaned",
            "data/processed/ntaa/structured",
            "data/processed/ntaa/chunked",
            "data/final/train",
            "data/final/validation",
            "data/final/test",
            "data/final/datasets",
            
            # Source code directories
            "src/extraction",
            "src/preprocessing",
            "src/structuring",
            "src/chunking",
            "src/training",
            "src/utils",
            "src/config",
            
            # Test directories
            "tests/test_extraction",
            "tests/test_cleaning",
            "tests/test_structuring",
            "tests/test_chunking",
            
            # Documentation
            "docs",
            
            # Logs
            "logs/extraction",
            "logs/preprocessing",
            "logs/training",
            
            # Models
            "models/checkpoints",
            "models/final",
            "models/evaluation",
            
            # Outputs
            "outputs/reports/daily_reports",
            "outputs/reports/weekly_summaries",
            "outputs/visualizations",
            "outputs/metrics",
            
            # Notebooks
            "notebooks",
            
            # Scripts
            "scripts",
            
            # Metadata
            "metadata",
        ]
        
        for directory in directories:
            path = self.root_dir / directory
            path.mkdir(parents=True, exist_ok=True)
            self.created_dirs.append(str(path))
            print(f"✅ Created: {path}")
        
        return self.created_dirs
    
    def create_init_files(self):
        """Create __init__.py files for all Python packages"""
        
        init_dirs = [
            "src",
            "src/extraction",
            "src/preprocessing",
            "src/structuring",
            "src/chunking",
            "src/training",
            "src/utils",
            "src/config",
            "tests",
        ]
        
        for directory in init_dirs:
            init_file = self.root_dir / directory / "__init__.py"
            init_file.touch(exist_ok=True)
            self.created_files.append(str(init_file))
            
            # Add docstring to __init__.py
            with open(init_file, "w") as f:
                f.write(f'"""\n{directory.replace("/", " ").title()} Module\n"""\n')
            
            print(f"✅ Created: {init_file}")
    
    def create_config_files(self):
        """Create configuration files"""
        
        # Create config.yaml
        config_yaml = self.root_dir / "src/config/config.yaml"
        config_content = """
# Legal Tax LLM Configuration

project:
  name: "Legal Tax Domain-Specific LLM"
  version: "1.0.0"
  created_date: "2026-01-18"

data:
  raw_path: "data/raw/"
  interim_path: "data/interim/"
  processed_path: "data/processed/"
  final_path: "data/final/"
  
  documents:
    nta:
      file: "Nigeria_Tax_Act.pdf"
      metadata: "metadata/nta.json"
    ntaa:
      file: "Nigeria_Tax_Administration_Act.pdf"
      metadata: "metadata/ntaa.json"

extraction:
  methods:
    - pymupdf
    - pdfplumber
    - ocr
  
  ocr:
    language: "eng"
    psm: 6  # Page segmentation mode
    dpi: 300

preprocessing:
  cleaning:
    remove_special_chars: true
    normalize_whitespace: true
    correct_unicode: true
  
  legal_terms:
    preserve: true
    standardization: true

chunking:
  strategy: "semantic"
  max_chunk_size: 512
  overlap: 50

model:
  base_model: "gpt2"  # or other small model
  fine_tuning:
    epochs: 3
    learning_rate: 5e-5
    batch_size: 8
  
  evaluation:
    metrics: ["perplexity", "bleu", "rouge"]

logging:
  level: "INFO"
  format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
  file: "logs/training/training.log"

training:
  device: "cuda"  # or cpu
  seed: 42
  num_workers: 4
"""
        
        with open(config_yaml, "w") as f:
            f.write(config_content)
        self.created_files.append(str(config_yaml))
        print(f"✅ Created: {config_yaml}")
        
        # Create paths_config.py
        paths_config = self.root_dir / "src/config/paths_config.py"
        paths_content = '''from pathlib import Path

class PathsConfig:
    """Centralized path configuration"""
    
    ROOT = Path(__file__).parent.parent.parent
    
    # Data paths
    DATA_RAW = ROOT / "data/raw"
    DATA_INTERIM = ROOT / "data/interim"
    DATA_PROCESSED = ROOT / "data/processed"
    DATA_FINAL = ROOT / "data/final"
    
    # Document paths
    NTA_RAW = DATA_RAW / "nta/Nigeria_Tax_Act.pdf"
    NTAA_RAW = DATA_RAW / "ntaa/Nigeria_Tax_Administration_Act.pdf"
    
    NTA_EXTRACTED = DATA_INTERIM / "extracted/nta"
    NTAA_EXTRACTED = DATA_INTERIM / "extracted/ntaa"
    
    NTA_PROCESSED = DATA_PROCESSED / "nta"
    NTAA_PROCESSED = DATA_PROCESSED / "ntaa"
    
    # Metadata paths
    METADATA = ROOT / "metadata"
    NTA_METADATA = METADATA / "nta.json"
    NTAA_METADATA = METADATA / "ntaa.json"
    
    # Model paths
    MODELS = ROOT / "models"
    CHECKPOINTS = MODELS / "checkpoints"
    FINAL_MODELS = MODELS / "final"
    
    # Logs
    LOGS = ROOT / "logs"
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all directories exist"""
        for attr in dir(cls):
            if not attr.startswith("_") and attr.isupper():
                path = getattr(cls, attr)
                if isinstance(path, Path):
                    path.mkdir(parents=True, exist_ok=True)
'''
        
        with open(paths_config, "w") as f:
            f.write(paths_content)
        self.created_files.append(str(paths_config))
        print(f"✅ Created: {paths_config}")
    
    def create_initial_files(self):
        """Create initial project files"""
        
        # .gitignore
        gitignore = self.root_dir / ".gitignore"
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv
pip-log.txt
pip-delete-this-directory.txt
.pytest_cache/
.coverage
htmlcov/
.tox/
.mypy_cache/
.dmypy.json
dmypy.json
*.log

# Data files
data/raw/
data/interim/
data/processed/
data/final/
*.pdf
*.png
*.jpg
*.jpeg

# Model files
*.pth
*.pt
*.h5
*.pb
*.ckpt
models/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# Jupyter
.ipynb_checkpoints/
*.ipynb

# Environment
.env
.env.local
.env.*.local

# Outputs
outputs/
logs/
"""
        
        with open(gitignore, "w") as f:
            f.write(gitignore_content)
        self.created_files.append(str(gitignore))
        print(f"✅ Created: {gitignore}")
        
        # requirements.txt
        requirements = self.root_dir / "requirements.txt"
        requirements_content = """# Core dependencies
PyMuPDF==1.23.8
pdfplumber==0.10.3
pytesseract==0.3.10
Pillow==10.0.1

# Data processing
pandas==2.1.4
numpy==1.24.3
scikit-learn==1.3.2

# NLP and ML
transformers==4.36.0
torch==2.1.0
datasets==2.16.1
tokenizers==0.15.0
accelerate==0.25.0

# Utilities
tqdm==4.66.1
pyyaml==6.0.1
python-dotenv==1.0.0
click==8.1.7

# Development
pytest==7.4.3
black==23.11.0
flake8==6.1.0
jupyter==1.0.0

# Logging and monitoring
wandb==0.16.0
mlflow==2.7.1
"""
        
        with open(requirements, "w") as f:
            f.write(requirements_content)
        self.created_files.append(str(requirements))
        print(f"✅ Created: {requirements}")
        
#         # README.md
#         readme = self.root_dir / "README.md"
#         readme_content = """# Legal Tax Domain-Specific LLM
        
#         ## Project Overview
#         # Building a domain-specific Small Language Model for legal advice in the Nigerian Tax domain.
#         # 
#         ### Project Timeline

# ### Day 1: Extraction (Completed: 2026-01-18)
# - PDF inspection and validation
# - Text extraction (PyMuPDF, pdfplumber, OCR)
# - Metadata creation

# ### Day 2: Data Cleaning (Scheduled)
# - Text normalization
# - Noise removal
# - Data validation

# ### Day 3: Structure Extraction (Scheduled)
# - Section/chapter identification
# - Legal entity extraction
# - Relationship mapping

# ### Day 4: Data Chunking (Scheduled)
# - Semantic chunking
# - Context building
# - Dataset preparation

# ### Days 5-7: Model Training (Scheduled)
# - Model architecture design
# - Fine-tuning
# - Evaluation

# ## Project Structure
        
if __name__ == "__main__":
    import sys
    print("Setting up project structure...")
    setup = ProjectSetup()
    setup.create_directory_structure()
    setup.create_init_files()
    setup.create_config_files()
    setup.create_initial_files()
    print("Project setup complete!")