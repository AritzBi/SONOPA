# compiled_pyke_files.py

from pyke import target_pkg

pyke_version = '1.1.1'
compiler_version = 1
target_pkg_version = 1

try:
    loader = __loader__
except NameError:
    loader = None

def get_target_pkg():
    return target_pkg.target_pkg(__name__, __file__, pyke_version, loader, {
         ('', '', 'rule_system.krb'):
           [1418815155.000727, 'rule_system_fc.py'],
         ('', '', 'sensor_data.kfb'):
           [1420621511.993821, 'sensor_data.fbc'],
        },
        compiler_version)

