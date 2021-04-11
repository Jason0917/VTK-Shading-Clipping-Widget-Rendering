import vtk

sphere = vtk.vtkSphereSource()
sphere.SetThetaResolution(50)
sphere.SetPhiResolution(50)
sphere.SetRadius(1.0)
mapper = vtk.vtkPolyDataMapper()
actor = vtk.vtkActor()
ren = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
iren = vtk.vtkRenderWindowInteractor()

mapper.SetInputConnection(sphere.GetOutputPort())
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToWireframe()

ren.AddActor(actor)
renWin.AddRenderer(ren)
iren.SetRenderWindow(renWin)

def slider_callback(obj, evt):
    global sphere, actor
    value = obj.GetRepresentation().GetValue()
    sphere.SetRadius(value)
    actor.Modified()

sliderRep = vtk.vtkSliderRepresentation2D()
sliderWidget = vtk.vtkSliderWidget()

sliderRep.SetMinimumValue(0.0)
sliderRep.SetMaximumValue(3.0)
sliderRep.SetValue(1)
sliderRep.SetTitleText("Radius")
sliderRep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint1Coordinate().SetValue(0.1,0.1)
sliderRep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
sliderRep.GetPoint2Coordinate().SetValue(0.9, 0.1)
sliderRep.SetSliderLength(0.05)
sliderRep.SetSliderWidth(0.02)
sliderRep.SetEndCapLength(0.002)

sliderWidget.SetInteractor(iren)
sliderWidget.SetRepresentation(sliderRep)
sliderWidget.EnabledOn()
sliderWidget.AddObserver("InteractionEvent", slider_callback)

renWin.Render()
iren.Initialize()
iren.Start()