<a name="readme-top"></a>


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
    <a href="docs/"><strong>Explore the docs »</strong></a>
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

<!---
Project Shields
-->
[![VSCode][vscode-shield]][vscode-url]

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
A common use case involves converting text to speech using the [ElevenLabsWrapper](docs/ElevenLabsWrapper.md), and making this speech more realistic using an [RVC Model](docs/RVCWrapper.md). To create these realistic audios, make a new _IPYNB_ or _PY_ file in the project's root directory.
```Python
from scripts.ElevenLabsAPI.elevenLabsAPI import elevenLabsAPI
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
elevenLabs.TTS_to_file("TTS_OUTPUT.mp3", text)

# Infer the RVC Model, save the output to TTS_OUTPUT.mp3
infer("sample_rvc.pth", "TTS_OUTPUT.mp3", "SAMPLE.mp3", "logs/sample_rvc/rvc_idx.index", 0, -2, "rmvpe", 160, 3, 0, 1, 0.95, 0.33)
```

_For more information and code examples, please refer to the [Documentation](docs/). The documentation was last updated 2/24/2024._

<!-- ROADMAP -->

## Roadmap (as of 2/28)

- [x] TTS Testing
- [x] ElevenLabs TTS
  - [x] Preprocessing
  - [x] ElevenLabs Model Development
  - [x] Wrapper
- [ ] Azure TTS
  - [ ] Data Collection
  - [ ] Training
  - [x] Code Implementation 
- [ ] RVC
  - [x] RVC Wrapper
  - [x] Data Preprocessing
  - [x] Training
  - [x] Individual Testing
  - [ ] Integration + Testing over ElevenLabs TTS
- [x] Translated Speech Time Estimations
  - [x] Collecting Character Averages
  - [x] Code Implementation
  - [ ] Adding Constants
- [x] GPT Adjustments
  - [x] Prompt Engineering
  - [x] Code Implementation
- [x] Aligning Translated Audio w/ Original Audio
  - [x] Pause Audios
  - [x] Speedups
  - [x] GPT Adjustments
- [ ] ElevenLabs Fully Automated Pipeline
  - [ ] Validating Translations
    - [ ] GPT Adjustments Integration
  - [ ] Code Implementation
    - [ ] RVC Integration
    - [ ] Audio Synchronization Integration

<!-- Shields and URLs -->
[vscode-shield]: https://img.shields.io/badge/Open%20in%20VS%20Code-open-blue.svg?logo=visual-studio-code
[vscode-url]: https://github.dev/shihabsarar29/3b1b-translations
