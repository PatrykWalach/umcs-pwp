import subprocess
import sys




if __name__ == "__main__":


  
  try:
    path = sys.argv[1]
    out = subprocess.run(["dir", path], shell=True,stdout=subprocess.PIPE,text=True, stderr=subprocess.DEVNULL, check=True)
    
    print(out.stdout)
  except IndexError:
    print("Nie podana nazwa katalogu")
  except subprocess.CalledProcessError:
    print("Podana błędna nazwa katalogu")
