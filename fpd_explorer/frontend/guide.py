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
    topics = {"navigating_and_loading": navigating_and_loading, "functions": functions,
              "about_us": about_us, "about_software": about_software, "live_coding": live_coding}
    return topics[topic]


live_coding = """<strong>TO BE UPDATED</strong>"""

about_software = """<p><strong><u>About software</u></strong></p>
<p>The software was created using Qt, Pyside2 and the FPD library.
<br>It is an open source software.</p>"""

about_us = """
<p><strong><u>About us</u></strong></p>
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
<p>To use Data Browser, look for the &lsquo;DataBrowser&rsquo;
button underneath the &lsquo;functions&rsquo; heading in the top
right of the user interface. Click this button and the DataBrowser
tab will open, on the left hand of the tab will be the Navigation image,
the right holding the Diffraction image. To navigate through the Diffraction
image, click on the desired position on the Diffraction image, and the Navigation
image will update appropriately. If you wish to accumulate a larger area of pixels,
instead of just 2x2, you can either use the arrow keys or click the up/increase buttons
to the right of &lsquo;XSize&rsquo; and &lsquo;YSize&rsquo; located above navigation image.
If you wish to change the colour map of the Diffraction image,
above the image there is a drop
 down menu with all of the different colour patterns, click on the one you want of to
 change the colour pattern.</p>
<p><strong><u>Circular Center</u></strong></p>
<p>To use the &lsquo;Find circular center&rsquo; function, navigate to the
 &lsquo;Find circular center button&rsquo; under the &lsquo;functions heading,
 and click on it. This will bring up a form with all of the available parameters,
 change them to your liking, these will save for future use and if you want it to
  return to the default values, click &lsquo;restore defaults&rsquo;.
  Once you are happy with your input parameters click &lsquo;Save&rsquo;
  and the circular center tab will pop up showing you the relevant images.</p>
<p><strong><u>Remove Aperture</u></strong></p>
<p>The &lsquo;Remove Aperture&rsquo; function works in the exact same way as the
&lsquo;find circular center function, however, the find circular center function
must be used/calculated before using the remove aperture function.</p>
<p>&nbsp;<strong><u>Center of Mass</u></strong></p>
<p>The &lsquo;Center of Mass&rsquo; function requires both the &lsquo;
Find circular center&rsquo; and &lsquo;Remove Aperture&rsquo; functions to have
been used/calculated before using this function. If they have been carried out then
navigate to the &lsquo;Center of Mass&rsquo; button underneath the functions tab and
click this button. Input the specific parameters you want and click &lsquo;Save&rsquo;,
this will calculate the center of mass based on the previous data and the files provided
 and generate the statistics on the &lsquo;Workflow help&rsquo; subsection.</p>
<p><strong><u>Ransac Tools</u></strong></p>
<p>The &lsquo;Ransac Tools&rsquo; function must have center
of mass ran before it can output data.</p>
<p><strong><u>DPC Explorer</u></strong></p>
<p>DPC Explorer will output different data depending
 on what is run before, as certain parameters will have a
 different effect on the output.</p>"""

navigating_and_loading = """<p><strong><u>What this software is used for</u></strong></p>
        <p>This software allows users to analyse and visualise electron microscopy
        images through a range of different functions.</p>
        <p><strong><u>Loading files</u></strong></p>
        <p>You can load 2 types of files .dm3 and. mib,
        to do this navigate to the top left of the user
        interface, under the &lsquo;loading files&rsquo; heading.
        Then click on which the filetype button you wish to load
        (.dm3 can be used on it&rsquo;s own but .mib must have a
        .dm3 loaded in conjunction to use the software)
         and your file browser will pop-up ,
        click on the file you want to load in and click
        &lsquo;Open&rsquo;. Once all desired files have been opened,
        click on the &lsquo;Load&rsquo; button.
        A window will pop up asking you for the down sampling rate for
        &lsquo;Diffraction Image&rsquo; and &lsquo;Navigation Image&rsquo;,
        increasing this value will allow for faster load speeds but lower
        quality of data to work with. Increase or decrease this value by using the
        up and down buttons to the right of the box which holds the value 2^3.</p>
        <p><strong><u>Navigating tabs</u></strong></p>
        <p>Tabs are produced through the usage of the functions,
        you will automatically be brought to a new tab screen within the GUI
        upon using one of the functions, if you wish to return to the home screen
        either navigate to the &lsquo;home&rsquo;
        tab in the top left, or if you wish for the calculation(if there is one)
        to remain but you want the tab to be removed, either click the red cross on the
        tab or press the enter button. If you wish to navigate through the tabs, left or
        right, the left and right arrow keys can also be used.</p>
        <p><strong><u>Workflow help</u></strong></p>
        <p>The workflow help subsection is used to help the user,
        it will notify you when a certain step has been taken,
        for example &lsquo;MIB file loaded correctly&rsquo; or &lsquo;Circular center
        has now been initalized&rsquo;. This can be useful for functions which require other
        functions to have been run beforehand to use them(you can check
        to see what you have done/have to do.</p>"""
