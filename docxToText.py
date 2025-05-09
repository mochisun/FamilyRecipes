import os
import docx

### class ####

#class to hold all recipe contents
class Recipe:
    def __init__(self, title='', ingredients=None, instructions=None):
        self.title = title
        self.ingredients = ingredients or []
        self.instructions = instructions or []
    #override str function
    def __str__(self):
        str = "Title: " + self.title + "\nIngredients: " 
        for i in self.ingredients:
            str += "\n- " + i
        str += "\nInstructions: "
        for i in self.instructions:
            str += "\n" + i
        return str
            

### functions ####

#function to recursively get all files in a directory
def list_files_recursive(path='.'):
    #create new path list
    file_paths = []
    #walk through dir
    for dirpath, _, filenames in os.walk(path):
        for file in filenames:
            #append new list
            file_paths.append(os.path.join(dirpath, file))
    return file_paths

def extract_word(lines, recipe):
    #iterator
    i = 0
    #these 2 boolean variables will be used to figure out when the 
    # .docx lines should be getting read into the object fields
    ingredient_bool = False
    instruction_bool = False

    #iterate through each line
    while i < len(lines):
        #get the text from each line
        text = lines[i].text
        #set the initial line into title
        if i == 0:
            recipe.title = text
        
        #check/mark if we are stepping into ingredients
        if text.find("Ingredients") == 0:
            ingredient_bool = True
            i += 1
            continue
        #check/mark if we are stepping into instructions (unmark ingredient bool)
        if text.find("Instructions") == 0:
            ingredient_bool = False
            instruction_bool = True
            i += 1
            continue

        #read in the ingredients
        if ingredient_bool:
            recipe.ingredients.append(text)

        #read in the directions
        if instruction_bool:
            recipe.instructions.append(text)

        i += 1

### main ###
if __name__ == "__main__":
    #recipeDir = input("Please enter the name of the new recipe directory: ")
    recipeDir = list_files_recursive('melinda_recipes_docx_files/')

    #create list of recipe objects
    recipes = []
    for file in recipeDir:
        #create single object instance
        recipe = Recipe()
        if file.find("Guac") > 0:
            word_doc = file
            #get contents of file with import docx
            contents = docx.Document(word_doc)
            #get all lines (paragraphs)
            lines = contents.paragraphs
            #extract the word document into recipe object
            extract_word(lines, recipe)
            print(recipe)
            #add the recipe to the list of recipes
            recipes.append(recipe)

            
