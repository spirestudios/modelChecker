from datetime import datetime, timedelta

import maya.cmds as cmds
import maya.api.OpenMaya as om

release = cmds.about(version=True)
version = 2023 if "Preview" in release else int(cmds.about(version=True))
numbers = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}


def trailingNumbers(nodes, SLMesh):
    trailingNumbers = []
    for node in nodes:
        childCheck = cmds.listRelatives(node, c=True) or []
        if node[-1] in numbers:
            if len(childCheck) == 0:
                trailingNumbers.append(node)
            else:
                for child in childCheck:
                    if "_geo" in child:
                        continue
                    else:
                        trailingNumbers.append(node)
                        break
    return trailingNumbers


def transformNamesEndInGeo(nodes, SLMesh):
    """
    Returns a list of shape nodes that don't end in "_geo"
    Each shape node should end in _geo and correspond to a parent transform node
    """
    misnamed = []
    nodes = cmds.ls(nodes, type="transform")
    for node in nodes:
        shapes = cmds.listRelatives(node, shapes=True)
        if shapes is not None:
            if "_geo" not in node:
                misnamed.append(node)
    return misnamed


def duplicatedNames(nodes, SLMesh):
    duplicatedNames = []
    for node in nodes:
        if "|" in node:
            duplicatedNames.append(node)
    return duplicatedNames


def namespaces(nodes, SLMesh):
    namespaces = []
    for node in nodes:
        if ":" in node:
            namespaces.append(node)
    return namespaces


def shapeNames(nodes, SLMesh):
    shapeNames = []
    for node in nodes:
        new = node.split("|")
        shapes = cmds.listRelatives(node, shapes=True)
        if shapes is not None:
            for shape in shapes:
                shapename = new[-1] + "Shape"
                if shape != shapename:
                    shapeNames.append(shape)
    return shapeNames


def triangles(_, SLMesh):
    triangles = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            numOfEdges = faceIt.getEdges()
            if len(numOfEdges) == 3:
                faceIndex = faceIt.index()
                componentName = str(objectName) + ".f[" + str(faceIndex) + "]"
                triangles.append(componentName)
            if version < 2020:
                faceIt.next(None)
            else:
                faceIt.next()
        selIt.next()
    return triangles


def ngons(_, SLMesh):
    ngons = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            numOfEdges = faceIt.getEdges()
            if len(numOfEdges) > 4:
                componentName = str(objectName) + ".f[" + str(faceIt.index()) + "]"
                ngons.append(componentName)
            if version < 2020:
                faceIt.next(None)
            else:
                faceIt.next()
        selIt.next()
    return ngons


def hardEdges(_, SLMesh):
    hardEdges = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.isSmooth == False and edgeIt.onBoundary() == False:
                componentName = str(objectName) + ".e[" + str(edgeIt.index()) + "]"
                hardEdges.append(componentName)
            edgeIt.next()
        selIt.next()
    return hardEdges


def lamina(_, SLMesh):
    selIt = om.MItSelectionList(SLMesh)
    lamina = []
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            laminaFaces = faceIt.isLamina()
            if laminaFaces == True:
                faceIndex = faceIt.index()
                componentName = str(objectName) + ".f[" + str(faceIndex) + "]"
                lamina.append(componentName)
            if version < 2020:
                faceIt.next(None)
            else:
                faceIt.next()
        selIt.next()
    return lamina


def zeroAreaFaces(_, SLMesh):
    zeroAreaFaces = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            faceArea = faceIt.getArea()
            if faceArea <= 0.00000001:
                componentName = str(objectName) + ".f[" + str(faceIt.index()) + "]"
                zeroAreaFaces.append(componentName)
            if version < 2020:
                faceIt.next(None)
            else:
                faceIt.next()
        selIt.next()
    return zeroAreaFaces


def zeroLengthEdges(_, SLMesh):
    zeroLengthEdges = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.length() <= 0.00000001:
                componentName = str(objectName) + ".f[" + str(edgeIt.index()) + "]"
                zeroLengthEdges.append(componentName)
            edgeIt.next()
        selIt.next()
    return zeroLengthEdges


def selfPenetratingUVs(transformNodes, SLMesh):
    selfPenetratingUVs = []
    for node in transformNodes:
        if "cornea" in node in node:
            continue
        shape = cmds.listRelatives(node, shapes=True, fullPath=True)
        convertToFaces = cmds.ls(
            cmds.polyListComponentConversion(shape, tf=True), fl=True
        )
        overlapping = cmds.polyUVOverlap(convertToFaces, oc=True)
        if overlapping:
            for node in overlapping:
                selfPenetratingUVs.append(node)
    return selfPenetratingUVs


def nonManifoldEdges(_, SLMesh):
    nonManifoldEdges = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.numConnectedFaces() > 2:
                componentName = str(objectName) + ".e[" + str(edgeIt.index()) + "]"
                nonManifoldEdges.append(componentName)
            edgeIt.next()
        selIt.next()
    return nonManifoldEdges


def openEdges(_, SLMesh):
    openEdges = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        edgeIt = om.MItMeshEdge(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not edgeIt.isDone():
            if edgeIt.numConnectedFaces() < 2:
                componentName = str(objectName) + ".e[" + str(edgeIt.index()) + "]"
                openEdges.append(componentName)
            edgeIt.next()
        selIt.next()
    return openEdges


def poles(_, SLMesh):
    poles = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        vertexIt = om.MItMeshVertex(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not vertexIt.isDone():
            if vertexIt.numConnectedEdges() > 5:
                componentName = str(objectName) + ".vtx[" + str(vertexIt.index()) + "]"
                poles.append(componentName)
            vertexIt.next()
        selIt.next()
    return poles


def starlike(_, SLMesh):
    starlike = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        polyIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not polyIt.isDone():
            if polyIt.isStarlike() == False:
                componentName = str(objectName) + ".f[" + str(polyIt.index()) + "]"
                starlike.append(componentName)
            if version < 2020:
                polyIt.next(None)
            else:
                polyIt.next()
        selIt.next()
    return starlike


def missingUVs(_, SLMesh):
    missingUVs = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            if faceIt.hasUVs() == False:
                componentName = str(objectName) + ".f[" + str(faceIt.index()) + "]"
                missingUVs.append(componentName)
            if version < 2020:
                faceIt.next(None)
            else:
                faceIt.next()
        selIt.next()
    return missingUVs


def uvRange(_, SLMesh):
    uvRange = []
    selIt = om.MItSelectionList(SLMesh)
    mesh = om.MFnMesh(selIt.getDagPath())
    objectName = selIt.getDagPath().getPath()
    Us, Vs = mesh.getUVs()
    for i in range(len(Us)):
        if Us[i] < 0 or Us[i] > 10 or Vs[i] < 0:
            componentName = str(objectName) + ".map[" + str(i) + "]"
            uvRange.append(componentName)
    return uvRange


def onBorder(_, SLMesh):
    onBorder = []
    selIt = om.MItSelectionList(SLMesh)
    mesh = om.MFnMesh(selIt.getDagPath())
    objectName = selIt.getDagPath().getPath()
    Us, Vs = mesh.getUVs()
    for i in range(len(Us)):
        if abs(int(Us[i]) - Us[i]) < 0.00001 or abs(int(Vs[i]) - Vs[i]) < 0.00001:
            componentName = str(objectName) + ".map[" + str(i) + "]"
            onBorder.append(componentName)
    return onBorder


def crossBorder(_, SLMesh):
    crossBorder = []
    selIt = om.MItSelectionList(SLMesh)
    while not selIt.isDone():
        faceIt = om.MItMeshPolygon(selIt.getDagPath())
        objectName = selIt.getDagPath().getPath()
        while not faceIt.isDone():
            U, V = set(), set()
            UVs = faceIt.getUVs()
            Us, Vs, = (
                UVs[0],
                UVs[1],
            )
            for i in range(len(Us)):
                u_add = int(Us[i]) if Us[i] > 0 else int(Us[i]) - 1
                v_add = int(Vs[i]) if Vs[i] > 0 else int(Vs[i]) - 1
                U.add(u_add)
                V.add(v_add)
            if len(U) > 1 or len(V) > 1:
                componentName = str(objectName) + ".f[" + str(faceIt.index()) + "]"
                crossBorder.append(componentName)
            if version < 2020:
                faceIt.next(None)
            else:
                faceIt.next()
        selIt.next()
    return crossBorder


def unfrozenTransforms(nodes, SLMesh):
    unfrozenTransforms = []
    for node in nodes:
        if cmds.nodeType(node) == "transform":
            translation = cmds.xform(node, q=True, worldSpace=True, translation=True)
            rotation = cmds.xform(node, q=True, worldSpace=True, rotation=True)
            scale = cmds.xform(node, q=True, worldSpace=True, scale=True)
            if (
                translation != [0.0, 0.0, 0.0]
                or rotation != [0.0, 0.0, 0.0]
                or scale != [1.0, 1.0, 1.0]
            ):
                unfrozenTransforms.append(node)
    return unfrozenTransforms


def layers(nodes, _):
    layers = []
    for node in nodes:
        layer = cmds.listConnections(node, type="displayLayer")
        if layer:
            layers.append(node)
    return layers


def shaders(transformNodes, _):
    # transformNodes = cmds.ls(type="transform")
    shaders = []
    for node in transformNodes:
        shape = cmds.listRelatives(node, shapes=True, fullPath=True)
        if cmds.nodeType(shape) == "mesh" and shape:
            try:
                shadingGrps = cmds.listConnections(shape, type="shadingEngine")
                materials = cmds.ls(cmds.listConnections(shadingGrps), materials=True)
                shader = shadingGrps[0].split("_", 1)
                material = materials[0].split("_", 1)
                if shader[1] != material[1] or shader[0] != "MI" or material[0] != "M":
                    shaders.append(node)
            except:
                shaders.append(node)
    return shaders


def history(nodes, SLMesh):
    history = []
    cleanedTime = cmds.fileInfo("spireHistoryCleaned", query=True)
    if (
        len(cleanedTime) != 0
        and datetime.strptime(cleanedTime[0], "%Y-%m-%d %H:%M:%S.%f")
        + timedelta(hours=1)
        > datetime.now()
    ):
        return history
    else:
        history.append("re-run spire remove history")
        return history


def uncenteredPivots(nodes, SLMesh):
    uncenteredPivots = []
    for node in nodes:
        if cmds.nodeType(node) == "transform":
            if cmds.xform(node, q=1, ws=1, rp=1) != [0, 0, 0]:
                uncenteredPivots.append(node)
    return uncenteredPivots


def emptyGroups(nodes, SLMesh):
    emptyGroups = []
    for node in nodes:
        children = cmds.listRelatives(node, ad=True)
        if not children and "Shape" not in node:
            emptyGroups.append(node)
    return emptyGroups


def parentGeometry(transformNodes, SLMesh):
    parentGeometry = []
    transformNodes = cmds.ls(transformNodes, type="transform")
    for node in transformNodes:
        parents = cmds.listRelatives(node, p=True, fullPath=True) or []
        for parent in parents:
            children = cmds.listRelatives(parent, fullPath=True) or []
            for parent in children:
                if cmds.nodeType(parent) == "mesh" and cmds.nodeType(node) != "shape":
                    parentGeometry.append(node)
    return parentGeometry


def keyFrames(nodes, SLMesh):
    keyFrames = []
    for node in nodes:
        shape = cmds.listRelatives(node, shapes=True, fullPath=True)
        if shape and cmds.nodeType(shape[0]) == "mesh":
            if cmds.currentTime(query=True) != cmds.findKeyframe(
                hi="below", shape=True, which="last"
            ):
                keyFrames += shape
    return keyFrames


def unknowns(nodes, _):
    return cmds.ls(type="unknown")


def noTextureIsolateNode(nodes, _):
    """
    Checks if your scene has any textureIsolateSelect nodes which cause issues down the line
    """
    issues = []
    nodes = cmds.ls(st=1)
    for node in nodes:
        if "textureEditorIsolateSelect" in node:
            issues.append(node)
    return issues


def uvSetName(_, SLMesh):
    return cmds.polyUVSet(uvs="map1", projections=True)
    # probably should switch to a regex, but Randy says only 'map1' causes issues


def multipleUvSets(nodes, _):
    multiples = []
    for node in nodes:
        if cmds.nodeType(node) == "mesh":
            try:
                second_set = node.uvSet[1]
                multiples.append(node)
            except:
                pass
