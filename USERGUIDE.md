# Navigating and loading

**_<ins>Loading files</ins>_**

You can load 4 types of files: .mib, .dm3, .hdf5 and .npz.  
To do this navigate to the top left of the user interface, under the **File** heading. Then click on which file type you wish to load.  
You can also use the buttons in the main window.  
A file browser will pop up, click on the file you want to load and click **Open**.  
Once all desired files have been opened, click on the **Load** button.

A window will pop up asking you for the down sampling rate for **Diffraction Image** and **Navigation Image**.  
Increasing this value will allow for faster load speeds but lower quality of data to work with.  
Increase or decrease this value by using the up and down buttons to the right of the box which holds the value 2^3.

**_<ins>Navigating tabs</ins>_**

Tabs are produced through the usage of the functions, you will automatically be brought to a new tab screen within the interface upon using one of the functions.

If you wish to return to the home screen either navigate to the **Home** tab in the top left. If you wish for the calculation (if there is one) to remain but you want the tab to be removed, either click the red cross on the tab or click the **OK** button.

If you wish to navigate through the tabs the left and right arrow keys can be used.

**_<ins>Workflow help</ins>_**

The workflow help section is used to help the user.  
It will notify you when a certain step has been taken. For example, **MIB file loaded correctly** or **Circular center has now been initalized**.

This can be useful for functions which require other functions to have been run beforehand. You can see at any time what has been done.

# Functions

**_<ins>Data Browser</ins>_**

To use Data Browser, look for the **Data Browser** button underneath the **Functions** heading in the top right of the user interface.  
Click this button and the Data Browser tab will open.  
The Navigation image will be on the left and the Diffraction image on the right.

To navigate through the Diffraction image, click on the desired position in the Navigation image, and the Diffraction image will update appropriately.

If you wish to accumulate a larger area of pixels, instead of just 1*1, you can click the up buttons to the right of **XSize** and **YSize** located above the navigation image.

If you wish to change the colour map of the Diffraction image, there is a drop down menu above the image with different colour maps. Simply click on one of your choice and the image will update automatically.

**_<ins>Circular Center</ins>_**

To use the **Find Circular Center** function, navigate to the **Find Circular Center button** under the **functions** heading, and click on it.  
This will bring up a form with all of the available parameters, change them to your liking. The parameters will save for future use and if you want it to return to the default values, click **Restore defaults**. Once you are happy with your input parameters click **OK** and the circular center tab will pop up showing the relevant images.

**_<ins>Synthetic Aperture</ins>_**

The **Synthetic Aperture** function works in the exact same way as the **Find Circular Center** function. However, the circular center must be calculated before using **Synthetic Aperture**.

**_<ins>Center of Mass</ins>_**

The **Center of Mass** function requires the **Synthetic Aperture** to have been calculated.

Once clicked, input the specific parameters you want and click **OK**. This will calculate the center of mass based on the previous data and the files provided and generate the statistics in the **Workflow help** section.

**_<ins>Ransac Tools</ins>_**

The **Ransac Tools** function requires **Center of Mass** to have been run before it can output data.

**_<ins>DPC Explorer</ins>_**

**DPC Explorer** will output different data depending on what is run beforehand. Certain parameters will have a different effect on the output.  

A standard work flow would look like this: **Find Circular Center->Synthetic Aperture->Center of Mass->Ransac Tools->DPC Explorer**

**_<ins>Matching Images</ins>_**

**Matching Images** requires only the files to be loaded to run.

**_<ins>Disc Edge Sigma</ins>_**

**Disc Edge Sigma** requires **Matching Images** to have been run.

**_<ins>Make Ref Im</ins>_**

**Make Ref Im** requires **Disc Edge Sigma** to have been run.

**_<ins>Phase Correlation</ins>_**

**Phase Correlation** requires only the files to be loaded to run.  
This function also requires a lot of computational power.  
The software may appear slow while running this function.

**_<ins>Virtual ADF</ins>_**

The **Virtual ADF** function requires only **Find Circular Center** to be run.  
It can also be used when loading an **npz file/configuration.**

**_<ins>Plot VADF</ins>_**

**Plotting VADF** requires **Virtual ADF** to be initialised.

**_<ins>Annular Slice</ins>_**

**Annular Slice** requires **Virtual ADF** to be initialised.

# Live coding

**_<ins>Information</ins>_**

Live coding can be accessed through **Explorer->Live Coding** or using CTRL-I shortcut.  
It consists of an IPython shell that behaves like any other Python shell.  
However it also has access to the application data using **fpd_app**.  
With this you can use this shell as a Jupyter notebook.

**_<ins>Important IPython commands</ins>_**

*   %/save [filename] [startLine]-[endLine]
*   %/load [filename]
*   SHIFT-ENTER to run cell
*   More commands can be found at : [Line magic](https://ipython.readthedocs.io/en/stable/interactive/magics.html)

**_<ins>Important FPD-Explorer commands</ins>_**

The following command allows the user to add a dataset to a specific button and use it within the interface:  
**fpd_app.add_data([location], [name], [data])**  

**[location]** corresponds to the button to add an option to. It can be:

*   data : for adding to fpgn of Data Browser
*   nav: for adding to nav_im of Data Browser
*   circular : for adding to Find Circular Center
*   mass : for adding to Center of Mass
*   ransac : for adding to Ransac Tools
*   dpc : for adding to DPC Explorer
*   matching : for adding to Matching Images
*   edge : for adding to Disc Edge Sigma
*   ref : for adding to Make Ref Im
*   phase : for adding to Phase Correlation
*   vadf : for adding to Virtual ADF

**[name]** corresponds to the name the dataset will show as in the interface  
**[data]** corresponds to the variable name under which the dataset is loaded
