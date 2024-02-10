<a name="readme-top"></a>

<!---
Project Shields
-->
[![Contributors][contributors-shield]][contributors-url]
[![VSCode][vscode-shield]][vscode-url]

<!-- PROJECT LOGO -->

<div align="center">
  <a href="https://github.com/shihabsarar29/3b1b-translations/">
    <img src="docs/images/logo.png" alt="Logo" width="80" height="80">
  </a>

<h3 align="center">3Blue1Brown Translation Project</h3>

<p align="center">
    AI-Powered Translations for 3Blue1Brown's Youtube Channel<br>  <strong>20+ supported languages</strong> 
    <br />
    <br>
    <a href="https://github.com/github_username/repo_name"><strong>Explore the docs »</strong></a>
  </p>
</div>

<!-- TABLE OF CONTENTS -->

<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#example-usage">Example Usage</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT 
## About The Project

[![Product Name Screen Shot][product-screenshot]](https://example.com)

Here's a blank template to get started: To avoid retyping too much info. Do a search and replace with your text editor for the following: `github_username`, `repo_name`, `twitter_handle`, `linkedin_username`, `email_client`, `email`, `project_title`, `project_description`

<p align="right">(<a href="#readme-top">back to top</a>)</p>-->

<!-- GETTING STARTED -->

## <a name="started"></a>Getting Started

### Prerequisites

Ensure you have the following installed before moving onto installation.

#### Necessities

* Python (tested with 3.9.17)
  ```sh
  python --version
  ```

#### Recommendations

* Anaconda Package Manager
  ```sh
  conda update conda
  conda update anaconda
  ```
* Capable NVIDIA GPU (For Faster Inference)
  ```sh
  nvidia-smi
  ```

### Installation

1. Get a free API Key at [https://https://elevenlabs.io/](https://elevenlabs.io/)
2. Clone the repo
   ```sh
   git clone https://github.com/shihabsarar29/3b1b-translations.git
   ```
3. Install Necessary Packages
- Anaconda
  ```sh
  conda install --yes --file conda_requirements.txt
  ```
- Pip
  ```sh
  pip install -r requirements.txt
  ```
4. Enter your API key in **./.env**
   ```console
   ELEVEN_LABS_API_KEY = <API_KEY_HERE>
   ```

### Example Usage
A common use case involves converting text to speech using the [ElevenLabsWrapper](https://example.com/documentation/ElevenLabsWrapper), and making this speech more realistic using an [RVC Model](https://example.com/documentation/RVC). To create these realistic audios, make a new _IPYNB_ or _PY_ file in the project's root directory.
```Python
from scripts.ElevenLabsAPI.elevenLabsAPI.py import elevenLabsAPI
from scripts.RVCAPI.RVCAPI import infer
import dotenv

# Load API_KEY from environment file
dotenv.load_dotenv()
API_KEY = os.getenv('ELEVEN_LABS_API_KEY')

# Initialize API Wrapper
elevenLabs = elevenLabsAPI(API_KEY)

# Get the voice_id for the custom model
elevenLabs.get_voice_id('3b1b', inPlace=True)

# Get the text to be converted
text = "Hello, World!"

# Convert the text to speech
elevenLabs.TTS_to_file("TTS_OUTPUT.mp3", text, voice_id='3b1b')

# Infer the RVC Model, save the output to TTS_OUTPUT.mp3
infer("sample_rvc.pth", "TTS_OUTPUT.mp3", "SAMPLE.mp3", "logs/sample_rvc/rvc_idx.index", 0, -2, "rmvpe", 160, 3, 0, 1, 0.95, 0.33)
```

_For more information and code examples, please refer to the [Documentation](https://example.com)_

<!-- ROADMAP -->

## Roadmap

- [x] ElevenLabs TTS Wrapper
  - [x] Preprocessing
  - [x] ElevenLabs Model Development
  - [x] Wrapper
- [ ] RVC
  - [x] RVC Wrapper
  - [x] Data Preprocessing
  - [ ] Training
- [ ] Automation
  - [x] Audio Alignments
  - [ ] ElevenLabs RVC Integration
  - [ ] Testing

<!-- Shields and URLs -->
[contributors-shield]: https://img.shields.io/github/contributors/shihabsarar29/3b1b-translations.svg?style=for-the-badge
[contributors-url]: https://github.com/shihabsarar29/3b1b-translations/graphs/contributors
[vscode-shield]: https://img.shields.io/badge/Open%20in%20VS%20Code-open-blue.svg?logo=visual-studio-code
[vscode-url]: https://github.dev/shihabsarar29/3b1b-translations
