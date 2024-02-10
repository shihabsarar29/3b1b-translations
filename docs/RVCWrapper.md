# MANGIO-RVC Library Inferencing Wrapper

This module serves as a wrapper for running inferencing using the MANGIO-RVC library. It provides a convenient interface for converting voice inputs to modified outputs, such as voice-to-voice conversion. The underlying functionality utilizes the `V2V_infer` function from the `lib.infer` module. The models this class utilizes are trained using the [Mangio-RVC](https://github.com/Mangio621/Mangio-RVC-Fork) fork, which provides a web interface and CLI for training RVC-based models. Other RVC-based models may be used as well.

## The `infer` Function

### Description:
Runs RVC (Residual Voice Conversion) inferencing on the input audio file and saves the converted output to a specified location. This function is particularly useful for voice-to-voice conversion tasks.

### Parameters:
- `pth_file` **str**: 
  - The name of the .pth model file located in the `lib/weights` directory.
- `input_file` **str**: 
  - The path to the input audio file to be converted. Supports all major audio formats.
- `output_file` **str**: 
  - The name of the output file (with .wav extension) where the converted audio will be saved. It will be placed in the `lib/audio-outputs` directory.
- `feature_index` **str**: 
  - Path to the feature .index file required for inferencing.
- `speaker_id` **int** (default: 0): 
  - The ID of the speaker the output audio should mimic. Defaults to 0.
- `transposition` **float** (default: 0.0**): 
  - The degree of pitch transposition applied to the audio. Positive values increase pitch, while negative values decrease pitch.
- `f0_method` **str** (default: "rmvpe"): 
  - The method used for pitch detection. Options include "**pm**", "**crepe**", "**crepe-tiny**", "**mangio-crepe**", "**mangio-crep-tiny**", "**rmvpe**", or combinations thereof (e.g., "**hybrid[method1+method2+method3]**"). Advantages and disadvantes of each method are listed below. It's recommended to use the method corresponding to the model's training. 
    - "**pm**": faster extraction but lower-quality speech; 
    - "**harvest**": better bass but extremely slow; 
    - "**crepe**": better quality but GPU intensive. 
- `crepe_hop` **int** (default: 160): 
  - The hop size for crepe pitch detection.
- `harvest_median_filter` **int** (range: 0-7, default: 3**): 
  - The radius size of the median filter for harvest pitch detection.
- `post_sample_rate` **int** (default: 0): 
  - The resampling rate for the output audio. Set to 0 for no resampling.
- `mix_vol_envelope` **float** (default: 1.0): 
  - The volume envelope of the output audio.
- `feature_index_ratio` **float** (range: 0-1, default: 1.0): 
  - The ratio of the feature index to use.
- `VCP` **float** (default: 0.50): 
  - Voiceless Consonant Preservation factor. Lower values provide more protection against artifacts.

### Returns:
- `str`: The path to the output file containing the converted audio.

### Exceptions:
- `ValueError`: 
  - Raised when an error occurs during inferencing. Provides a traceback if available.

### Example Usage:
```python
output_path = infer(
    pth_file="init-experiment-2.pth", # The model file at lib/weights/init-experiment-2.pth will be used
    input_file="audios/someguy.mp3", # audios/someguy.mp3 will be used as the input file
    output_file="myTest.mp3", # The converted audio will be saved as myTest.mp3
    feature_index="logs/init-experiment-2/added_IVF4048_Flat_nprobe_1_init-experiment-2_v2.index", # The feature index file
    speaker_id=0, # The output audio will mimic the first (and often only) speaker
    transposition=-2, # The output audio will be transposed down by 2 semitones, resulting in a lower pitch
    f0_method="rmvpe", # The RMVPE method will be used for pitch detection
    crepe_hop=160, # The hop size for crepe pitch detection
    harvest_median_filter=3, # The radius size of the median filter for harvest pitch detection
    post_sample_rate=0, # The output audio will not be resampled
    mix_vol_envelope=1, # The volume envelope of the output audio
    feature_index_ratio=0.95, # 95% of the feature index will be used
    VCP=0.33 # Voiceless Consonant Preservation factor
)
```