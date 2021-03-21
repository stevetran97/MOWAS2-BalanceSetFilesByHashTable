Can be used to translate large ordered hash tables of MP MOW:AS2 vehicle properties TO numerous faction vehicle roster set files.

## Use
  - Place all of the txt/set files that you want to edit in the FilestoEdit Folder
  - Create a hash table (manually or algorithmically) of the vehicle names (under a vehicle class) and the property you want it to be updated with (See default structure)
  - Running the code (updateUnits.py) will loop through all files in the FilestoEdit folder and update each vehicle entry with the new properties
    - By default, the editted property is the cost of the vehicle
      - To change the editted property, one must edit both the 'replacementPattern' and 'newProp' formats

## Usecases
  - To distribute new properties to multiple formatted text files from an easy-to-store/edit hash table

## Algorithm
  - Loops through each set (equivalent to txt) file in the Editting Folder
  - Looping through the file will return each line in a string format
  - The Algorithm check if first string key in the line is == to the commentTrigger set in main.py
  - The Algorithm uses the comment trigger to select the vehicle class from the main hash table of replacement values
    - The current vehicle class state is stored in the classProps variable if found. It is none if no class is found.
  - The Algorithm continues looping through the following lines but now calls a callback to check old properties and replace them on these lines
    - Callback: 
      - Finds the vehicle name on the current line
      - Finds the vehicle name in the sub vehicle class hash table
      - If found, replace the old pattern in text with the new formatted pattern as per the hash table
      - If no vehicle name found, write the line as is 
    - This behaviour is reset when this inner-most loop runs into another comment which either: finds a new state or sets the state to None

## Current Intrinsic Issues
  - Poor flexibility: Must format vehicle property hash table in exactly 2 layers (Vehicle Class then Vehicle)
