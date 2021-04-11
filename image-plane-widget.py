import vtk
import colorsys

dir_ = r"CT"

# Read data
reader = vtk.vtkDICOMImageReader()
reader.SetDirectoryName(dir_)
reader.Update()

W,H,D = reader.GetOutput().GetDimensions()
X,Y,Z = reader.GetOutput().GetSpacing()
A,B = reader.GetOutput().GetScalarRange()
print("Dimension", W,H,D)
print("Voxel resolution",X,Y,Z)
print("Intensities",A,B)

# Create colour transfer function
colorFunc = vtk.vtkColorTransferFunction()
colorFunc.AddRGBPoint(-3024, 0.0, 0.0, 0.0)
colorFunc.AddRGBPoint(-77, 0.54902, 0.25098, 0.14902)
colorFunc.AddRGBPoint(94, 0.882353, 0.603922, 0.290196)
colorFunc.AddRGBPoint(179, 1, 0.937033, 0.954531)
colorFunc.AddRGBPoint(260, 0.615686, 0, 0)
colorFunc.AddRGBPoint(3071, 0.827451, 0.658824, 1)

# Create opacity transfer function
alphaChannelFunc = vtk.vtkPiecewiseFunction()
alphaChannelFunc.AddPoint(-3024, 0.0)
alphaChannelFunc.AddPoint(-77, 0.0)
alphaChannelFunc.AddPoint(94, 0.29)
alphaChannelFunc.AddPoint(179, 0.55)
alphaChannelFunc.AddPoint(260, 0.84)
alphaChannelFunc.AddPoint(3071, 0.875)

# Instantiate necessary classes and create VTK pipeline
volume = vtk.vtkVolume()
ren = vtk.vtkRenderer()
ren.SetViewport(0, 0, 0.5, 1)
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(ren)
iren = vtk.vtkRenderWindowInteractor()
iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
iren.SetRenderWindow(renWin)
renWin.SetSize(800, 800)

# Define volume mapper
volumeMapper = vtk.vtkSmartVolumeMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())

# Define volume properties
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetScalarOpacity(alphaChannelFunc)
volumeProperty.SetColor(colorFunc)
volumeProperty.ShadeOn()

# Set the mapper and volume properties
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

# Define volume mapper
volumeMapper = vtk.vtkSmartVolumeMapper()
volumeMapper.SetInputConnection(reader.GetOutputPort())

# Define volume properties
volumeProperty = vtk.vtkVolumeProperty()
volumeProperty.SetScalarOpacity(alphaChannelFunc)
volumeProperty.SetColor(colorFunc)
volumeProperty.ShadeOn()

# Set the mapper and volume properties
volume.SetMapper(volumeMapper)
volume.SetProperty(volumeProperty)

# Add volume to renderer
ren.AddVolume(volume)

RGB_tuples = [(1, 0, 0), (0, 1, 0), (0, 0, 1)]  # define colors for plane outline

# Define look up table for displaying the data
table = vtk.vtkLookupTable()
table.SetRange(-1000, 3072)
table.SetRampToLinear()
table.SetValueRange(0, 1)
table.SetHueRange(0.0, 1.0)
table.SetSaturationRange(0.0, 0.0)

mapToColors = vtk.vtkImageMapToColors()
mapToColors.SetInputConnection(reader.GetOutputPort())
mapToColors.SetLookupTable(table)
mapToColors.Update()

# A picker is used to get information about the volume
picker = vtk.vtkCellPicker()
picker.SetTolerance(0.005)

# Define plane widgets for x, y and z
planeWidgetX, planeWidgetY, planeWidgetZ = [vtk.vtkImagePlaneWidget() for i in range(3)]

# Set plane properties
for plane, axtext, wgtcolor, ind in zip((planeWidgetX, planeWidgetY, planeWidgetZ), ("x", "y", "z"),
                                        ((0.5, 0, 0.5), (0.5, 0.5, 0), (0, 0.5, 0.5)), range(3)):
    plane.SetInputConnection(reader.GetOutputPort())
    plane.SetPlaneOrientation(ind)
    plane.DisplayTextOn()
    plane.SetSliceIndex(100)
    plane.SetPicker(picker)
    plane.SetLookupTable(table)
    plane.SetColorMap(mapToColors)
    plane.SetKeyPressActivationValue(axtext)
    prop = plane.GetPlaneProperty()
    prop.SetColor(RGB_tuples[ind])

# Place plane widget and set interactor
for plane in (planeWidgetX, planeWidgetY, planeWidgetZ):
    plane.SetCurrentRenderer(ren)
    plane.SetInteractor(iren)
    plane.PlaceWidget()
    plane.On()

# create VTK pipeline
ren2 = vtk.vtkRenderer()
imageActor2 = vtk.vtkImageActor()
ren2.SetViewport(0.5, 0.5, 1.0, 1.0)

renWin.Render()

# Create histogram object
histogram = vtk.vtkImageAccumulate()
histogram.SetComponentExtent(0, 255, 0, 0, 0, 0)
histogram.SetComponentOrigin(0, 0, 0)
histogram.SetComponentSpacing(1, 0, 0)
histogram.IgnoreZeroOff()

def GetSample(obj, ev):
    # Get the observed plane and bind it
    planeX = GetSample.planeX
    imageActor2.SetInputData(planeX.GetResliceOutput())
    ren2.AddActor(imageActor2)
    renWin.AddRenderer(ren2)

    # Set the number of scalar components to 3,
    # otherwise vtkImageAccumulate can't process it.
    # planeX.GetResliceOutput().AllocateScalars(vtk.VTK_INT, 3)

    # Set the input data for histogram
    histogram.SetInputData(planeX.GetResliceOutput())
    histogram.Update()

    # Construct an array to store the histogram
    red = [1, 0, 0]
    frequencies = vtk.vtkIntArray()
    frequencies.SetNumberOfComponents(1)
    frequencies.SetNumberOfTuples(256)
    o = histogram.GetOutput()
    output = o.GetPointData().GetScalars()
    j = 0
    while j < 256:
        frequencies.SetTuple1(j, output.GetValue(j))
        j = j + 1

    # Convert the array to vtkDataObject
    dataObject = vtk.vtkDataObject()

    dataObject.GetFieldData().AddArray(frequencies)

    # Create a barChart to display the histogram
    barChart = vtk.vtkBarChartActor()

    barChart.SetInput(dataObject)
    barChart.SetTitle("Histogram")
    barChart.GetPositionCoordinate().SetValue(0.05, 0.05, 0.0)
    barChart.GetPosition2Coordinate().SetValue(0.95, 0.85, 0.0)
    barChart.GetProperty().SetColor(1, 1, 1)
    barChart.GetLegendActor().SetNumberOfEntries(dataObject.GetFieldData().GetArray(0).GetNumberOfTuples())
    barChart.LegendVisibilityOff()
    barChart.LabelVisibilityOff()

    count = 0
    while count < 256:
        barChart.SetBarColor(count, red)
        count += 1

    # Visualize the histogram
    ren3 = vtk.vtkRenderer()
    ren3.SetViewport(0.5, 0, 1.0, 0.5)
    ren3.AddActor(barChart)
    renWin.AddRenderer(ren3)


# Setup the mouse event observer
GetSample.planeX = planeWidgetX
iren.AddObserver('EndInteractionEvent', GetSample)


iren.Start()
