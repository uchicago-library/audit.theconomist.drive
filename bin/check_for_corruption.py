"""a tool to check if files are corrupted
"""

from argparse import ArgumentParser
from hashlib import md5
from xml.etree import ElementTree
from os import _exit, scandir
from PIL import Image
from sys import stdout

XML_ERRORS = []
JPEG_ERRORS = []

def _md5(fname):
    hash_md5 = md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def _find_all_files(file_path):
    try:
        for n in scandir(path=file_path):
            if n.is_dir():
                yield from _find_all_files(n.path)
            elif n.is_file():
                yield n
    except PermissionError:
        appending_file = open("../datafiles/denied_files.txt", "a+", encoding="utf-8")
        appending_file.write("{}\n".format(file_path))
        appending_file.close()

def _validate_jpeg(file_path):
    try:
        img = Image.open(file_path)
        img.verify()
        #stdout.write("{} is a valid JPEG file.\n".format(file_path))
    except (IOError, SyntaxError, ValueError):
        corrupted_file = open("../datafiles/corrupted_jpegs.txt", "a+", encoding="utf-8")
        corrupted_file.write("{}\n".format(file_path))
        corrupted_file.close()

def _validate_xml(file_path):
    try:
        ElementTree.parse(file_path)
        stdout.write("{} is good xml\n".format(file_path))
    except ElementTree.ParseError:
        corrupted_files = open("../datafiles/corrupted_xml.txt", "a+", encoding="utf-8")
        corrupted_files.write("{}\n".format(file_path))
        corrupted_files.close()

def _main():
    arguments = ArgumentParser(description="A tool to check the contents" +
                               " of an external hard drive for corruption.")
    arguments.add_argument("drive_location", type=str, action='store')
    parsed = arguments.parse_args()
    try:
        gen = _find_all_files(parsed.drive_location)
        jpeg_files_count = 0
        xml_files_count = 0
        tbl_files_count = 0
        dtd_files_count = 0
        total_files = 0
        for item in gen:
            if item.path.endswith("JPG"):
                jpeg_files_count += 1
                #_validate_jpeg(item.path)
            elif item.path.endswith(".xml"):
                xml_files_count += 1
                #_validate_xml(item.path)
            elif item.path.endswith(".dtd"):
                dtd_files_count += 1
                # dtd_files = open("../datafiles/dtd_files.txt", "a+", encoding="utf-8")
                # dtd_files.write("{}\n".format(item.path))
                # dtd_files.close()

            elif item.path.endswith(".tbl"):
                try:
                    test = open(item.path, "r")
                    test.close()
                except:
                    stdout.write("{} cannot be opened".format(item.path))
                tbl_files_count += 1
                # tbl_files = open("../datafiles/tbl_files.txt", "a+", encoding="utf-8")
                # tbl_files.write("{}\n".format(item.path))
                # tbl_files.close()
            # else:
            #     stdout.write("hello from {}\n".format(item.path))
            else:
                # undefined_files = open("../datafiles/undefined_files.txt", "a+", encoding="utf-8")
                # undefined_files.write("{}\n".format(item.path))
                # undefined_files.close()
                print("{} does not fit any pre-defined category".format(item.path))
            total_files += 1
            checksum = _md5(item.path)
            inventory_file = open("../datafiles/inventory.txt", "a+", encoding="utf=8")
            inventory_file.write("{}\t{}\n".format(item.path, checksum))
        print("number of jpeg files=" + str(jpeg_files_count))
        print("number of xml files=" + str(xml_files_count))
        print("number of dtd files=" + str(dtd_files_count))
        print("number of tbl files=" + str(tbl_files_count))
        print("total number of files=" + str(total_files))
        return 0
    except KeyboardInterrupt:
        return 131

if __name__ == "__main__":
    _exit(_main())
