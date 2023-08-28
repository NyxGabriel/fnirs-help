# Scripts to make new masks 
This software allows you to create mew masks to use in TurboSatori and Satori analysis for which channels you want to look at. It takes the real optode distances if you have those, get them, why bother if you are not even including what is really happening? 

## Making Masks and updating hdr files for TS
The use_new_masks.py script allows the user to give a directory of TS data and the script will create a new folder with this data but with different masks, as specified by the user.

**Input**:
    Path to the already existing data (this will preferably be data ran through TurboSatori with all channels and should have contrast GLM as well)
    Number of participants (just so that there could be other folders inside the analysis such as settings etc)
    Number of channels - so the size of the recording matrix (currently the number of sources and detectors should be the same)
    Type of information - oxygenated or deoxygenated blood information 
    Then specify what masks you want:   
        Based on the first order channels - 
        Based on a number of channels you want to use, they are ordered by t-value so the number of channels with the "best" t-values will be picked
        Based on a specific t-value - if you want channels that have more than a given t-value to be included 

**Output**
    A folder with the name MCPA_type_masktype_numberused and inside the same structure as the original 
    All of the .hdr files inside are updated with new mask information and new channel distance information. 

## Making masks - Find_Best_Channels
This script looks at already ran localization data through a GLM, and based on that creates a list of different masks. Maybe you want them to only include the best channel for each participant, or the 10 best channels, or all channels with T-values over some threshold. 
**IN:** GLM results from Localization session
**OUT:** txt file with a list of the masks you want for each participant

#### User parameters: 
1. number of participants to look at
2. masks based on type of info: oxygenated blood or deoxygenated blood
3. Number of channels desired, threshold values if using that, first order channels
