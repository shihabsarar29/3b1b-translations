# Setting Up Conda Environment

This guide assumes you have Conda installed on your system. If you do not have Conda installed, please visit [the official Conda installation guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) for instructions on installing Conda.

## Creating the Environment

Navigate to the directory containing the `conda_requirements.txt` file in your terminal. Then, run the following command to create a new Conda environment:

```bash
conda create --name rvc-env --file conda_requirements.txt
```

## Activating the Environment

```bash
conda activate rvc-env
```

## Run the sync_audio pipeline

1. Move to the root directory of the project
2. Provide the translations_path and music_path in scripts/sync_audio.py
3. Run the script

```bash
python scripts/sync_audio.py
```