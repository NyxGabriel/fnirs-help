# Scripts to make new masks 
This software allows you to create mew masks to use in TurboSatori and Satori analysis for which channels you want to look at. It takes the real optode distances if you have those, get them, why bother if you are not even including what is really happening? 

## Making Masks and updating hdr files for TS
The use_new_masks.py script allows the user to give a directory of TS data and the script will create a new folder with this data but with different masks, as specified by the user.

**Input**:
    - Path to the already existing data (this will preferably be data ran through TurboSatori with all channels and should have contrast GLM as well)\
    - Number of participants (just so that there could be other folders inside the analysis such as settings etc)\
    - Number of channels - so the size of the recording matrix (currently the number of sources and detectors should be the same)\
    - Type of information - oxygenated or deoxygenated blood information \
    - Then specify what masks you want:   \
        - Based on the first-order channels - input in optode_info file \
        - Based on the number of channels you want to use, they are ordered by t-value so the number of channels with the "best" t-values will be picked \
        - Based on a specific t-value - if you want channels that have more than a given t-value to be included \

**Output**
    A folder with the name MCPA_type_masktype_numberused and inside the same structure as the original \
    All of the .hdr files inside are updated with new mask information and new channel distance information. \


