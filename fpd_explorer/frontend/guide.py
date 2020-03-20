# Copyright 2019-2020 Florent AUDONNET, Michal BROOS, Bruce KERR, Ewan PANDELUS, Ruize SHEN

# This file is part of FPD-Explorer.

# FPD-Explorer is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# FPD-Explorer is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY
# without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with FPD-Explorer.  If not, see < https: // www.gnu.org / licenses / >.


def get_guide(topic):
    """
    Returns the html-formatted guide text based on the parameter topic.

    Parameters
    ----------
    topic : str
        Key to look up in the dictionary of guide topics.
    """
    return globals()[topic]


live_coding = """<p><strong><u>Information</u></strong></p>
    <p>Live Coding can be accessed through <b>Explorer->Live Coding</b> or using CTRL-I shortcut.
    <br>It consists of an IPython shell that behaves like any other Python shell.
    <br>However it also has access to the application data using <b>fpd_app</b>.
    <br>With this you can use this shell as a Jupyter notebook.</p>
    <p><strong><u>Important IPython commands</u></strong></p>
    <ul>
    <li>%/save [filename] [startLine]-[endLine]</li>
    <li>%/load [filename]</li>
    <li>SHIFT-ENTER to run cell</li>
    <li>More commands can be found at :
    <a href="https://ipython.readthedocs.io/en/stable/interactive/magics.html"> Line magic</a></li>
    </ul>
    <p><strong><u>Important FPD-Explorer commands</u></strong></p>
    <p>The following command allows the user to add a dataset to a specific button and use it within the interface:
    <br><b>fpd_app.add_data([location], [name], [data])</b><br>
    <br><b>[location]</b> corresponds to the button to add an option to. It can be:
    <ul>
    <li>data : for adding to fpgn of Data Browser</li>
    <li>nav: for adding to nav_im of Data Browser</li>
    <li>circular : for adding to Find Circular Center</li>
    <li>mass : for adding to Center of Mass</li>
    <li>ransac : for adding to Ransac Tools</li>
    <li>dpc : for adding to DPC Explorer</li>
    <li>matching : for adding to Matching Images</li>
    <li>edge : for adding to Disc Edge Sigma</li>
    <li>ref : for adding to Make Ref Im</li>
    <li>phase : for adding to Phase Correlation</li>
    <li>vadf : for adding to Virtual ADF</li>
    </ul>
    <p><b>[name]</b> corresponds to the name the dataset will show as in the interface
    <br><b>[data]</b> corresponds to the variable name under which the dataset is loaded</p>
    <br>"""

about_software = """<p><strong><u>About the software</u></strong></p>
    <p>This software allows users to analyse and visualise STEM
    images through a range of different functions.</p>
    <p>This software was created using Qt5, Pyside2 and the FPD library.</p>
    <p>This software is licensed under GPLv3.</p>"""

about_us = """<p><strong><u>About us</u></strong></p>
    <p>This software was created by:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</p>
    <ul>
    <li>Bruce Kerr</li>
    <li>Ewan Pandelus</li>
    <li>Florent Audonnet</li>
    <li>Michal Broos</li>
    <li>Ruize Shen</li>
    </ul>
    """

functions = """<p><strong><u>Data Browser</u></strong></p>

    <p>To use Data Browser, look for the <b>Data Browser</b>
    button underneath the <b>Functions</b> heading in the top
    right of the user interface.
    <br>Click this button and the Data Browser tab will open.
    <br>The Navigation image will be on the left and the Diffraction image on the right.</p>
    <p>To navigate through the Diffraction
    image, click on the desired position in the Navigation image, and the Diffraction
    image will update appropriately.</p>
    <p>If you wish to accumulate a larger area of pixels,
    instead of just 1*1, you can click the up buttons
    to the right of <b>XSize</b> and <b>YSize</b> located above the navigation image.</p>
    <p>If you wish to change the colour map of the Diffraction image,
    there is a drop down menu above the image with different colour maps.
    Simply click on one of your choice and the image will update automatically.</p>

    <p><strong><u>Circular Center</u></strong></p>

    <p>To use the Find Circular Center function, navigate to the
    Find Circular Center button under the <b>functions</b> heading,
    and click on it.
    <br>This will bring up a form with all of the available parameters,
    change them to your liking. The parameters will save for future use and if you want it to
    return to the default values, click <b>Restore defaults</b>.
    Once you are happy with your input parameters click <b>OK</b>
    and the circular center tab will pop up showing the relevant images.</p>

    <p><strong><u>Synthetic Aperture</u></strong></p>

    <p>The Synthetic Aperture function works in the exact same way as the
    <b>Find Circular Center</b> function. However, the circular center
    must be calculated before using <b>Synthetic Aperture</b>.</p>

    <p><strong><u>Center of Mass</u></strong></p>

    <p>The Center of Mass function requires the
    <b>Synthetic Aperture</b> to have been calculated.</p>
    <p> Once clicked, input the specific parameters you want and click <b>OK</b>.
    This will calculate the center of mass based on the previous data and the files provided
    and generate the statistics in the <b>Workflow help</b> section.</p>

    <p><strong><u>Ransac Tools</u></strong></p>

    <p>The Ransac Tools function requires <b>Center of Mass</b>
    to have been run before it can output data.</p>

    <p><strong><u>DPC Explorer</u></strong></p>

    <p>DPC Explorer will output different data depending
    on what is run beforehand. Certain parameters will have a
    different effect on the output.
    <br><br> A standard work flow would look like this: <b>Find
    Circular Center->Synthetic Aperture->Center of Mass->Ransac Tools->DPC Explorer</b></p>

    <p><strong><u>Matching Images</u></strong></p>

    <p>Requires only the files to be loaded to run.</p>

    <p><strong><u>Disc Edge Sigma</u></strong></p>

    <p>Requires <b>Matching Images</b> to have been run.</p>

    <p><strong><u>Make Ref Im</u></strong></p>

    <p>Requires <b>Disc Edge Sigma</b> to have been run.</p>

    <p><strong><u>Phase Correlation</u></strong></p>

    <p>Requires only the files to be loaded to run.
    <br>This function also requires a lot of computational power.
    <br>The software may appear slow while running this function.</p>

    <p><strong><u>Virtual ADF</u></strong></p>

    <p>Requires only <b>Find Circular Center</b>
    to be run.
    <br>It can also be used when loading an <b>npz file/configuration.</b>

    <p><strong><u>Plot VADF</u></strong></p>

    <p>Requires only <b>Virtual ADF</b> to be initialised.

    <p><strong><u>Annular Slice</u></strong></p>

    <p>Requires only <b>Virtual ADF</b> to be initialised.
     """

navigating_and_loading = """
    <p><strong><u>Loading files</u></strong></p>
    <p>You can load 4 types of files: .mib, .dm3, .hdf5 and .npz.
    <br>To do this navigate to the top left of the user
    interface, under the <b>File</b> heading.
    Then click on which file type you wish to load.<br>
    You can also use the buttons in the main window.<br>
    A file browser will pop up,
    click on the file you want to load and click
    <b>Open</b>.
    <br>Once all desired files have been opened,
    click on the <b>Load</b> button.</p>
    <p>A window will pop up asking you for the down sampling rate for
    <b>Diffraction Image</b> and <b>Navigation Image</b>.
    <br>Increasing this value will allow for faster load speeds but lower
    quality of data to work with.
    <br>Increase or decrease this value by using the
    up and down buttons to the right of the box which holds the value 2^3.</p>

    <p><strong><u>Navigating tabs</u></strong></p>

    <p>Tabs are produced through the usage of the functions,
    you will automatically be brought to a new tab screen within the interface
    upon using one of the functions.</p>
    <p>If you wish to return to the home screen
    either navigate to the <b>Home</b>
    tab in the top left. If you wish for the calculation (if there is one)
    to remain but you want the tab to be removed, either click the red cross on the
    tab or click the <b>OK</b> button.</p>
    <p>If you wish to navigate through the tabs the left and right arrow keys can be used.</p>

    <p><strong><u>Workflow help</u></strong></p>

    <p>The workflow help section is used to help the user.
    <br>It will notify you when a certain step has been taken. For example,
    <b>MIB file loaded correctly</b> or <b>Circular center
    has now been initalized</b>.</p>
    <br>This can be useful for functions which require other
    functions to have been run beforehand. You can see at any time what has been done.</p>"""
