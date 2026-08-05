# AI Research Workflow Specification

## 1. Purpose & Objective
Guide scientific exploration, literature synthesis, hypothesis formulation, model prototyping, and empirical evaluation.

## 2. Prerequisites & Trigger Conditions
- **Prerequisites**: Research problem statement, compute resource allocation (GPU cluster), benchmark datasets.
- **Trigger Conditions**: Initiation of AI research initiative or algorithm optimization grant.

## 3. Participating Agent Roles & Responsibilities
- **AI Research Lead**: Formulates hypotheses, defines metrics, and oversees experimental methodology.
- **Data Scientist**: Preprocesses datasets, runs statistical analyses, and engineers features.
- **ML Research Engineer**: Implements model architectures in PyTorch/JAX, trains baseline models, and logs experiments.

## 4. Step-by-Step Execution Sequence

### Step 1: Literature Review & State of the Art (SOTA) Analysis
- **Inputs**: Research topic query, academic databases (ArXiv, PapersWithCode).
- **Actions**: Aggregate SOTA publications, compare architectural approaches, identify research gaps.
- **Outputs**: Literature Review & Benchmark Survey synthesis document.
- **Verification**: AI Research Lead approval of research hypothesis.

### Step 2: Experimental Setup & Dataset Curation
- **Inputs**: Raw datasets, compute environment (PyTorch, CUDA, WandB).
- **Actions**: Clean raw data, create reproducible train/val/test splits, verify label distribution, configure dataset loaders.
- **Outputs**: Standardized dataset splits and data pipeline scripts.
- **Verification**: Dataset validation check confirming no data leakage across splits.

### Step 3: Model Architecture Prototyping
- **Inputs**: Dataset loaders, model design hypotheses.
- **Actions**: Write modular PyTorch/JAX model components, construct loss functions, write training loops with mixed-precision support.
- **Outputs**: Model codebase and modular component unit tests.
- **Verification**: Forward-pass sanity check with dummy input tensor passing without dimension mismatches.

### Step 4: Experimental Execution & Hyperparameter Tracking
- **Inputs**: Model codebase, WandB / MLflow tracking, GPU cluster.
- **Actions**: Execute training sweeps across hyperparameter grids; track loss curves, accuracy, latency, and memory utilization.
- **Outputs**: Experiment logs, checkpoint weights, and WandB runs dashboard.
- **Verification**: Validation metric convergence without gradient explosion or vanishing.

### Step 5: Results Synthesis & Paper Drafting
- **Inputs**: WandB experiment runs, evaluation metrics, visual charts.
- **Actions**: Compile ablation study tables, draft methodology section, write comparative evaluation vs SOTA baselines.
- **Outputs**: Comprehensive Research Paper draft (LaTeX format) and model weights repository.
- **Verification**: Internal peer review approval from AI Research Lead.

## 5. Decision Gates & Branching Rules
- Gate 1: Dataset split verification must confirm zero data contamination before training run.
- Gate 2: Model ablation study must demonstrate statistically significant improvement over SOTA baseline (p < 0.05).

## 6. Failure Modes & Fallback/Recovery Procedures
- Failure Mode 1: Model gradient explosion during deep training -> Action: Implement gradient clipping, adjust learning rate scheduler, inspect norm distributions.
- Failure Mode 2: Overfitting on validation set -> Action: Add data augmentation, increase regularization (weight decay/dropout), re-run sweep.

## 7. Artifact Delivery & Output Standard
Compiled LaTeX research paper PDF, WandB experiment run logs, verified PyTorch model weights (.pt), and reproducible benchmark script.
