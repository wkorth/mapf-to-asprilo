import os
import sys

# TODO: Maybe different verbosity grades?

terms = {".": ("node",), "T": ("tree", "node"), "W": ("water", "node")}

termcounter = dict((term, 0) for tuple in terms.values() for term in tuple)


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


def aspriloStatements(char, x, y):
    statement = ""
    for t in terms[char]:
        termcounter[t] += 1
        statement += (
            f"init(object({t},{termcounter[t]}),"
            f"value(at,({x},{y}))).\n"
        )
    return statement


def mapfConvert(sourceFile, targetFile):

    for k in termcounter.keys():
        termcounter[k] = 0

    with open(sourceFile, 'r') as source:
        # TODO: Use General Expressions
        mapName = os.path.basename(sourceFile)[:-4]
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
                        target.write(aspriloStatements(c, column, row))


def convertFile(sourceFile, targetDir):
    if not os.path.exists(targetDir):
        os.mkdir(targetDir)
    mapfFile = os.path.basename(sourceFile)
    print(f"Converting {mapfFile}...")
    mapfConvert(sourceFile, f"{targetDir}/{os.path.splitext(mapfFile)[0]}.lp")
    print("Finished")


def convertDir(sourceDir, targetDir):
    if not os.path.exists(targetDir):
        os.mkdir(targetDir)
    for mapfFile in [file.name for file in os.scandir(sourceDir)
                     if file.name.endswith(".map")]:

        print(f"Converting {mapfFile}...")
        mapfConvert(f"{sourceDir}/{mapfFile}",
                    f"{targetDir}/{os.path.splitext(mapfFile)[0]}.lp")

    print("Finished")


# TODO: handling of wrong arguments
def main(argv):
    source, targetDir = argv[1], argv[2]

    if os.path.isdir(source):
        convertDir(source, targetDir)

    elif os.path.isfile(source):
        convertFile(source, targetDir)

    else:
        print("Error: Cannot find source file(s)")
        sys.exit(2)


main(sys.argv)
# print(f"Source directory: {sourceFolder}")
# print(f"Target directory: {targetFolder}")
# convertDir(sourceFolder, targetFolder)
