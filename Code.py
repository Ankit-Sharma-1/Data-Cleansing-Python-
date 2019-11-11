"""
The data cleansing program identifies errors in the data from events in Commonwealth Games.
It then corrects or marks the tuple of data as CORRUPT before sending to the website.

Extension 2 and 3 have have been implemented.
As per medal rules place 1 must be for gold, 2 must be for silver and 3 must be for bronze.
A tie hasn't been considered as Extension 1 has not been implemented.
So place 1,2 and 3 must have medal if event has any medal.
"""

__author__ = "Ankit Sharma 45155291"


"""Variable Declaration for column length and position"""
#Maximum Character length of columns
NAME_MAX_CHARACTER_LENGTH = 30
COUNTRY_CODE_MAX_CHARACTER_LENGTH = 3 
PLACE_MAX_CHARACTER_LENGTH = 3
SCORE_MAX_CHARACTER_LENGTH = 6
TIME_MAX_CHARACTER_LENGTH = 8
MEDAL_MAX_CHARACTER_LENGTH = 6
OLYMPIC_RECORD_MAX_CHARACTER_LENGTH = 8
WORLD_RECORD_MAX_CHARACTER_LENGTH = 8 
TRACK_RECORD_MAX_CHARACTER_LENGTH = 8 

#Column Position in processed row
EVENT_NAME_POSITION = 0
ATHLETE_FIRST_NAME_POSITION = 1
ATHLETE_SURNAME_POSITION = 2
COUNTRY_CODE_POSITION = 3
PLACE_POSITION = 4
SCORE_POSITION = 5
TIME_POSITION = 6
MEDAL_POSITION = 7
OLYMPIC_RECORD_POSITION = 8
WORLD_RECORD_POSITION = 9 
TRACK_RECORD_POSITION = 10


#Import functions from another python file
from assign1_utilities import get_column, replace_column, truncate_string


def remove_athlete_id(row):
    """Returns a row with first column value in the input removed.

    Parameters:
        row (str): Row to be truncated.
        
    Returns:
        str: Values from second column onwards in input row.

    Preconditions:
        len(row) >= 0.
    """
    return row[row.find(',') + 1:]

def truncate_name_length(row_to_process):   
    """Returns a row  with first three columns truncated to size 30.

    Parameters:
        row_to_process (str): Row whose column values are to be truncated.
        
    Returns:
        str: Row with event and athlete names truncated to size 30.

    Preconditions:
        maximum character length of the columns is specified as constant variable.
        functions get_column, replace_column and truncate_string have been \
        imported from assign1_utilities.
    """
    column_position = 0
    row_length_check = row_to_process
    while column_position < 3:
        value = get_column(row_to_process,column_position)
        if len(value) > NAME_MAX_CHARACTER_LENGTH:
            value = truncate_string(value,NAME_MAX_CHARACTER_LENGTH)
            row_length_check = replace_column(row_length_check, value, column_position)
        column_position += 1
    return(row_length_check)

def check_column_character_length(row_to_process):   
    """Returns a string with value True if the column width exceeds max character.

    Parameters:
        row_to_process (str): Row whose column values are checked for length of characters.
        
    Returns:
        boolean: True if column width exceeds specified max character length, else False.

    Preconditions:
        functions get_column and replace_column have been imported from assign1_utilities.
        column position and column width specified as constant variable.
    """
    column_position = 3
    corrupt = False
    while column_position < 11:
        value = get_column(row_to_process,column_position)
        if column_position == COUNTRY_CODE_POSITION:
            if len(value) > COUNTRY_CODE_MAX_CHARACTER_LENGTH:
                corrupt = True
        if column_position == PLACE_POSITION:
            if len(value) > PLACE_MAX_CHARACTER_LENGTH:
                corrupt = True
        if column_position == SCORE_POSITION:
            if len(value) > SCORE_MAX_CHARACTER_LENGTH:
                corrupt = True
        if column_position == TIME_POSITION:
            if len(value) > TIME_MAX_CHARACTER_LENGTH:
                corrupt = True
        if column_position == MEDAL_POSITION:
            if len(value) > MEDAL_MAX_CHARACTER_LENGTH:
                corrupt = True                       
        if column_position == OLYMPIC_RECORD_POSITION:
            if len(value) > OLYMPIC_RECORD_MAX_CHARACTER_LENGTH:
                corrupt = True
        if column_position == WORLD_RECORD_POSITION:
            if len(value) > WORLD_RECORD_MAX_CHARACTER_LENGTH:
                corrupt = True
        if column_position == TRACK_RECORD_POSITION:
            if len(value[:-1]) > TRACK_RECORD_MAX_CHARACTER_LENGTH:
                corrupt = True
        column_position += 1
    return(corrupt)

def correct_column_format(row_to_process):   
    """Returns a string with row value after making country code and medal uppercase.

    Parameters:
        row_to_process (str): Row whose Country Code and Medal is to be changed.
        
    Returns:
        str: Row with corrected Country Code and Medal values.

    Preconditions:
        functions get_column and replace_column have been imported from assign1_utilities.
        column position specified as constant variable.
    """
    #Make country code capital. Row is already corrupt if it exceeds max character length
    country_code_value = get_column(row_to_process,COUNTRY_CODE_POSITION)
    country_code_corrected = country_code_value
    # If country code only has characters make it uppercase 
    if country_code_value.isalpha() == True:
        country_code_corrected = country_code_value.upper()
    
    #Make Medal capital. Don't change if it had invalid characters
    medal_value = get_column(row_to_process,MEDAL_POSITION)
    medal_corrected = correct_medal_format(medal_value)
    row_to_process = replace_column(row_to_process,country_code_corrected,COUNTRY_CODE_POSITION)
    row_to_process = replace_column(row_to_process,medal_corrected,MEDAL_POSITION)
    return(row_to_process)

def check_column_format(row_to_process,corrupt):   
    """Returns a string with value True if the column data is not as per specified format or \
       row doesn't follow rules checked earlier 

    Parameters:
        row_to_process (str): Row whose columns are checked for character values.
        corrupt (boolean) : status of row.
        
    Returns:
        boolean: corrupt value as input or set as True if column formatting is incorrect.

    Preconditions:
        functions get_column and replace_column have been imported from assign1_utilities
        functions have been defined checking the formatting of names, country code, \
        place and numbers.
        column position specified as constant variable.
        corrupt value is already True if the row doesn't abide with rules checked before.
    """
    column_position = 0
    while column_position < 11:
        value = get_column(row_to_process,column_position)
        if column_position == EVENT_NAME_POSITION \
           or column_position == ATHLETE_FIRST_NAME_POSITION \
           or column_position == ATHLETE_SURNAME_POSITION:
            corrupt = check_name_format(value,corrupt) # Check name formatting
        if column_position == COUNTRY_CODE_POSITION:
            corrupt = check_country_code_format(value,corrupt) # Check for Country Code
        if column_position == PLACE_POSITION:
            corrupt = check_place_format(value,corrupt) # Check for Place
        if column_position == MEDAL_POSITION:
            if value != "Gold":
                if value != "Silver":
                    if value != "Bronze":
                        if value != "":
                            corrupt = True
        if column_position == SCORE_POSITION or column_position == TIME_POSITION \
           or column_position == OLYMPIC_RECORD_POSITION \
           or column_position == WORLD_RECORD_POSITION:
            corrupt = check_number_format(value,corrupt) # Check number formatting
        if column_position == TRACK_RECORD_POSITION:
            last_value = value[:-1]# Remove \n at the end before checking formatting
            corrupt = check_number_format(last_value,corrupt) # Check number formatting
        column_position += 1
    return(corrupt)
            
def check_name_format(value, corrupt):
    """Returns a string with value True if the characters in name is incorrect.

    Parameters:
        value (str): value to be checked.
        corrupt (boolean) : status of row.
        
    Returns:
        boolean: corrupt value as input or set as True if name formatting is incorrect.

    Preconditions:
        corrupt value is already True if the row doesn't abide with rules checked before.
    """
    total_characters = len(value)
    corrupt_after_check = corrupt
    if value == "":
        corrupt_after_check = True
    else:
        index = 0
        while index < total_characters:
            character_value = value[index]
            is_letter = character_value.isalpha() # check if character is a letter
            is_digit = character_value.isdigit() # check if character is a number
            if is_letter == False:
                if is_digit == False:
                    if character_value != " ":
                        if character_value != "-":
                            if character_value != "'":
                                corrupt_after_check = True
                                break
            index += 1
    return(corrupt_after_check)

def check_country_code_format(value, corrupt):
    """Returns a string with value True if value of Country Code is incorrect.

    Parameters:
        value (str): value to be checked.
        corrupt (boolean) : status of row.
        
    Returns:
        boolean: corrupt value as input or set as True if country code formatting is incorrect.

    Preconditions:
        country code is uppercase if it only has characters.
        corrupt is already true if Country code exceeds length of 3 character.
        corrupt value is already True if the row doesn't abide with rules checked before.
    """
    corrupt_after_check = corrupt
    # Check value for being a string of length 3 
    if value.isalpha() == False or len(value) != 3: 
        corrupt_after_check = True
    return(corrupt_after_check)

def check_place_format(value, corrupt):
    """Returns a string with value True if the place data is not as per specified format or \
       row doesn't follow rules checked earlier 

    Parameters:
        value (str): value to be checked.
        corrupt (boolean) : status of row.
        
    Returns:
        boolean: corrupt value as input or set as True if place is not a positive integer \
        nor one of (DNS,DNF,PEN)

    Preconditions:
        corrupt is already true if place exceeds length of 3 character.
        corrupt value is already True if the row doesn't abide with rules checked before.
    """
    corrupt_after_check = corrupt
    if value.isdigit() == False:
        if value != "DNS":
            if value != "DNF":
                if value != "PEN":
                    if value != "":
                        corrupt_after_check = True
    return(corrupt_after_check)

def correct_medal_format(value) :
    """Returns corrected medal format if it gold, silver or bronze.

    Parameters:
        value (str): value to be checked.
        
    Returns:
        str: Gold, Silver, Bronze or input value is returned.

    Preconditions:
        medal may have invalid characters or it may not follow column rules.
    """
    input_value = value.lower()
    if input_value == "gold":
        return("Gold")
    elif input_value == "silver":
        return("Silver")
    elif input_value == "bronze":
        return("Bronze")
    else:
        return(value)

def is_float(s):
    """Returns False if the string input is not an integer.

    Parameters:
        s (str): Input string which is checked for being an integer.
        
    Returns:
        boolean: If string value is integer then True, else False.

    Preconditions:
        input is in string format.
        input value is a float or integer. 
    """
    try:
        float(s)
        return True
    except ValueError:
        pass
    return False

def check_number_format(value, corrupt):
    """Returns a string with value True if the column data is not a number 

    Parameters:
        value (str): value to be checked.
        corrupt (boolean) : status of row.
        
    Returns:
        boolean: corrupt value as input or set as True if value is not a number.

    Preconditions:
        corrupt value is already True if the row doesn't abide with rules checked before.

    """
    corrupt_after_check = corrupt
    if value != "" and is_float(value) == False:
        corrupt_after_check = True
    return(corrupt_after_check)

def check_column_rules(row_to_process,corrupt):   
    """Returns a string with value True if the column data is not as per specified rules or \
       row doesn't follow rules checked earlier 

    Parameters:
        row_to_process (str): Row whose columns are checked for specified rules.
        corrupt (boolean) : status of row.
        
    Returns:
        boolean: corrupt value as input or set as True if column doesn't follow checked rules.

    Preconditions:
        corrupt value is already True if the row doesn't abide with rules checked before.
        functions have been defined checking the rules for place, medal and world record.
    """
    corrupt_after_check = corrupt
    
    #Check if Place is a whole number then either Score or Time should have value
    #Score and Time both should not have a value 
    corrupt_after_check = check_place_column_rules(row_to_process,corrupt_after_check)
    #Check if Medal has a value then Place should have a value
    corrupt_after_check = check_medal_column_rules(row_to_process,corrupt_after_check)
    #Check if World Record is a legal value then it should be equal to Olympic Record
    corrupt_after_check = check_world_record_column_rules(row_to_process,corrupt_after_check)
    
    return(corrupt_after_check)

def check_place_column_rules(row_to_process,corrupt):   
    """Returns a string with value True if place is a whole number and \
       either score or time have value but not both or row doesn't follow rules checked earlier 

    Parameters:
        row_to_process (str): Row whose place value is checked.
        corrupt (boolean) : status of row
        
    Returns:
        boolean: corrupt value as input or set as True if place doesn't follow checked rules

    Preconditions:
        corrupt value is already True if the row doesn't abide with rules checked before.
        functions get_column and replace_column have been imported from assign1_utilities.
        maximum column value and column position have been specified as constant variable.
    """
    corrupt_after_check = corrupt
    
    #If score value and length follow rules it is a legal value
    #score_value_correct is set as True if score is a legal value
    
    score_value = get_column(row_to_process,SCORE_POSITION)
    score_value_check = check_number_format(score_value,corrupt_after_check)
    
    if len(score_value) <=  SCORE_MAX_CHARACTER_LENGTH and len(score_value) > 0:
        score_formatting = True
    else:
        score_formatting = False

    if score_value_check == False and score_formatting == True:
        score_value_correct = True
    else:
        score_value_correct = False

    #If time value and length follow rules it is a legal value
    #time_value_correct is set as True if time is a legal value
        
    time_value = get_column(row_to_process,TIME_POSITION)
    time_value_check = check_number_format(time_value,corrupt_after_check)
    
    if len(time_value) <=  TIME_MAX_CHARACTER_LENGTH and len(time_value) > 0:
        time_formatting = True
    else:
        time_formatting = False

    if time_value_check == False and time_formatting == True:
        time_value_correct = True
    else:
        time_value_correct = False

    #Check if Place is a whole number then either Score or Time should have legal value but not both
    place_value = get_column(row_to_process,PLACE_POSITION)

    if place_value.isdigit() == True and len(place_value) <=  PLACE_MAX_CHARACTER_LENGTH:
        if score_value_correct == True and time_value_correct == True:
            corrupt_after_check = True
        if score_value_correct == False and time_value_correct == False:
            corrupt_after_check = True
        
    return(corrupt_after_check)

def check_medal_column_rules(row_to_process,corrupt):   
    """Returns a string with value True if the medal has a value but place does not or \
       row doesn't follow rules checked earlier 

    Parameters:
        row_to_process (str): Row whose medal value has to be checked.
        corrupt (boolean) : status of row
        
    Returns:
        boolean: corrupt value as input or set as True if medal doesn't follow checked rules

    Preconditions:
        corrupt value is already True if the row doesn't abide with rules checked before.
        functions get_column and replace_column have been imported from assign1_utilities.
        column position specified as constant variable
    """
    corrupt_after_check = corrupt
    
    medal_value = get_column(row_to_process,MEDAL_POSITION)
    
    place_value = get_column(row_to_process,PLACE_POSITION)

    if medal_value == "Gold":
        if place_value != "1":
            corrupt_after_check = True

    if medal_value == "Silver":
        if place_value != "2":
            corrupt_after_check = True

    if medal_value == "Bronze":
        if place_value != "3":
            corrupt_after_check = True
    
    return(corrupt_after_check)

def check_world_record_column_rules(row_to_process,corrupt):
    """Returns a string with value True if World Record is a legal value \
        but not equal to Olympic Record or row doesn't follow rules checked earlier 

    Parameters:
        row_to_process (str): Row whose world record and olympic record value is checked.
        corrupt (boolean) : status of row
        
    Returns:
        boolean: corrupt value as input or set as True if world record doesn't follow checked rules

    Preconditions:
        corrupt value is already True if the row doesn't abide with rules checked before.
        functions get_column and replace_column have been imported from assign1_utilities.
        column position specified as constant variable.
    """
    corrupt_after_check = corrupt
    
    world_record_value = get_column(row_to_process,WORLD_RECORD_POSITION)
    world_record_value_check = check_number_format(world_record_value,corrupt_after_check)
    
    olympic_record_value = get_column(row_to_process,OLYMPIC_RECORD_POSITION)

    if world_record_value_check == False and len(world_record_value) <=  WORLD_RECORD_MAX_CHARACTER_LENGTH and world_record_value != "":
        if world_record_value != olympic_record_value:
            corrupt_after_check = True
        
    return(corrupt_after_check)

def check_valid_rules(row_to_process,corrupt):
    """Returns a string with value True if values are invalid or \
       row doesn't follow rules checked earlier 

    Parameters:
        row_to_process (str): Row whose values are to be validated.
        corrupt (boolean) : status of row
        
    Returns:
        boolean: corrupt value as input or set as True if columns doesn't have valid values

    Preconditions:
        corrupt value is already True if the row doesn't abide with rules checked before.
        functions get_column and replace_column have been imported from assign1_utilities.
        column position specified as constant variable.
    """
    corrupt_after_check = corrupt
    
    """Check for invalid event name"""
    event_name_value = get_column(row_to_process,EVENT_NAME_POSITION)
    is_event_name_valid = False
    
    # For the event name matches with any valid name in file it is valid
    with open("event_names.csv","r") as valid_event_name_file:
        for row in valid_event_name_file:
            valid_event_name = row[:-1]# Remove /n
            valid_event_name = truncate_string(valid_event_name,NAME_MAX_CHARACTER_LENGTH)
            if valid_event_name == event_name_value:
                is_event_name_valid = True
                
    if is_event_name_valid == False:
        corrupt_after_check = True

    """Check for invalid country code"""
    country_code_value = get_column(row_to_process,COUNTRY_CODE_POSITION)
    is_country_code_valid = False
    
    # If the country code matches with any valid name in file it is valid
    with open("country_codes.csv","r") as valid_country_code_file:
        for row in valid_country_code_file:
            valid_country_code = row[:-1] # Remove /n
            if valid_country_code == country_code_value:
                is_country_code_valid = True
                
    if is_country_code_valid == False:
        corrupt_after_check = True

    """Check for invalid athlete name"""
    athlete_first_name_value = get_column(row_to_process,ATHLETE_FIRST_NAME_POSITION)
    athlete_surname_value = get_column(row_to_process,ATHLETE_SURNAME_POSITION)
    
    is_athlete_name_valid = False

    # If the event name matches with any valid name in file it is valid
    with open("athlete_names.csv","r") as valid_athlete_names_file:
        for row in valid_athlete_names_file:
            valid_athlete_first_name = get_column(row,0)
            valid_athlete_surname = get_column(row,1)
            valid_athlete_surname = valid_athlete_surname[:-1] # Remove /n
            valid_athlete_first_name = truncate_string(valid_athlete_first_name,NAME_MAX_CHARACTER_LENGTH)
            valid_athlete_surname = truncate_string(valid_athlete_surname,NAME_MAX_CHARACTER_LENGTH)
            if valid_athlete_first_name == athlete_first_name_value \
               and valid_athlete_surname == athlete_surname_value:
                is_athlete_name_valid = True
                
    if is_athlete_name_valid == False:
        corrupt_after_check = True

    # Return input corrupt value or set corrupt value as True if names are invalid   
    return(corrupt_after_check)

def check_three_medal_rule(row_to_process,corrupt):
    """Returns a string with value True if row doesn't have valid medal value or \
       row doesn't follow rules checked earlier 

    Parameters:
        row_to_process (str): Row on which three medal rule is to be checked.
        corrupt (boolean) : status of row
        
    Returns:
        boolean: corrupt value as input or set as True if row should have medal value but doesn't

    Preconditions:
        corrupt value is already True if the row doesn't abide with rules checked before.
        functions get_column and replace_column have been imported from assign1_utilities.
        column position specified as constant variable.
    """
    corrupt_after_check = corrupt
    event_name = get_column(row_to_process,EVENT_NAME_POSITION)
    place = get_column(row_to_process,PLACE_POSITION)
    medal = get_column(row_to_process,MEDAL_POSITION)
    
    # Check is event has medal in any instance
    event_has_medal = check_event_medal(event_name)

    three_medal_check = False

    # If event has medal, places 1,2 and 3 must have medal and rest shouldn't
    if event_has_medal == True:
        if place == "1" or place == "2" or place == "3":
            if medal != "":
                three_medal_check = True
        if place != "1" and place != "2" and place != "3":
            if medal == "":
                three_medal_check = True
    if event_has_medal == False:
        three_medal_check = True
        
    if three_medal_check == False:
        corrupt_after_check = True
        
    # Return input corrupt value or set corrupt value as True if row should have a medal 
    return(corrupt_after_check)

def check_event_medal(event_name):
    """Returns a string with value True if event has at least one medal in dataset.

    Parameters:
        event_name (str): Event which is checked for having medal.
        
    Returns:
        boolean: event_has_medal as True if the event has medal in any of the record else False

    Preconditions:
        functions get_column and replace_column have been imported from assign1_utilities.
    """
    # Open raw file and check if the event has medal in any instance
    event_has_medal = False
    with open("athlete_data.csv", "r") as raw_data_file2 :
        for row in raw_data_file2 :
            event_name_raw_data = get_column(row,1)
            if event_name == event_name_raw_data:
                medal_raw_data = get_column(row,8)
                if medal_raw_data != "":
                    event_has_medal = True          
        
    # Return True if event has medal for at least one occurance 
    return(event_has_medal)


def main() :
    """Main functionality of program."""
    with open("athlete_data.csv", "r") as raw_data_file, \
         open("athlete_data_clean.csv", "w") as clean_data_file :
        for row in raw_data_file :
            corrupt = False
            row = remove_athlete_id(row)
            row_to_process = row    # Saves row in original state, minus athlete id.
            # Truncate event name, athelete's first name and athelete's surname
            row_to_process = truncate_name_length(row_to_process)
            
            """ On violation of formatting and rules set corrupt as True"""
            # Check max character length of values.
            corrupt = check_column_character_length(row_to_process)
            # Correct country code and medal format of columns
            row_to_process = correct_column_format(row_to_process)
            # Check format of other columns.
            corrupt = check_column_format(row_to_process,corrupt)
            # Check rules of all columns data.
            corrupt = check_column_rules(row_to_process,corrupt)
            # Check for valid country code, event names and athlete names
            corrupt = check_valid_rules(row_to_process,corrupt)
            # Check that three medals are awarded for every event
            corrupt = check_three_medal_rule(row_to_process,corrupt)

            

            # Save the row data to the cleaned data file.
            if not corrupt :
                clean_data_file.write(row_to_process)
            else :
                row = row[:-1]      # Remove new line character at end of row.
                clean_data_file.write(row + ",CORRUPT\n")    



# Call the main() function if this module is executed
if __name__ == "__main__" :
    main()
