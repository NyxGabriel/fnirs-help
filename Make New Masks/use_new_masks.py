# This script works best if you have a folder of fnirs recorded data ran once through TurboSatori
# with all of the channels active for the localizator analysis 
# Your files should be organized as follows: 
#   folder for the analysis with all channels
    #   inside : folder for each participant 
    #       inside: folders for localizaition session with Loc_EquiSetup in the name
    #               and all other following sessions (only these folders should contain .hdr files)

import os 
import shutil
import optode_info #this is the excel file that contains the distances between your optodes 


def is_integer(value):
    """Check if the given value can be converted to an integer."""
    try:
        int(value)
        return True
    except ValueError:
        return False
    
def is_float(value):
    """Check if the given value can be converted to a float."""
    try:
        float(value)
        return True
    except:
        return False

def get_user_input():
    # Ask for folder path and validate it.
    origin_folder_path = input("Enter the origin folder path: ")
    while not os.path.isdir(origin_folder_path):
        print("Invalid folder path. Please enter a valid path.")
        origin_folder_path = input("Enter the origin folder path: ")

    # Ask for number of participants and validate it.
    num_participants = input("Enter the number of participants: ")
    while not is_integer(num_participants) or int(num_participants) <= 0:
        print("Invalid number for participants. Please enter a positive integer.")
        num_participants = input("Enter the number of participants: ")


    # Ask for number of channels and validate it.
    num_channels = input("Enter the number of channels: ")
    while not is_integer(num_channels) or int(num_channels) <= 0:
        print("Invalid number for channels. Please enter a positive integer.")
        num_channels = input("Enter the number of channels: ")

    # Ask for type of signal.
    signal_type = input("Choose the type of signal (oxy/deoxy): ").lower()
    while signal_type not in ['oxy', 'deoxy']:
        print("Invalid choice. Please choose either 'oxy' or 'deoxy'.")
        signal_type = input("Choose the type of signal (oxy/deoxy): ").lower()

    # Ask for channel selection method and its corresponding value.
    channel_method = input("Choose channels based on: t value, number, or first order (Enter 't', 'number', 'first'): ").lower()
    while channel_method not in ['t', 'number', 'first']:
        print("Invalid choice. Please choose 't', 'number', or 'first'.")
        channel_method = input("Choose channels based on: t value, number, or first order (Enter 't', 'number', 'first'): ").lower()

    if channel_method == 't':
        t_value = input("Enter the desired t value: ")
        while not is_float(t_value):
            print("Invalid t value. Please enter a valid float number.")
            t_value = input("Enter the desired t value: ")
        channel_value = float(t_value)

    elif channel_method == 'number':
        num_value = input("Enter the number of channels desired: ")
        while not is_integer(num_value) or int(num_value) <= 0:
            print("Invalid number of channels. Please enter a positive integer.")
            num_value = input("Enter the number of channels desired: ")
        channel_value = int(num_value)

    elif channel_method == 'first':
        print("Enter the matrix describing the first order channels in the optode_info.py")
    
    return origin_folder_path, int(num_participants), int(num_channels), signal_type, channel_method, channel_value

# Handle all the paths and locations within the file structure and open the correct file 
def copy_folder_with_new_name(origin_path, signal_type, channel_method, channel_value):
    """
    Copies the entire folder from origin_path to a new folder named with the provided parameters.
    """
    # Construct the new folder name based on provided parameters.
    new_name = f"MCPA_{signal_type}_{channel_method}_{channel_value}"
    
    # Ensure that this name does not have invalid characters or spaces.
    new_name = new_name.replace(" ", "_").replace("[", "").replace("]", "").replace(",", "-")

    # Get the directory of the original folder.
    parent_directory = os.path.dirname(origin_path)

    # Form the full path of the new directory.
    new_path = os.path.join(parent_directory, new_name)


    # Check if folder with the new name already exists.
    if os.path.exists(new_path):
        print(f"Folder named {new_name} already exists at the destination path. Exiting without copying.")
        return new_path

    # Use shutil to copy the entire folder.
    shutil.copytree(origin_path, new_path)
    print(f"Copied to {new_path}")
    return new_path

def path_name_subject(path, subject):
	if subject <=9:
		sub_name = 'S0'+str(subject+1)
	else:
		sub_name = 'S'+str(subject+1)
	path = os.path.join(path, sub_name) # + "/"  + sub_name + "_003_Loc_EquiSetup"
	return path

def get_folder_path(directory_path, keyword="Loc"):
    """
    Gets the path of a folder with the given keyword in its name. 
    Searching for localization folder 

    Args:
    - directory_path (str): The path to the directory to search in.
    - keyword (str): The keyword to search for in folder names.

    Returns:
    - str: The path of the first folder matching the keyword.
           Returns None if no match is found.
    """

    # List all folders in the given directory
    all_folders = [d for d in os.listdir(directory_path) if os.path.isdir(os.path.join(directory_path, d))]

    # Find folders with the keyword in their name
    matching_folders = [f for f in all_folders if keyword in f]

    if not matching_folders:
        print(f"No folders with the name containing '{keyword}' were found.")
        return None

    # Return the path of the first matching folder
    return os.path.join(directory_path, matching_folders[0])

def read_glm_results_file(folder_path, keyword="GLMResults"):
    
    """
    Searches for a file with the given keyword in its title inside the specified folder,
    then reads and returns its content as a list.

    Args:
    - folder_path (str): The path to the folder to search in.
    - keyword (str): The keyword to search for in file names.

    Returns:
    - list: A list containing lines of the file content.
            Returns None if no match is found.
    """

    # List all files in the given folder
    all_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Find files with the keyword in their name
    matching_files = [f for f in all_files if keyword in f]

    if not matching_files:
        print(f"No files with the name containing '{keyword}' were found.")
        return None

    # Open and read the first matching file
    with open(os.path.join(folder_path, matching_files[0]), 'r') as file:
        content = file.readlines()

    return content 
#____
# Work with the GLM results

def count_lines_between_occurrences(lst, start_word1, start_word2, end_word):
    """
    Counts the number of lines between the occurrence of a line containing two start words
    and a line containing an end word in a given list of sub-lists. 
    
    In this case it is used to find the beginning and end of the GLM results that are important for the goal of the user
    
    Parameters:
    - lst (list of list of str): The main list containing sub-lists to be searched.
    - start_word1 (str): The first word to look for in a line to determine the starting point.
    - start_word2 (str): The second word to look for in the same line as start_word1 to determine the starting point.
    - end_word (str): The word to look for to determine the ending point.
    
    Returns:
    - count (int): Number of lines between the start and end occurrences.
    - start_line (int): The line number (index) where both start words were found.

    Note:
    The search stops as soon as the end_word is found after the start words. If the end_word
    is not found, the count would represent the lines till the end of the list after the start words.
    """
    
    count = 0
    found_start = False
    start_line=0

    for index, sub_list in enumerate(lst):
        if not found_start:
            if start_word1 in sub_list and start_word2 in sub_list:
                found_start = True
                start_line=index
        elif end_word in sub_list:
            break
        else:
            count += 1

    return count, start_line

def order_glm_by_t_value(input_list, start_line, end_line):
    """
    Sort a segment of an input list by the t-value in descending order. 
    The segment to be sorted is determined by the provided start and end lines.
    
    Parameters:
    - input_list (list): The list containing strings, where each string is expected 
                         to have a t-value as one of its components.
    - start_line (int): The index to start sorting from.
    - end_line (int): The index to stop sorting at.
    
    Returns:
    - list: A segment of the input list sorted by the t-value.
    
    Notes:
    - This function assumes that the t-value is the second element of each 
      space-separated string in the segment. If this is not the case, 
      or if the conversion to float fails, a default value of 0 is used.
    """
    def get_t_value(line):
        parts = line.split()
        try:
            return float(parts[1])
        except (IndexError, ValueError):
            return print("There are no contrast results in the GLMresults file in the localizer. Did you run the localizer with the contrast settings on in TurboSatori?")  # Return a default value if the line doesn't match the expected format

    # Extract the part of the list that needs to be sorted
    segment_to_sort = input_list[start_line:end_line+1]

    # Sort the segment by the t-value
    sorted_segment = sorted(segment_to_sort, key=get_t_value, reverse=True)

    # Return the results with the preceding lines, sorted segment, and succeeding lines
    return sorted_segment 

#_____
# Make the different Masks
def make_mask(sub_data, target, channels_grid):
    """
    Create a binary matrix mask from a given data structure.

    The function takes data from `sub_data`, and for each channel up to the target,
    it extracts x and y coordinates. These coordinates are used to mark positions 
    in a binary matrix (`new_matrix`). Positions that correspond to channels 
    in the data are marked with a 1, all other positions are set to 0.

    Parameters:
    - sub_data (list): A nested list where each item represents data for a channel.
                       The x and y coordinates are assumed to be at specific positions 
                       within the nested structure.
    - target (int): The number of channels to process from `sub_data`.
    - channels_grid (int): The dimensions of the square binary matrix to be returned.

    Returns:
    - list: A 2D binary matrix of size [channels_grid x channels_grid].
            Positions corresponding to channels are set to 1, others are set to 0.

    Notes:
    - This function assumes a specific structure for `sub_data`. 
      It expects each channel data to have x and y coordinates at 
      positions [0][1] and [0][4], respectively.
    """
    new_matrix = [[0]*channels_grid for _ in range(channels_grid)]
    x = []
    y = []
    for channel in range(target):
        #print("counting")
        x.append(int(sub_data[channel][0][1]))
        y.append(int(sub_data[channel][0][4]))
        #print('x', sub_data[sub][typ][channel][0][1], 'y',sub_data[sub][typ][channel][0][4])
        #print(new_matrix)
    for coor in range (len(x)):
        new_x = x[coor] - 1 
        new_y = y[coor] - 1 
        new_matrix[new_x][new_y] = 1

    return new_matrix

def update_file(filename, nested_list, new_line):
     # define the sequences to look for in the file
    sequence_x = "S-D-Mask="
    sequence_y = "[ChannelsDistance]"
    # initialize a list to store the new lines of the file
    new_lines = []
    # flags to indicate if we are currently inserting the nested list or the new line
    insert_nested_list = False
    insert= False
    
    # try to open the file and read it line by line
    try:
        with open(filename, 'r') as file:
            for line in file:
                # if we find the first sequence, we start inserting the nested list
                if sequence_x in line:
                    # Insert the nested list with desired formatting
                    insert_nested_list = True
                     # format the nested list as lines of tab-separated values
                    nested_list_lines = ['\t'.join(map(str, sub_list)) + '\n' for sub_list in nested_list]
                    # add the formatted nested list to the new lines
                    new_lines.extend('S-D-Mask="#'+'\n')
                    new_lines.extend(nested_list_lines)
                    new_lines.extend('#"'+'\n')
                
                # if we find the second sequence, we start inserting the new line
                elif sequence_y in line:
                    # Modify the next line after finding sequence Y
                    new_lines.append(sequence_y+'\n')
                    new_lines.append(new_line)
                    insert=True
                 # if we are currently inserting the nested list or the new line,
                # we skip the lines from the original file until we reach an empty line
                elif insert_nested_list or insert:
                    # Skip lines until the end of the nested list is reached
                    if line.strip() == '':
                        insert_nested_list = False
                        insert = False
                else:
                    # Keep the line as it is
                    new_lines.append(line)
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        return
    except PermissionError:
        print(f"Permission denied to read the file {filename}.")
        return
    
    try:
        # Write the modified lines back to the file
        with open(filename, 'w') as file:
            file.writelines(new_lines)
    except PermissionError:
        print(f"Permission denied to write the file {filename}.")
            

def get_distances(mask_list, distance_mask):
    """
    This function receives two 2D lists, mask_list and distance_mask, of the same dimensions.
    It creates a string with the values of distance_mask where the corresponding value in mask_list is 1.
    
    :param mask_list: 2D list of integers (0 or 1)
    :param distance_mask: 2D list of distances (floats or integers)
    :return: string of distances separated by tabs
    """

    # Initialize a list to store the values of distance_mask that correspond to a 1 in mask_list
    values = []

    # Iterate over the elements of mask_list
    for i in range(len(mask_list)):
        for j in range(len(mask_list[i])):
            # If the current element of mask_list is 1, 
            # append the corresponding element of distance_mask to the values list
            if int(mask_list[i][j]) == 1:
                value = distance_mask[i][j]
                values.append(str(value))

    # Join the values list into a single string, separated by tabs
    line = '\t'.join(values)
    # Add the prefix 'ChanDis=' to the string
    line = 'ChanDis="' + line + '"'

    return line



# variables that remian the same
control_word = "Contrast" #this is how in the GLM file we distinguish between the start and the end of a single result
results_type = None
glm_data  = []
distance_matrix = optode_info.distances_SD

#main 
origin_path, participants, channels, signal, method, value = get_user_input()

if signal == "oxy":
    results_type = "oxy-Hb"
elif signal == "deoxy":
    results_type = "deoxy-Hb"
    
destination_path = copy_folder_with_new_name(origin_path, signal, method, value)


for sub in range(0,participants):
    
    sub_path = path_name_subject(origin_path,sub)
    
    loc_path = get_folder_path(sub_path)
    
    contrastResults = read_glm_results_file(loc_path)
    
    total_channels,start = count_lines_between_occurrences(contrastResults, control_word, results_type, control_word)
    
    glm_data = order_glm_by_t_value(contrastResults, start+1, start+total_channels-1)
    
    glm_data = [item.split() for item in glm_data]
    
    if method == 'first':
        new_mask = optode_info.first_order
    else:
        if method == 'number': #'t', 'number', 'first'
            target = value
        elif method == 't':
            line_numbers = [i+1 for i, sublist in enumerate(glm_data) if float(sublist[1]) < value]
            line_number = line_numbers[0] if line_numbers else None
            target = line_number-1
        new_mask = make_mask(glm_data, target, channels)



    participant_destination = path_name_subject(destination_path,sub)
    distance = get_distances(new_mask, distance_matrix)

    #goes over all folders for each subject , inside e.g. S01
    for trial_folder in os.listdir(participant_destination):
        folder_path = os.path.join(participant_destination, trial_folder)
        if os.path.isdir(folder_path):
            #goes over all files inside a trial e.g MT(3)_2
            files = os.listdir(folder_path)
            for file_name in files:
                file_path = os.path.join(folder_path, file_name)
                if os.path.isfile(file_path):
                    if file_path.endswith('.hdr'):
                        update_file(os.path.join(participant_destination,trial_folder,file_path), new_mask, distance)
    
    print("Ready with all headers for participant {}".format(sub+1))
        
