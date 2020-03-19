# Navigation/Loading

**<u>Loading files</u>**

You can load 4 types of files .dm3, .mib, .hdf5 and .npz,  
To do this navigate to the top left of the user interface, under the **File** heading. Then click on which file type you wish to load.  
You can also use the buttons in the main window.  
A file browser will pop-up, click on the file you want to load and click **Open**.  
Once all desired files have been opened, click on the **Load** button.

A window will pop up asking you for the down sampling rate for **Diffraction Image** and **Navigation Image**.  
Increasing this value will allow for faster load speeds but lower quality of data to work with.  
Increase or decrease this value by using the up and down buttons to the right of the box which holds the value 2^3.

**<u>Navigating tabs</u>**

Tabs are produced through the usage of the functions, you will automatically be brought to a new tab screen within the GUI upon using one of the functions.

If you wish to return to the home screen either navigate to the **home** tab in the top left, or if you wish for the calculation(if there is one) to remain but you want the tab to be removed, either click the red cross on the tab or click the **OK**.

If you wish to navigate through the tabs the left and right arrow keys can be used.

**<u>Workflow help</u>**

The workflow help subsection is used to help the user.  
It will notify you when a certain step has been taken, for example **MIB file loaded correctly** or **Circular center has now been initalized**.

This can be useful for functions which require other functions to have been run beforehand to use them (you can check to see what you have done/have to do).

# Function Guide

**<u>Data Browser</u>**

To use Data Browser, look for the **DataBrowser** button underneath the **Functions** heading in the top right of the user interface.  
Click this button and the DataBrowser tab will open.  
On the left hand side will be the Navigation image and on the right the Diffraction image.

To navigate through the Diffraction image, click on the desired position on the Navigation image, and the Diffraction image will update appropriately.

If you wish to accumulate a larger area of pixels, instead of just 1*1, you can click the up/increase buttons to the right of **XSize** and **YSize** located above navigation image.

If you wish to change the colour map of the Diffraction image, above the image there is a drop down menu with all of the different colour patterns, click on the one you want of to change the colour pattern.

**<u>Circular Center</u>**

To use the **Find circular center** function, navigate to the **Find circular center button** under the **functions** heading, and click on it.  
This will bring up a form with all of the available parameters, change them to your liking, these will save for future use and if you want it to return to the default values, click **restore defaults**. Once you are happy with your input parameters click **OK** and the circular center tab will pop up showing you the relevant images.

**<u>Remove Aperture</u>**

The **Remove Aperture** function works in the exact same way as the **find circular center function, however, the find circular center function must be used/calculated before using the remove aperture function.**


**<u>Center of Mass</u>**

The **Center of Mass** function requires the **Remove Aperture** functions to have been calculated before using this function.

Once clicked, input the specific parameters you want and click **OK**, this will calculate the center of mass based on the previous data and the files provided and generate the statistics on the **Workflow help** subsection.

**<u>Ransac Tools</u>**

The **Ransac Tools** function must have center of mass ran before it can output data.

**<u>DPC Explorer</u>**

DPC Explorer will output different data depending on what is run before, as certain parameters will have a different effect on the output.

# Live Coding

**<u>Information</u>**

Live Coding can be accessed through **Explorer**, **Live Coding** or using CTRL-I  
It consist of a ipython shell that behave like any other python shell  
However it also has access to the application data using **fpd_app**.  
With this you can use this shell as a jupyter notebook.

**<u>Important Ipython commands</u>**

*   %/save [filename] [startLine]-[endLine]
*   %/load [filename]
*   SHIFT-ENTER to run cell
*   More commands can be found at : [Line magic](https://ipython.readthedocs.io/en/stable/interactive/magics.html)

**<u>Important FPD-Explorer commands</u>**

This command allow the user to add some dataset to a specific button to use it with the GUI  
**fpd_app.add_data([location], [name], [data])**  

**[location]** correspond to which button you want to add an option. It can be:

*   dpc : for adding to DPC Explorer
*   circular : for adding to Find Circular Center
*   mass : for adding to center of Mass
*   ransac : for adding to Ransac Tools
*   matching : for adding to Macthing Image
*   edge : for adding to Disc Edge Sigma
*   ref : for adding to Make Ref Im
*   phase : for adding to Phase Correlation
*   vadf : for adding to Virtual ADF

**[name]** correspond to the name you want the dataset to appear  
**[data]** correspond to the variable name under which the dataset is loaded
