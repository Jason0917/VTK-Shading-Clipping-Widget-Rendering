import vtk

reader = vtk.vtkSTLReader()
#reader.SetFileName("Charmander.stl")
reader.SetFileName("teapot.stl")

# sphere = vtk.vtkSphereSource()
# sphere.SetThetaResolution(60)
# sphere.SetPhiResolution(60)

# arrow = vtk.vtkArrowSource()
# arrow.SetTipResolution(60)
# arrow.SetShaftResolution(60)

mapper1 = vtk.vtkPolyDataMapper()
mapper2 = vtk.vtkPolyDataMapper()
mapper3 = vtk.vtkPolyDataMapper()
mapper4 = vtk.vtkPolyDataMapper()
actor1 = vtk.vtkActor()
actor2 = vtk.vtkActor()
actor3 = vtk.vtkActor()
actor4 = vtk.vtkActor()
ren1 = vtk.vtkRenderer()
ren2 = vtk.vtkRenderer()
ren3 = vtk.vtkRenderer()
ren4 = vtk.vtkRenderer()

# Compute normals
normals = vtk.vtkPolyDataNormals()
normals.SetInputConnection(reader.GetOutputPort())

# VTK pipeline for mapper and actor
mapper1.SetInputConnection(normals.GetOutputPort())
mapper2.SetInputConnection(normals.GetOutputPort())
mapper3.SetInputConnection(normals.GetOutputPort())
mapper4.SetInputConnection(normals.GetOutputPort())
actor1.SetMapper(mapper1)
actor2.SetMapper(mapper2)
actor3.SetMapper(mapper3)
actor4.SetMapper(mapper4)

# actor.GetProperty().SetColor(1,1,0)

ren1.AddActor(actor1)
ren1.SetViewport(0, 0.5, 0.5, 1.0)
ren2.AddActor(actor2)
ren2.SetViewport(0.5, 0.5, 1.0, 1.0)
ren3.AddActor(actor3)
ren3.SetViewport(0, 0, 0.5, 0.5)
ren4.AddActor(actor4)
ren4.SetViewport(0.5, 0, 1.0, 0.5)

# Set object properties
prop1 = actor1.GetProperty()
# prop.SetInterpolationToFlat() # Set shading to Flat
# prop.ShadingOn()
prop1.SetColor(1, 1, 0)
prop1.SetDiffuse(0.8)  # 0.8
prop1.SetAmbient(0.3)  # 0.3
prop1.SetSpecular(1.0)  # 1.0
prop1.SetSpecularPower(100.0)

prop2 = actor2.GetProperty()
prop2.SetInterpolationToGouraud()  # Set shading to Flat
prop2.ShadingOn()
prop2.SetColor(1, 1, 0)
prop2.SetDiffuse(0.8)  # 0.8
prop2.SetAmbient(0.3)  # 0.3
prop2.SetSpecular(1.0)  # 1.0
prop2.SetSpecularPower(100.0)

prop3 = actor3.GetProperty()
prop3.SetInterpolationToFlat()  # Set shading to Flat
prop3.ShadingOn()
prop3.SetColor(1, 1, 0)
prop3.SetDiffuse(0.8)  # 0.8
prop3.SetAmbient(0.3)  # 0.3
prop3.SetSpecular(1.0)  # 1.0
prop3.SetSpecularPower(100.0)

prop4 = actor4.GetProperty()
prop4.SetInterpolationToPhong()  # Set shading to Flat
prop4.ShadingOn()
prop4.SetColor(1, 1, 0)
prop4.SetDiffuse(0.8)  # 0.8
prop4.SetAmbient(0.3)  # 0.3
prop4.SetSpecular(1.0)  # 1.0
prop4.SetSpecularPower(100.0)

# Define light
light = vtk.vtkLight()
light.SetLightTypeToSceneLight()
light.SetAmbientColor(1, 1, 1)
light.SetDiffuseColor(1, 1, 1)
light.SetSpecularColor(1, 1, 1)
light.SetPosition(-100, 100, 25)
light.SetFocalPoint(0, 0, 0)
light.SetIntensity(0.8)

# Add the light to the renderer
ren1.AddLight(light)
ren2.AddLight(light)
ren3.AddLight(light)
ren4.AddLight(light)

renWin = vtk.vtkRenderWindow()
renWin.SetSize(800, 800)

renWin.AddRenderer(ren1)
renWin.AddRenderer(ren2)
renWin.AddRenderer(ren3)
renWin.AddRenderer(ren4)

iren = vtk.vtkRenderWindowInteractor()
iren.SetInteractorStyle(vtk.vtkInteractorStyleTrackballActor())

iren.SetRenderWindow(renWin)

renWin.Render()
iren.Initialize()
iren.Start()
