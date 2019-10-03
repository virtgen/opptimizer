

import sys
import imp

#sys.path.append("../..")

def main(argv):

   print("runscript.py")
   script = imp.load_source("script", "test.py")
   script.execute()
   
if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
