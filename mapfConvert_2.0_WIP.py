import os
import sys
from pathlib import Path
# TODO: Maybe different verbosity grades?

terms = {".": "node", "T": "tree", "W": "water"}

termcounter = dict((t, 0) for t in terms.keys())


def showInfo():
    print(
        "mapfConvert\n"
        "Commands:\n"
        "mapfConvert <file or directory>"
        "mapfConvert <file or directory> <directory>"
    )


# TODO: Put amount of atoms in header without significant performance impact
def generateHeader(mapName, mapType, mapHeight, mapWidth):
    return (
        ('%' * 50) + "\n\n"
        f"% Map: {mapName}\n\n"
        f"% mapType: {mapType}\n\n"
        f"% Height: {mapHeight}\n\n"
        f"% Width: {mapWidth}\n\n"
        + ('%' * 50) + "\n\n"
    )


def mapfConvert(sourceFile, targetFile):

    for k in termcounter.keys():
        termcounter[k] = 0

    with open(sourceFile, 'r') as source:
        # TODO: Use General Expressions
        mapName = sourceFile.stem
        mapType = source.readline()[5:-1]
        mapHeight = int(source.readline()[7:-1])
        mapWidth = source.readline()[6:-1]
        source.readline()

        with open(targetFile, 'w') as target:

            target.write(generateHeader(mapName, mapType, mapHeight, mapWidth))

            for row in range(1, mapHeight + 1):
                column = 0
                for c in source.readline():
                    column += 1
                    if c in terms.keys():
                        termcounter[c] += 1
                        target.write(
                            f"init(object({terms[c]},{termcounter[c]}),"
                            f"value(at,({row},{column}))).\n")


def convertFile(sourceFile, targetDir):
    if not sourceFile.exists():
        os.mkdir(targetDir)
    mapfFile = os.path.basename(sourceFile)
    print(f"Converting {mapfFile}...")
    mapfConvert(sourceFile, f"{targetDir}/{os.path.splitext(mapfFile)[0]}.lp")
    print("Finished")


def convertDir(sourceDir, targetDir):
    if not targetDir.exists():
        targetDir.mkdir()
    for mapfFile in (file.name for file in targetDir.iterdir()
                     if file.name.endswith(".map")):

        print(f"Converting {mapfFile}...")
        mapfConvert(f"{sourceDir}/{mapfFile}",
                    f"{targetDir}/{os.path.splitext(mapfFile)[0]}.lp")

    print("Finished")


# TODO: handling of wrong arguments
def main(argv):

    if len(argv) == 2:
        source = Path(argv[1])
        if not source.exists():
            print("Error: Cannot find source file(s)")
            sys.exit(2)

        if source.is_dir():
            convertDir(source, source)
        elif source.is_file():
            targetDir = source.

    elif len(argv) == 3:
        source, targetDir = argv[1], argv[2]

        if source.is_dir():
            convertDir(source, targetDir)

        elif source.is_file():
            convertFile(source, targetDir)

        else:
            print("Error: Cannot find source file(s)")
            sys.exit(2)

    else:
        showInfo()
        return


main(sys.argv)
# print(f"Source directory: {sourceFolder}")
# print(f"Target directory: {targetFolder}")
# convertDir(sourceFolder, targetFolder)
