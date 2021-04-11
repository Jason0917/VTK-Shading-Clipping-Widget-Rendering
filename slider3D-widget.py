import vtk

sphere = vtk.vtkSphereSource()
sphere.SetThetaResolution(50)
sphere.SetPhiResolution(50)
sphere.SetRadius(10.0)
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

sliderRep = vtk.vtkSliderRepresentation3D()
sliderWidget = vtk.vtkSliderWidget()

sliderRep.SetMinimumValue(0.0)
sliderRep.SetMaximumValue(10.0)
sliderRep.SetValue(10)
sliderRep.SetTitleText("Radius")
sliderRep.GetPoint1Coordinate().SetCoordinateSystemToWorld()
sliderRep.GetPoint1Coordinate().SetValue(-8,-15,0)
sliderRep.GetPoint2Coordinate().SetCoordinateSystemToWorld()
sliderRep.GetPoint2Coordinate().SetValue(8,-15,0)

sliderWidget.SetInteractor(iren)
sliderWidget.SetRepresentation(sliderRep)
sliderWidget.SetAnimationModeToAnimate()
sliderWidget.EnabledOn()
sliderWidget.AddObserver("InteractionEvent", slider_callback)

renWin.Render()
iren.Initialize()
iren.Start()