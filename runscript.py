

import sys
import imp
from opptimizer import *

#sys.path.append("../..")

def main(argv):

    print("runscript.py")
    print("argv:" + str(argv))

    scriptfile = argv[1]
    print('scriptfile:' + str(scriptfile))
      
    scriptname = oppval('script', argv[2])
    print('scriptname:' + scriptname)
       
    script = imp.load_source(scriptname, scriptfile)
    scobj = script.getScript()
    scobj.init(argv)
    scobj.execute(argv)
    
   
if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
