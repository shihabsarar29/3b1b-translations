# Calculate File Documentation

## Overview
Calculate the average number of characters per line and per second in the translated text for each language.

## Attributes
- `ROOT_DIR`: **str**
    - The root directory of the folder containing the files you want to calculate the average characters per line and per second for.
- `character_counts`: **dict**
    - `total`: **int**
        - Total number of characters in the translated transcript
    - `avg_per_line` **float**
        - Average number of characters per line in the translated transcript
    - `avg_translated` **float**
        - Average number of characters per second in the translated audio
    - `avg_translated_sync` **float**
        - Average number of characters per second in synced translated Azure audio
- `character_count_detailed`: **dict**
  - `start`: **float**
      - The start time of the line
  - `end`: **float**
      - The end time of the line
  - `character_count`: **int**
      - The number of characters in the line

## Output
- `character_counts.json`:
    - A JSON file containing the character_counts dictionary. A JSON file is saved for every language the video was translated to into the respective folder.
- `character_count_detailed.json`:
    - A JSON file containing the character_count_detailed dictionary. A JSON file is saved for every language the video was translated to into the respective folder.