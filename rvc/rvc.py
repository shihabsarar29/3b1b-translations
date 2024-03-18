import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = '1'

""" 
Wrapper for MANGIO-RVC Library Inferencing
"""

from rvc.infer import V2V_infer
import os

#NEED TO ADD "is_working_dir: bool" AS ARG
def infer(pth_file: str, input_file: str, output_file: str, feature_index: str, speaker_id: int, transpoition: float, f0_method: str, crepe_hop: int, harvest_median_filter: int, post_sample_rate: int, mix_vol_envelope: float, feature_index_ratio: float, VCP: float) -> str:
    """
    Run RVC inferencing on the input file and save output to the output file (voice to voice conversion). [Online Demo](https://huggingface.co/spaces/lj1995/vocal2guitar)

    Parameters:
        pth_file (str): .pth model name with (in lib/weights).
        input_file (str): The input file to convert. All major audio formats are supported
        output_file (str): The name of the output file (with .wav extension) to be placed in lib/audio-outputs
        feature_index (str): Path to feature .index file.
        speaker_id (int): Which speaker the new audio file should mimic. Majority of .pth files are trained on 1 speaker, such as in 3b1b use case. Default is (0)
        transposition (float): How much to transpose (change the pitch) the audio. Higher values should be used if target's voice is higher pitched than input voice, and lower values should be used if target's voice is lower pitched than input voice. Default is (0.0)
        f0 method (str): Method to use for pitch detection. Options are "pm", "crepe", "crepe-tiny", "mangio-crepe", "mangio-crep-tiny", "rmvpe", or multiple methods. For multiple methods, use the following format: "hybrid[method1+method2+method3]" etc. It's recommended to use whatever model is trained with, for 3b1b this is rmvpe. Default is (rmvpe)
        crepe_hop (int): The hop size for crepe. Only applicable if atleast 1 chosen f0 method is a type of crepe. Default is (160)
        harvest_median_filter (int) (0-7): The median filter radius size for harvest. Only applicable if atleast 1 chosen f0 method harvest. Min 0, max 7, (default) is 3.
        post_sample_rate (int): The resample rate for the output audio.  Default is (0) (meaning nothing will happen).
        mix_vol_envelope (float): The volume envelope of the output audio. Default is (1.0)
        feature_index_ratio (float) (0-1): The ratio of the feature index to use. Default is (1.0)
        VCP (float): Whether to use Voiceless Consonant Preservation (Less Artifact): 0.33 (Smaller number = more protection. 0.50 means Dont Use.) Default is (0.50)
    
    Returns:
        (str): The path to the output file
    """

    # Make list of all args, convert all args to strings
    args = [str(arg) for arg in [pth_file, input_file, output_file, feature_index, speaker_id, transpoition, f0_method, crepe_hop, harvest_median_filter, post_sample_rate, mix_vol_envelope, feature_index_ratio, VCP]]

    # Add False to args to signify no formant shifting
    args.append(False)

    # Run inferencing
    inference_data = V2V_infer(args)

    if os.path.exists(inference_data):
        # Return the path to the output file. Everything went well if a path is returned
        return inference_data
    elif type(inference_data) == tuple:
        # Raise an error if the inference data is not a string. inference_data[0] will contain traceback
        raise ValueError("Error occured while performing inference. Full traceback: " + str(inference_data[0]))
    else:
        # Raise an error if the inference data is not a string or tuple. This is an unidentified error
        raise ValueError("UNIDENTIFIED ERROR occured while performing inference. Full traceback: " + str(inference_data))
    
# EXAMPLE USAGE:
#infer("init-experiment-2.pth", "audios/someguy.mp3", "myTest.mp3", "logs/init-experiment-2/added_IVF4048_Flat_nprobe_1_init-experiment-2_v2.index", 0, -2, "rmvpe", 160, 3, 0, 1, 0.95, 0.33)