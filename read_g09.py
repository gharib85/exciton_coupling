""" Read and extracts information from gaussian 09 log files
"""
from periodic import element
import numpy as np
def get_xyz(g09_file):
    """
    Opens a g09 log file and returns the first geometry in Input orientation.
    Iterators are used so that the file is not all loaded into memory, which
    can be expensive.

    The function searches for the following text pattern in the log file:

                            Input orientation:
    ---------------------------------------------------------------------
    Center     Atomic      Atomic             Coordinates (Angstroms)
    Number     Number       Type             X           Y           Z
    ---------------------------------------------------------------------

    And will save the coordinates and the atomic symbols succeeding it

    Parameters
    ----------
    g09_file: Path to g09 log file
        File path

    Returns
    ----------
    coordinates: List of lists
        Outer list is whole xyz file, each inner list is a line of the file containing
        the symbol and x,y,z coordinates

    """
    with open(g09_file) as f:
        # Get the number of atoms so we can iterate without loading the file into memory
        for i,line in enumerate(f):
            # Ensures line is not blank
            if line.strip():
                if line.split()[0]=="NAtoms=":
                    natoms=(int(line.split()[3]))
                    break
        # Will hold the coordinates and symbols
        coordinates=[]
        # Reset the iterator to the top of the file
        f.seek(0)
        for i,line in enumerate(f):
            if line.strip():
                if "Input orientation:" in line:
                    for i in range(5):
                        # Skip 5 lines to start of coordinates
                        line=f.next()
                    for i in range(natoms):
                        linesplit=line.split()
                        symb=str(element(linesplit[1]).symbol)
                        x=float(linesplit[3])
                        y=float(linesplit[4])
                        z=float(linesplit[5])
                        coordinates.append([symb,x,y,z])
                        line=f.next()
                    break
                    f.close()
        return coordinates

def read_TD(g09_file,state):
    """
    Reads a G09 logfile and returns the Transition Dipole vector for the specified
    electronic state

    Parameters
    ----------
    g09_file: Path to g09 log file
        File path

    Returns
    ----------
    TD: np.array
        1x3 array of x,y,z components of TD vector
    """
    with open(g09_file) as f:
        # Get the number of atoms so we can iterate without loading the file into memory
        for i,line in enumerate(f):
            # Ensures line is not blank
            if line.strip():
                if " Ground to excited state transition electric dipole moments (Au):" in line:
                    for i in range(state+1):
                        line=f.next()
                    s,X,Y,Z,DipS,Osc = line.split()
                    break
        f.close()
        return np.array([float(X),float(Y),float(Z)])