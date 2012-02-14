Sublime Text 2 plugin: Goto Symbol
==================================

This plugin adds a command to Sublime Text 2, allowing you to jump between the symbol of your open files.

Supports
--------

 * PHP
 * JS
 * Python
 * Shell script
 * ... (languages' regexp are customizable via the settings file)

Submit a patch adding more and I'll include it.

Using
-----

 * Use ctrl+shift+r (command on OSX) to list the existing symbols in your open files.
 * While your cursor is on a word, use alt+click to jump to the relative symbol's definition of the word.

Notes
-----
 * Sometimes, system does not allow using of alt+click, you'll need to remap the key binding to another one.
 * After the installation, you'll need to restart Sublime Text 2.

Installation
------------

The recommmended method of installation is via Package Control. It will download upgrades to your packages automatically.

### Package Control ###

* Follow instructions on http://wbond.net/sublime_packages/package_control
* Install using Package Control: Install > Goto Symbol package

### Using Git ###

Go to your Sublime Text 2 Packages directory and clone the repository using the command below:

    git clone https://github.com/SublimeText/Goto Symbol "Goto Symbol"

### Download Manually ###

* Download the files using the GitHub .zip download option
* Unzip the files and rename the folder to `Goto Symbol`
* Copy the folder to your Sublime Text 2 Packages directory
