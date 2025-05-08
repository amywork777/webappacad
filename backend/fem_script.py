def fem_py(step_path: str, force=100):
    return f"""
import FreeCAD, Import, ObjectsFem
from femtools import ccxtools
doc=FreeCAD.newDocument(); Import.insert('{step_path}',doc.Name)
mat=ObjectsFem.makeMaterialSolid('Mat'); mat.Material={{'Name':'PLA','YoungsModulus':2e9,'PoissonRatio':0.35}}
analysis=ObjectsFem.makeAnalysis(doc,'Analysis'); analysis.addObject(mat)
fix=ObjectsFem.makeConstraintFixed('Fix',analysis); fix.References=[(doc.Objects[0],('Face1',))]
load=ObjectsFem.makeConstraintForce('Load',analysis); load.References=[(doc.Objects[0],('Face2',))]; load.Force={force}
solver=ObjectsFem.makeSolverCalculixCcxTools('Solver',analysis)
ccx=ccxtools.CalculiXTools(doc,analysis,solver); ccx.fea_write_inp_file(); ccx.solver.run(); ccx.load_results()
ccx.export_vtk('{step_path}.vtk')
"""