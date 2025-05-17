import os
import json
import docx

### class ####

#class to hold all recipe contents
class Recipe:
    def __init__(self, title='', path='', ingredients=None, instructions=None):
        self.title = title
        self.path = path
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
    #dictionary function for conversion into .json
    def to_dict(self):
        return{
            "title": self.title,
            "ingredients": self.ingredients,
            "instructions": self.instructions, 
            "file_path": self.path
        }
            

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

def extract_word(lines, recipe, file):
    #set the recipe file path 
    recipe.path = file

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

def create_recipes_json(recipes):
    #convert each recipe into a dictionary by using the class function
    recipe_dicts = [recipe.to_dict() for recipe in recipes]

    #open/write to json file
    with open("recipes.json", "w", encoding="utf-8") as f:
        json.dump(recipe_dicts, f, indent=4)


### main ###
if __name__ == "__main__":
    #recipeDir = input("Please enter the name of the new recipe directory: ")
    recipeDir = list_files_recursive('melinda_recipes_docx_files/')

    #create list of recipe objects
    recipes = []
    #extract all .docx files in dir into recipe objects
    for file in recipeDir:
        #create single object instance
        recipe = Recipe()
        #get contents of file with import docx
        contents = docx.Document(file)
        #get all lines (paragraphs)
        lines = contents.paragraphs
        #extract the word document into recipe object
        extract_word(lines, recipe, file)
        #add the recipe to the list of recipes
        recipes.append(recipe)
    
    #now that we have a list of recipe objects, we can turn into .json file
    create_recipes_json(recipes)

            
