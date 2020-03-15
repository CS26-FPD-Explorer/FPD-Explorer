
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
    <p>Live Coding can be accessed through <b>Explorer</b>, <b>Live Coding</b> or using CTRL-I
    <br>It consists of a ipython shell that behaves like any other python shell
    <br>However it also has access to the application data using <b>fpd_app</b>.
    <br>With this you can use this shell as a jupyter notebook.</p>
    <p><strong><u>Important Ipython commands</u></strong></p>
    <ul>
    <li>%/save [filename] [startLine]-[endLine]</li>
    <li>%/load [filename]</li>
    <li>SHIFT-ENTER to run cell</li>
    <li>More commands can be found at :
    <a href="https://ipython.readthedocs.io/en/stable/interactive/magics.html"> Line magic</a></li>
    </ul>
    <p><strong><u>Important FPD-Explorer commands</u></strong></p>
    <p>This command allows the user to add some dataset to a specific button to use it with the GUI
    <br><b>fpd_app.add_data([location], [name], [data])</b><br>
    <br><b>[location]</b> corresponds to which button you want to add an option. It can be:
    <ul>
    <li>dpc : for adding to DPC Explorer</li>
    <li>circular : for adding to Find Circular Center</li>
    <li>mass : for adding to center of Mass</li>
    <li>ransac : for adding to Ransac Tools</li>
    <li>matching : for adding to Macthing Image</li>
    <li>edge : for adding to Disc Edge Sigma</li>
    <li>ref : for adding to Make Ref Im</li>
    <li>phase : for adding to Phase Correlation</li>
    <li>vadf : for adding to Virtual ADF</li>
    </ul>
    <p><b>[name]</b> corresponds to the name you want the dataset to appear
    <br><b>[data]</b> corresponds to the variable name under which the dataset is loaded</p>
    <br>"""

about_software = """<p><strong><u>About the software</u></strong></p>
    <p>This software allows users to analyse and visualise STEM
    images through a range of different functions.</p>
    <p>This software was created using Qt5, Pyside2 and the FPD library.
    <br>This software is lisenced under GPLv3</p>"""

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

    <p>To use Data Browser, look for the <b>DataBrowser</b>
    button underneath the <b>Functions</b> heading in the top
    right of the user interface.
    <br>Click this button and the DataBrowser
    tab will open.
    <br>On the left hand side will be the Navigation image and on
    the right the Diffraction image. </p>
    <p>To navigate through the Diffraction
    image, click on the desired position on the Navigation image, and the Diffraction
    image will update appropriately. </p>
    <p>If you wish to accumulate a larger area of pixels,
    instead of just 1*1, you can click the up/increase buttons
    to the right of <b>XSize</b> and <b>YSize</b> located above navigation image.</p>
    <p>If you wish to change the colour map of the Diffraction image,
    above the image there is a drop
    down menu with all of the different colour patterns, click on the one you want to
    change the colour pattern.</p>

    <p><strong><u>Circular Center</u></strong></p>

    <p>To use the <b>Find circular center</b> function, navigate to the
    <b>Find circular center button</b> under the <b>functions</b> heading,
    and click on it.
    <br>This will bring up a form with all of the available parameters,
    change them to your liking, these will save for future use and if you want it to
    return to the default values, click <b>restore defaults</b>.
    Once you are happy with your input parameters click <b>OK</b>
    and the circular center tab will pop up showing you the relevant images.</p>

    <p><strong><u>Remove Aperture</u></strong></p>

    <p>The <b>Remove Aperture</b> function works in the exact same way as the
    <b>find circular center function, however, the find circular center function
    must be used/calculated before using the remove aperture function.</p>

    <p><strong><u>Center of Mass</u></strong></p>

    <p>The <b>Center of Mass</b> function requires the
    <b>Synthetic Aperture</b> function to have
    been calculated before using this function. </p>
    <p> Once clicked, input the specific parameters you want and click <b>OK</b>,
    this will calculate the center of mass based on the previous data and the files provided
    and generate the statistics on the <b>Workflow help</b> subsection.</p>

    <p><strong><u>Ransac Tools</u></strong></p>

    <p>The <b>Ransac Tools</b> function must have <b>Center
    of mass</b> run, before it can output data.</p>

    <p><strong><u>DPC Explorer</u></strong></p>

    <p><b>DPC</b> Explorer will output different data depending
    on what is run before, as certain parameters will have a
    different effect on the output.
    <br><br> A standard work flow would look like this - <b>Find
    circular center->Synthetic aperture->Center of mass->Ransac tools -> DPC Explorer</b></p>

    <p><strong><u>Matching Images</u></strong></p>

    <p><b>Matching Images</b> requires only the files to be loaded to run this function.</p>

    <p><strong><u>Disc Edge Sigma</u></strong></p>

    <p><b>Disc Edge Sigma</b> requires <b>Matching Images</b> to have been run before
    this function can be used.</p>

    <p><strong><u>Make Ref Im</u></strong></p>

     <p>The <b>Make Ref Im</b> function requires <b>Disc Edge Sigma</b> to have been run before
    it can be run.</p>

    <p><strong><u>Phase Correlation</u></strong></p>

    <p><b>Phase Correlation</b> requires only the files to be loaded to run this function.
    <br>This function is also requires a lot of computational power,
    so the software may appear slow
    when this function is run.</p>

    <p><strong><u>Virtual ADF</u></strong></p>

    <p> The <b>Virtual ADF</b> function requires only <b>Find circular center</b>
    to be run before it can be run.
    <br>It can also be used when loading a <b>npz file/configuration.</b>

    <p><strong><u>Plot VADF</u></strong></p>

    <p><b>Plotting VADF</b> requires  <b>Virtual ADF</b> to be initialised before it can be run.

    <p><strong><u>Annular Slice</u></strong></p>

    <p>The <b>Annular Slice</b> function requires  <b>Virtual ADF</b>
    to be initialised before it can be run.
     """

navigating_and_loading = """
    <p><strong><u>Loading files</u></strong></p>
    <p>You can load 4 types of files .dm3, .mib, .hdf5 and .npz,
    <br>To do this navigate to the top left of the user
    interface, under the <b>File</b> heading.
    Then click on which file type you wish to load.<br>
    You can also use the buttons in the main window.<br>
    A file browser will pop-up,
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
    you will automatically be brought to a new tab screen within the GUI
    upon using one of the functions.</p>
    <p>If you wish to return to the home screen
    either navigate to the <b>home</b>
    tab in the top left, or if you wish for the calculation(if there is one)
    to remain but you want the tab to be removed, either click the red cross on the
    tab or click the <b>OK</b>.</p>
    <p>If you wish to navigate through the tabs the left and right arrow keys can be used.</p>

    <p><strong><u>Workflow help</u></strong></p>

    <p>The workflow help subsection is used to help the user.
    <br>It will notify you when a certain step has been taken,
    for example <b>MIB file loaded correctly</b> or <b>Circular center
    has now been initalized</b>. </p>
    <p>This can be useful for functions which require other
    functions to have been run beforehand to use them (you can check
    to see what you have done/have to do).</p>"""
