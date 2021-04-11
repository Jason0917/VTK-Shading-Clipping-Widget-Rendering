import vtk
from vtk.util.colors import brown_ochre, tomato, banana
import argparse

# Reference: https://kitware.github.io/vtk-examples/site/Python/Snippets/WriteImage
def WriteImage(fileName, renWin, rgba=True):
    import os

    if fileName:
        # Select the writer to use.
        path, ext = os.path.splitext(fileName)
        ext = ext.lower()
        if not ext:
            ext = '.png'
            fileName = fileName + ext
        if ext == '.bmp':
            writer = vtk.vtkBMPWriter()
        elif ext == '.jpg':
            writer = vtk.vtkJPEGWriter()
        elif ext == '.pnm':
            writer = vtk.vtkPNMWriter()
        elif ext == '.ps':
            if rgba:
                rgba = False
            writer = vtk.vtkPostScriptWriter()
        elif ext == '.tiff':
            writer = vtk.vtkTIFFWriter()
        else:
            writer = vtk.vtkPNGWriter()
        windowto_image_filter = vtk.vtkWindowToImageFilter()
        windowto_image_filter.SetInput(renWin)
        windowto_image_filter.SetScale(1)  # image quality
        if rgba:
            windowto_image_filter.SetInputBufferTypeToRGBA()
        else:
            windowto_image_filter.SetInputBufferTypeToRGB()
            # Read from the front buffer.
            windowto_image_filter.ReadFrontBufferOff()
            windowto_image_filter.Update()

        writer.SetFileName(fileName)
        writer.SetInputConnection(windowto_image_filter.GetOutputPort())
        writer.Write()
    else:
        raise RuntimeError('Need a filename.')


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--srcdir", help="path to the model")
args = ap.parse_args()



reader = vtk.vtkSTLReader()
reader.SetFileName(args.srcdir)
reader.Update()
normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(reader.GetOutputPort())
print("Vertices in original model: "+ str(reader.GetOutput().GetNumberOfPoints()))


plane = vtk.vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(-1, -1, 0)

clipper = vtk.vtkClipPolyData()
clipper.SetInputConnection(normals.GetOutputPort())
clipper.SetClipFunction(plane)
clipper.GenerateClipScalarsOn()
clipper.GenerateClippedOutputOff()
clipper.SetValue(0)

clipper.Update()
print("Vertices in remaining part: "+ str(clipper.GetOutput().GetNumberOfPoints()))

clipper.SetInsideOut(True)
clipper.Update()
print("Vertices in clipped out part: "+ str(clipper.GetOutput().GetNumberOfPoints()))

clipper.GenerateClippedOutputOn()

clipMapper = vtk.vtkPolyDataMapper()
clipMapper.SetInputConnection(clipper.GetOutputPort())
clipMapper.ScalarVisibilityOff()
backProp = vtk.vtkProperty()
backProp.SetDiffuseColor(tomato)
clipActor = vtk.vtkActor()
clipActor.SetMapper(clipMapper)
clipActor.GetProperty().SetColor(brown_ochre)
clipActor.SetBackfaceProperty(backProp)


cutEdges = vtk.vtkCutter()
cutEdges.SetInputConnection(normals.GetOutputPort())
cutEdges.SetCutFunction(plane)
cutEdges.GenerateCutScalarsOn()
cutEdges.SetValue(0, 0)
cutEdges.Update()
cutStrips = vtk.vtkStripper()
cutStrips.SetInputConnection(cutEdges.GetOutputPort())
cutStrips.Update()
cutPoly = vtk.vtkPolyData()
cutPoly.SetPoints(cutStrips.GetOutput().GetPoints())
cutPoly.SetPolys(cutStrips.GetOutput().GetLines())
print("Vertices in intersection part part: "+ str(cutPoly.GetNumberOfPoints()))



cutTriangles = vtk.vtkTriangleFilter()
cutTriangles.SetInputData(cutPoly)
cutMapper = vtk.vtkPolyDataMapper()
cutMapper.SetInputData(cutPoly)
cutMapper.SetInputConnection(cutTriangles.GetOutputPort())
cutActor = vtk.vtkActor()
cutActor.SetMapper(cutMapper)
cutActor.GetProperty().SetColor(banana)

restMapper = vtk.vtkPolyDataMapper()
restMapper.SetInputData(clipper.GetClippedOutput())
restMapper.ScalarVisibilityOff()
restActor = vtk.vtkActor()
restActor.SetMapper(restMapper)
restActor.GetProperty().SetRepresentationToWireframe()

sample = vtk.vtkSampleFunction()
sample.SetImplicitFunction(plane)
sample.SetModelBounds(reader.GetOutput().GetBounds())
sample.SetSampleDimensions(40, 40, 40)
sample.ComputeNormalsOff()

# contour
surface = vtk.vtkContourFilter()
surface.SetInputConnection(sample.GetOutputPort())
surface.SetValue(0, 0.0)

# mapper
mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.ScalarVisibilityOff()
actor = vtk.vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(.2, .2, .5)

ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

ren.AddActor(clipActor)
ren.AddActor(cutActor)
ren.AddActor(restActor)
ren.AddActor(actor)

renWin.Render()

WriteImage("Screenshot.jpeg", renWin, False)

iren.Initialize()
iren.Start()