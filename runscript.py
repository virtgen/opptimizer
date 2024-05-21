import sys
import importlib.util
from opptimizer import *

#sys.path.append("../..")

def main(argv):

    print("runscript.py")
    print("argv:" + str(argv))

    scriptfile = argv[1]
    print('scriptfile:' + str(scriptfile))
      
    scriptname = oppval('script', argv[2])
    print('scriptname:' + scriptname)
       

    # Load the script dynamically using importlib
    spec = importlib.util.spec_from_file_location(scriptname, scriptfile)
    script = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(script)

    scobj = script.getScript()
    scobj.init(argv)
    scobj.execute(argv)
    
   
if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
