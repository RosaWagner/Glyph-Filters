#MenuTitle: 31. Iso
# -*- coding: utf-8 -*-
__doc__="""
31. Iso
"""

import GlyphsApp
from NaNGFGraphikshared import *
from NaNGFAngularizzle import *
from NaNGFSpacePartition import *

# COMMON
font = Glyphs.font
selectedGlyphs = beginFilterNaN(font)


# ====== OFFSET LAYER CONTROLS ================== 

def doOffset( Layer, hoffset, voffset ):
	try:
		offsetCurveFilter = NSClassFromString("GlyphsFilterOffsetCurve")
		offsetCurveFilter.offsetLayer_offsetX_offsetY_makeStroke_autoStroke_position_error_shadow_( Layer, hoffset, voffset, False, False, 0.5, None,None)
	except Exception as e:
		print("offset failed")

def saveOffsetPaths( Layer , hoffset, voffset, removeOverlap):
	templayer = Layer.copy()
	templayer.name = "tempoutline"
	currentglyph = Layer.parent
	currentglyph.layers.append(templayer)
	tmplayer_id = templayer.layerId
	doOffset(templayer, hoffset, voffset)
	if removeOverlap==True: templayer.removeOverlap()
	offsetpaths = templayer.paths
	del currentglyph.layers[tmplayer_id]
	return offsetpaths

# ================================================


def SortCollageSpace(thislayer, outlinedata, outlinedata2, gridsize, bounds):

	final_in_triangles = []
	in_triangles = []
	out_triangles = []
	edge_triangles = []

	isogrid = makeIsometricGrid(bounds, gridsize)

	isogrid = SnapToGrid(isogrid, gridsize)

	alltriangles = IsoGridToTriangles(isogrid)
	# Return triangles within and without
	in_out_triangles = returnTriangleTypes(alltriangles, outlinedata)
	in_triangles = in_out_triangles[0]
	out_triangles = in_out_triangles[1]

	#edge_triangles = StickTrianglesToOutline(out_triangles, outlinedata)
	edge_triangles = ReturnOutlineOverlappingTriangles(out_triangles, outlinedata)	

	return TrianglesListToPaths(edge_triangles)

	

# ---------


def SnapToGrid(lines, gridsize):

	for n in range(0, len(lines)):
		line = lines[n]
		for l in range(0, len(line)):
			x = lines[n][l][0]
			y = lines[n][l][1]
			gridy = int(y/gridsize)*gridsize
			lines[n][l][0] = x
			lines[n][l][1] = gridy

	return lines


def ApplyIso(thislayer, groups, gridsize):

	isopaths = []

	for g in groups:

		if len(g)>2:

			for path in g:

				isopaths.append(path)

	return isopaths


def OutputTopography():

	for glyph in selectedGlyphs:

		glyph.beginUndo()
		beginGlyphNaN(glyph)

		# --- °°°°°°°

		thislayer = font.glyphs[glyph.name].layers[0]
		thislayer.beginChanges()

		# ---
		
		glyphsize = glyphSize(glyph)

		if glyphsize=="S": 
			offset = 0
			gridsize = 45
		if glyphsize=="M": 
			offset = 4
			gridsize = 45
		if glyphsize=="L": 
			offset = 4
			gridsize = 45

		# ----

		pathlist = doAngularizzle(thislayer.paths, 20)
		outlinedata = setGlyphCoords(pathlist)
		bounds = AllPathBounds(thislayer)
		
		offsetpaths = saveOffsetPaths(thislayer, offset, offset, removeOverlap=True)
		pathlist2 = doAngularizzle(offsetpaths, 4)
		outlinedata2 = setGlyphCoords(pathlist2)
		bounds2 = AllPathBoundsFromPathList(pathlist2)

		ClearPaths(thislayer)

		newtris = SortCollageSpace(thislayer, outlinedata, outlinedata2, gridsize, bounds)
		maxchain = random.randrange(200,400)
		groups = BreakUpSpace(thislayer, outlinedata, newtris, gridsize, maxchain)
		isopaths = ApplyIso(thislayer, groups, gridsize)
		isopaths = ConvertPathlistDirection(isopaths, 1)

		AddAllPathsToLayer(isopaths, thislayer)

		thislayer.removeOverlap()

		# ---

		thislayer.endChanges()

		# --- °°°°°°°

		endGlyphNaN(glyph)
		glyph.endUndo()


# =======

OutputTopography()

# =======

#OutputFur()
#OutputSpikes()

endFilterNaN(font)


