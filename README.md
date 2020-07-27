# CPR Tools Inventory Database

This is a program I created for my company, CPR Tools, to manage our extensive lab inventory. One of its key features is the use of "search types" which allow for custom item categories with custom parameters that can be filtered. 


## Installation
A minimum of Python 3.7 is recommended for maximum compatibility.

Use the package manager  [pip](https://pip.pypa.io/en/stable/)  to install this program's dependencies:

```bash
pip install Pandas
pip install PySide2
```
**Note:** If you do not wish to install this program's dependencies or are looking for a portable solution, an all-in-one executable is available from this [link](https://www.mediafire.com/file/3416y89li6pvol2/inventory_database.exe/file)
## Setup
**Creating a new user:**
To start, it is recommended, but not required, to create a named user to replace the default user. This can be done through: 

    Edit -> Users... -> Add...
Once a second user is created, the default user can be deleted, if desired. 

**Note:** At least **one** user entry is required for the program to function.

**Creating a new search type:**
As the program does not have a default search type, it is required to create at least one before you can properly use the program. To do this:

    Edit -> Search Types... -> Add...
1. Start by naming the search type in the Search Type Name field (e.g. "Seagate Hard Drives"). The following characters are prohibited: `&"?<>#{}%~/\`

2. After you have chosen a name, you can either confirm your entry and create a generic search type with no parameters (if so, skip to next section), or you can proceed to create some search parameters. 

3. To define a parameter, enter a name in the Parameter Name field (e.g. "Part Number"). Once you are satisfied with a name, click Add to create the parameter.

4. There is no limit to the amount of parameters one search type can contain. If you wish to delete a parameter, you can select it in the bottom menu and click Delete. If you wish to change the order of your parameters, you can use the on-screen arrow buttons to move a parameter up and down.

5. Once you are done, confirm your entry and continue to the next section!

## Usage
Now that you have successfully set up the program, you can now begin using it! Here are some quick tips to get started:

**Adding items to a search type category:**

 1. To add an item, start by selecting a search type from the drop down menu in the top-right corner.
 
 2. Once you have selected a search type, click the Add.. button on the left side of the window. This will bring up a menu which we will use to fill in the item details.

 3. By default, every search type has name and location parameters. This cannot be changed and they are required entries. The name can be used to quickly find items from the search bar, and the location can be used to track the location of an item in your inventory.

 4. Once you have filled out the name and location fields, if your search type isn't generic, you can then proceed to fill out the item's parameters. 
**Note:** While the name and location parameters are required to proceed, custom parameters are not. If a parameter is left empty, its entry will be replaced with "nan."

 5. When you are finished, select confirm and continue to the next section.

**Editing items in a search type category:**
 1. Editing an item is done the exact same way as adding one. With one minor exception: 
You must search for the item after selecting its search type, and then you must select it in the table below.

 2. Once you have selected an item, select the Edit... button on the left of the window and edit it as needed.
**Note:** You can only edit one item at a time.

**Removing items in a search type category:**

 Removing items is done the exact same way as editing, except you have to select the Remove button.
**Note:** You can remove multiple items at once.

**Searching for an item**
 1. To search for an item, select the desired Search Type from the drop down menu in the top left corner.

 2. Once a Search Type has been selected, you can search for a specific item name by using the search bar and/or by searching parameters via the filters menu, or you can view the full inventory by clicking the Search button.

 11. To filter an item by its parameters, you can use the filter menu. In the filter menu, you can filter parameters by term. Once you have configured your filters, you can close the window and click the search button (your filter entries will be retained by the program).
 **Note:** Though the filters are not case sensitive, if the exact filter search term is not contained within the item's parameter entry, the item will not show up.

**Checking items in and out:**

Listed items can be checked in and out by a user. To do so, you can select an item (or multiple items) from the inventory table and click Check In or Check Out from the left side of the window.
