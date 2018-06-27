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
# AAX
aax_base_path = "/Library/Application Support/Avid/Audio/"
plug_aax_used_path = os.path.join(aax_base_path, "Plug-Ins/")
plug_aax_unused_path = os.path.join(aax_base_path, "Plug-Ins (Unused)/")

aax_suffix = ".aaxplugin"

# Waves
plug_waves_path = "/Applications/Waves/Plug-Ins V9/"

waves_suffix = ".bundle"

# VST and AU
other_plug_base = "/Library/Audio/Plug-Ins/"
plug_vst_path = os.path.join(other_plug_base, "VST")
plug_vst3_path = os.path.join(other_plug_base, "VST3")
plug_au_path = os.path.join(other_plug_base, "Audio Units")

vst_suffix = ".vst"
vst3_suffix = ".vst3"
au_suffix = ".au"

plist_path = "Contents/Info.plist"

# {plugin_type: [path, suffix, plist_path]}
plugin_info_dict = {"AAX": [plug_aax_used_path, aax_suffix, plist_path],
                    "AAX Unused": [plug_aax_unused_path, aax_suffix, plist_path],
                    "Waves": [plug_waves_path, waves_suffix, plist_path],
                    "AU": [plug_au_path, au_suffix, plist_path],
                    "VST": [plug_vst_path, vst_suffix, plist_path],
                    "VST3": [plug_vst3_path, vst3_suffix, plist_path]}


class Plugin:

    def __init__(self, type, fullname, path, suffix, version):
        self.type = type
        self.fullname = fullname
        self.path = path
        self.version = version
        self.fullpath = os.path.join(self.path, self.fullname)
        self.shortname = fullname.replace(suffix, "")
    # All will have:
        # manufactuer
        # info (not all will have this, look at plist file)

    def file_output(self):
        return [self.shortname, self.version, self.type]

    def gui_output(self):
        return "{},{},{}".format(self.shortname, self.version, self.type)

    def __str__(self):
        return "{:<30}{:^30}{:>30}".format(self.shortname, self.version, self.type)

class AAX(Plugin):

    used_path = "/Library/Application Support/Avid/Audio/Plug-Ins"
    unused_path = "/Library/Application Support/Avid/Audio/Plug-Ins (Unused)"

    def __init__(self, type, fullname, path, suffix, version):
        super().__init__(type, fullname, path, suffix, version)

        if self.unused:
            self.type = "AAX Unused"
        else:
            self.type = "AAX"

    # Not currently implemented
    def move_plug(self):
        if not self.unused[0]:
            password = getpass("Password: ")
            os.system("{} mv {} {}".format(self.sudo(password), self.fullpath, self.unused_path))
            self.path = self.unused_path

        else:
            password = getpass("Password: ")
            os.system("{} mv {} {}".format(self.sudo(password), self.fullpath, self.used_path))
            self.path = self.used_path

    @staticmethod
    def sudo(password):
        return "echo {} | sudo -S".format(password)


    @property
    def unused(self):
        if "Unused" in self.path:
            return True
        else:
            return False

    # @classmethod
    # def from_list(cls, input_list):
    #     return cls(input_list[0], input_list[1], input_list[2])

class Waves(Plugin):

    def __init__(self, type, fullname, path, suffix, version):
        super().__init__(type, fullname, path, suffix, version)


class VST(Plugin):

    def __init__(self, type, fullname, path, suffix, version):
        super().__init__(type, fullname, path, suffix, version)


class VST3(Plugin):

    def __init__(self, type, fullname, path, suffix, version):
        super().__init__(type, fullname, path, suffix, version)

class AU(Plugin):

    def __init__(self, type, fullname, path, suffix, version):
        super().__init__(type, fullname, path, suffix, version)

    # @classmethod
    # def from_list(cls, input_list):
    #     return cls(input_list[0], input_list[1], input_list[2])


def read_plist(path, plist_path):  # web_keyword
    key_found = False
    version_keywords = ["CFBundleShortVersionString", "CFBundleVersion"]

    plist_loc = os.path.join(path, plist_path)
    with open(plist_loc, "rb") as file:
        file_info = plistlib.load(file)

    version_keyword = 0
    while not key_found:
        try:
            version = file_info[version_keywords[version_keyword]]
            key_found = True
        except KeyError:
            version_keyword += 1
            if (version_keyword - 1) > len(version_keywords):
                version = "Version Not Found"
                key_found = True

    # website = file_info[web_keyword]
    return version  # website

"""Document function once amended."""
def find_plugin_info(path, suffix, plist_path, new_class, type):  # web_keyword,
    info_dict = {}
    for root, dirs, files in os.walk(path):
        for dir in dirs:
            if dir.endswith(suffix):
                full_path = os.path.join(root, dir)
                version = read_plist(full_path, plist_path)
                add_class = new_class(type, dir, full_path, suffix, read_plist(full_path, plist_path))
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
    all_plugins = []
    plugin_classes = {"AAX": AAX, "AAX Unused": AAX, "Waves": Waves, "VST": VST, "VST3": VST3, "AU": AU}

    for key, value in plugin_info_dict.items():
        new_item = find_plugin_info(value[0], value[1], value[2], plugin_classes[key], key)
        all_plugins.append(new_item)

    return all_plugins

def export_plugins_list(filename, list_to_export, category, all_plugins=True, sep_files=False):

    if all_plugins:
        count = 0
        if sep_files:
            source_path, stripped_filename = filename.rsplit("/", 1)
            os.system("mkdir {}".format(filename))
            filename = os.path.join(filename, stripped_filename)
            for plugin_class in list_to_export:
                if len(plugin_class) == 0:
                    pass
                    count += 1
                else:
                    with open(filename + "_" + category[count] + ".csv", "w+") as save_file:
                        writerfile = csv.writer(save_file, delimiter=",")
                        writerfile.writerow([category[count]])
                        writerfile.writerow(["{:^2}".format("Plugin"),
                                             "{:^2}".format("Version"),
                                             "{:^2}".format("Type")])
                        for plugin in plugin_class.values():
                            writerfile.writerow(plugin.file_output())
                        writerfile.writerow(["Total " + category[count] + ": " + str(len(plugin_class))])
                        writerfile.writerow([" "])
                        count += 1
        else:
            with open(filename + ".csv", "w+") as save_file:
                writerfile = csv.writer(save_file, delimiter=",")
                for plugin_class in list_to_export:
                    if len(plugin_class) == 0:
                        pass
                        count += 1
                    else:
                        writerfile.writerow([category[count]])
                        writerfile.writerow(["{:^2}".format("Plugin"),
                                             "{:^2}".format("Version"),
                                             "{:^2}".format("Type")])
                        for plugin in plugin_class.values():
                            writerfile.writerow(plugin.file_output())
                        writerfile.writerow(["Total " + category[count] + ": " + str(len(plugin_class))])
                        writerfile.writerow([" "])
                        count += 1

    elif not sep_files:
        count = 0
        with open(filename + ".csv", "w+") as save_file:
            writerfile = csv.writer(save_file, delimiter=",")
            for plugin_class in list_to_export:
                if plugin_class == 0:
                    pass
                else:
                    writerfile.writerow([category[count]])
                    writerfile.writerow(["{:^2}".format("Plugin"),
                                         "{:^2}".format("Version"),
                                         "{:^2}".format("Type")])
                    for plugin in plugin_class.values():
                        writerfile.writerow(plugin.file_output())
                    writerfile.writerow(["Total " + category[count] + ": " + str(len(plugin_class))])
                    writerfile.writerow([" "])
                    count += 1


    else:
        source_path, stripped_filename = filename.rsplit("/", 1)
        os.system("mkdir {}".format(filename))
        filename = os.path.join(filename, stripped_filename)
        with open(filename + "_" + category + ".csv", "w+") as save_file:
            writerfile = csv.writer(save_file, delimiter=",")
            writerfile.writerow(["Plugin", "Version", "Type"])
            writerfile.writerow([category])

            for printer in list_to_export.values():
                writerfile.writerow(["Total " + category + ": " + str(len(list_to_export))])
                writerfile.writerow(printer.file_output())

def main():
    pass


if __name__ == "__main__":
    main()
