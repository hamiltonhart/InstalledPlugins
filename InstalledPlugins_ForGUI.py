#!/usr/local/bin/python3

# Created by George Hart

# Should the find and read functions run immediately with minimal arguments and create classes based on path? I think so
# How best to order and sort then for user interaction? Alphabetically, search, by first letter, manufacturer?
# Option to export to a csv file. Can this be used in excel? If not, what can?
# Take input list and confirm installation? Would be super cool
# Option to move to/from Unused. sudo called from python?

import os
import plistlib
from getpass import getpass
import csv
import subprocess


# Variables
website_key = "CFBundleIdentifier"
version_key = "CFBundleShortVersionString"

plug_aax_used_path = "/Library/Application Support/Avid/Audio/Plug-Ins/"
plug_aax_unused_path = "/Library/Application Support/Avid/Audio/Plug-Ins (Unused)/"
plug_waves_path = "/Applications/Waves/Plug-Ins V9/"
plist_path = "Contents/Info.plist"

aax_suffix = ".aaxplugin"
waves_suffix = ".bundle"

class Plugin:

    def __init__(self, fullname, path, version):
        self.fullname = fullname
        self.path = path
        self.version = version
        self.fullpath = os.path.join(self.path, self.fullname)
    # All will have:
        # manufactuer
        # info (not all will have this, look at plist file)

class AAXPlugin(Plugin):

    used_path = "/Library/Application Support/Avid/Audio/Plug-Ins"
    unused_path = "/Library/Application Support/Avid/Audio/Plug-Ins (Unused)"

    def __init__(self, fullname, path, version):
        super().__init__(fullname, path, version)
        self.shortname = fullname.replace(".aaxplugin", "")

    def move_plug(self):
        if not self.unused[0]:
            password = getpass("Password: ")
            os.system("{} mv {} {}".format(self.sudo(password), self.fullpath, self.unused_path))
            self.path = self.unused_path

        else:
            password = getpass("Password: ")
            os.system("{} mv {} {}".format(self.sudo(password), self.fullpath, self.used_path))
            self.path = self.used_path

    def file_output(self):
        return [self.shortname, self.version, self.unused[1]]

    @property
    def unused(self):
        if "Unused" in self.path:
            return True, "Plug-Ins Unused"
        else:
            return False, "Plug-Ins"

    @classmethod
    def from_list(cls, input_list):
        return cls(input_list[0], input_list[1], input_list[2])

    @staticmethod
    def sudo(password):
        return "echo {} | sudo -S".format(password)

    def gui_output(self):
        return "{},{},{}".format(self.shortname, self.version, self.unused[1])


    def __str__(self):
        return "{:<30}{:^30}{:>30}".format(self.shortname, self.version, self.unused[1])

class Waves(Plugin):

    def __init__(self, fullname, path, version):
        super().__init__(fullname, path, version)
        self.shortname = fullname.replace(".bundle", "")
        self.waves_flag = "Waves"

    def file_output(self):
        return [self.shortname, self.version, self.waves_flag]

    @classmethod
    def from_list(cls, input_list):
        return cls(input_list[0], input_list[1], input_list[2])

    def gui_output(self):
        return "{},{},{}".format(self.shortname, self.version, self.waves_flag)

    def __str__(self):
        return "{:<30}{:^30}{:>30}".format(self.shortname, self.version, self.waves_flag)

def read_plist(path, vers_keyword, plist_path):  # web_keyword
    plist_loc = os.path.join(path, plist_path)
    with open(plist_loc, "rb") as file:
        file_info = plistlib.load(file)
    version = file_info[vers_keyword]
    # website = file_info[web_keyword]
    return version  # website

def find_plugin_info(path, suffix, vers_keyword, plist_path, new_class):  # web_keyword,
    info_dict = {}
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir.endswith(suffix):
                full_path = os.path.join(root, dir)
                add_class = new_class(dir, full_path, read_plist(full_path, vers_keyword, plist_path))
                info_dict[add_class.shortname] = add_class
    return info_dict  # remove dictionary creation and make class list

def swap_used_unused():
    pass
# if object in used list, remove and add to unused - visa versa

# searches all_plugins.keys() for user input, returns all matches
def search_dicts(user_input, dict_to_search, search_all=True):
    found_plugs = []
    if search_all:
        for item_dict in dict_to_search:
            for plugin in item_dict.keys():
                if user_input in plugin.lower():
                    found_plugs.append(item_dict[plugin])
        return found_plugs  # The call for this function needs to perform a test for length to determine output
    else:
        for plugin in dict_to_search:
            if user_input in plugin.lower():
                found_plugs.append(dict_to_search[plugin])
        return found_plugs

def list_dicts(dict_to_search):
    text_to_return = []
    for class_item in dict_to_search.values():
        text_to_return.append(class_item.gui_output())
    return text_to_return

def create_new_classes():
    aax_dict = find_plugin_info(plug_aax_used_path, aax_suffix, version_key, plist_path, AAXPlugin)
    unused_dict = find_plugin_info(plug_aax_unused_path, aax_suffix, version_key, plist_path, AAXPlugin)
    waves_dict = find_plugin_info(plug_waves_path, waves_suffix, version_key, plist_path, Waves)

    all_plugins = [aax_dict, unused_dict, waves_dict]


    return aax_dict, unused_dict, waves_dict, all_plugins

def export_plugins_list(filename, list_to_export, category, all_plugins=True, sep_files=False):

    new_file = filename

    if all_plugins:
        count = 0
        if sep_files:
            for plugin_class in list_to_export:

                with open(new_file + "_" + category[count] + ".csv", "w+") as save_file:
                    writerfile = csv.writer(save_file, delimiter=",")
                    writerfile.writerow([category[count]])
                    writerfile.writerow(["{:^2}".format("Plugin"),
                                         "{:^2}".format("Version"),
                                         "{:^2}".format("Location")])
                    for plugin in plugin_class.values():
                        writerfile.writerow(plugin.file_output())
                    writerfile.writerow([" "])
                    count += 1
        else:
            with open(new_file + ".csv", "w+") as save_file:
                writerfile = csv.writer(save_file, delimiter=",")
                for plugin_class in list_to_export:
                    writerfile.writerow([category[count]])
                    writerfile.writerow(["{:^2}".format("Plugin"),
                                         "{:^2}".format("Version"),
                                         "{:^2}".format("Location")])
                    for plugin in plugin_class.values():
                        writerfile.writerow(plugin.file_output())
                    writerfile.writerow([" "])
                    count += 1

    elif not sep_files:
        count = 0
        with open(new_file + ".csv", "w+") as save_file:
            writerfile = csv.writer(save_file, delimiter=",")
            for plugin_class in list_to_export:
                writerfile.writerow([category[count]])
                writerfile.writerow(["{:^2}".format("Plugin"),
                                     "{:^2}".format("Version"),
                                     "{:^2}".format("Location")])
                for plugin in plugin_class.values():
                    writerfile.writerow(plugin.file_output())
                writerfile.writerow([" "])
                count += 1


    else:
        with open(new_file + "_" + category + ".csv", "w+") as save_file:
            writerfile = csv.writer(save_file, delimiter=",")
            writerfile.writerow(["Plugin", "Version", "Location"])
            writerfile.writerow([category])

            for printer in list_to_export.values():

                writerfile.writerow(printer.file_output())

def main():
    pass


if __name__ == "__main__":
    main()
