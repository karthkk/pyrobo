from numpy import pi, mat, cos, sin, zeros, eye, array
from numpy.core import concatenate


def rotx(theta):
    """
    Rotation about X-axis

    @type theta: number
    @param theta: the rotation angle
    @rtype: 3x3 orthonormal matrix
    @return: rotation about X-axis

    @see: L{roty}, L{rotz}, L{rotvec}
    """

    ct = cos(theta)
    st = sin(theta)
    return mat([[1,  0,    0],
            [0,  ct, -st],
            [0,  st,  ct]])

def roty(theta):
    """
    Rotation about Y-axis

    @type theta: number
    @param theta: the rotation angle
    @rtype: 3x3 orthonormal matrix
    @return: rotation about Y-axis

    @see: L{rotx}, L{rotz}, L{rotvec}
    """

    ct = cos(theta)
    st = sin(theta)

    return mat([[ct,   0,   st],
            [0,    1,    0],
            [-st,  0,   ct]])

def rotz(theta):
    """
    Rotation about Z-axis

    @type theta: number
    @param theta: the rotation angle
    @rtype: 3x3 orthonormal matrix
    @return: rotation about Z-axis

    @see: L{rotx}, L{roty}, L{rotvec}
    """

    ct = cos(theta)
    st = sin(theta)

    return mat([[ct,      -st,  0],
            [st,       ct,  0],
            [ 0,    0,  1]])

def trotx(theta):
    """
    Rotation about X-axis

    @type theta: number
    @param theta: the rotation angle
    @rtype: 4x4 homogeneous matrix
    @return: rotation about X-axis

    @see: L{troty}, L{trotz}, L{rotx}
    """
    return r2t(rotx(theta))

def troty(theta):
    """
    Rotation about Y-axis

    @type theta: number
    @param theta: the rotation angle
    @rtype: 4x4 homogeneous matrix
    @return: rotation about Y-axis

    @see: L{troty}, L{trotz}, L{roty}
    """
    return r2t(roty(theta))

def trotz(theta):
    """
    Rotation about Z-axis

    @type theta: number
    @param theta: the rotation angle
    @rtype: 4x4 homogeneous matrix
    @return: rotation about Z-axis

    @see: L{trotx}, L{troty}, L{rotz}
    """
    return r2t(rotz(theta))


##################### Euler ang
def transl(x, y=None, z=None):
    """
    Create or decompose translational homogeneous transformations.

    Create a homogeneous transformation
    ===================================

        - T = transl(v)
        - T = transl(vx, vy, vz)

        The transformation is created with a unit rotation submatrix.
        The translational elements are set from elements of v which is
        a list, array or matrix, or from separate passed elements.

    Decompose a homogeneous transformation
    ======================================


        - v = transl(T)

        Return the translation vector
    """

    if y==None and z==None:
            x=mat(x)
            try:
                    if ishomog(x):
                            return x[0:3,3].reshape(3,1)
                    else:
                            return concatenate((concatenate((eye(3),x.reshape(3,1)),1),mat([0,0,0,1])))
            except AttributeError:
                    n=len(x)
                    r = [[],[],[]]
                    for i in range(n):
                            r = concatenate((r,x[i][0:3,3]),1)
                    return r
    elif y!=None and z!=None:
            return concatenate((concatenate((eye(3),mat([x,y,z]).T),1),mat([0,0,0,1])))

def r2t(R):
    """
    Convert a 3x3 orthonormal rotation matrix to a 4x4 homogeneous transformation::

        T = | R 0 |
            | 0 1 |

    @type R: 3x3 orthonormal rotation matrix
    @param R: the rotation matrix to convert
    @rtype: 4x4 homogeneous matrix
    @return: homogeneous equivalent
    """

    return concatenate( (concatenate( (R, zeros((3,1))),1), mat([0,0,0,1])) )


Tz = lambda z: transl(x=0, y=0, z=z)
Ty = lambda y: transl(x=0, y=y, z=0)
Tx = lambda x: transl(x=x, y=0, z=0)
Rx = lambda x: trotx(x)
Ry = lambda y: troty(y)
Rz = lambda z: trotz(z)
