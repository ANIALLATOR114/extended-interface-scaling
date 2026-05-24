from zipfile import ZipFile
from argparse import ArgumentParser
from py_compile import compile
import xml.etree.ElementTree as ET
import os
import sys

parser = ArgumentParser()
parser.add_argument("-u", "--username", default="ANIALLATOR", help="Username")
parser.add_argument(
    "-n",
    "--name",
    default="Extended Interface Scaling",
    help="Mod name",
)
parser.add_argument("-v", "--version", default="2.0.0", help="Mod version")
parser.add_argument(
    "-d",
    "--description",
    default="Precision UI scaling with sharpness guidance for World of Tanks PC",
    help="Mod description",
)
parser.add_argument("-f", "--folder", default="./res", help="res folder path")
args = parser.parse_args()

if sys.version_info[:2] != (2, 7):
    sys.stderr.write(
        "Error: Python 2.7 is required to compile WoT mod bytecode.\n"
        "Install Python 2.7.18 from https://www.python.org/downloads/release/python-2718/\n"
        "Then run: C:\\Python27\\python.exe build.py\n"
    )
    sys.exit(1)

mod_id = args.username + "." + args.name.replace(" ", "_")

root = ET.Element("root")
ET.SubElement(root, "id").text = mod_id
ET.SubElement(root, "version").text = args.version
ET.SubElement(root, "name").text = args.name
ET.SubElement(root, "description").text = args.description

XML = ET.ElementTree(root)

res_folder = os.path.normpath(os.path.join(os.getcwd(), args.folder))

if not os.path.isdir(res_folder):
    raise ValueError("Incorrect path to a res folder: %s" % res_folder)

build_dir = "./build"
if not os.path.exists(build_dir):
    os.mkdir(build_dir)

for filename in os.listdir(build_dir):
    path = os.path.join(build_dir, filename)
    if os.path.isfile(path):
        os.remove(path)

XML.write(os.path.join(build_dir, "meta.xml"))


def add_folder(zip_file, folder):
    for elem in os.listdir(folder):
        full_path = os.path.join(folder, elem)
        if os.path.isfile(full_path):
            archive_path = "./res" + full_path.split("res", 1)[1]
            if os.path.splitext(full_path)[1] == ".py":
                compile(full_path)
                pyc_path = full_path + "c"
                zip_file.write(pyc_path, archive_path + "c")
                os.remove(pyc_path)
            else:
                zip_file.write(full_path, archive_path)
        elif os.path.isdir(full_path):
            add_folder(zip_file, full_path)


output_name = mod_id + "_" + args.version + ".wotmod"
package_path = os.path.join(build_dir, output_name)

package = ZipFile(package_path, "w")
package.write(os.path.join(build_dir, "meta.xml"), "meta.xml")
add_folder(package, res_folder)
package.close()

print("Built %s" % package_path)
