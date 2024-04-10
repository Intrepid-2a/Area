import numpy as np

def placeCurvatureDots(B, C, curvature):

    # B: coordinates of point B
    # C: coordinates of point C
    # curvature: the amount of curvature for the previous and next points

    # Assuming the time that passes between presentation of B and C
    # is equal to the time passing between A and B and between C and D
    # the location of A and D can be calculated, such that the 2 triplets 
    # of points have the specified curvature.

    # First, we need B to be lower on the screen than C:
    if B[1] > C[1]:
        B, C = C, B

    # Then, if the specified curvature is 0, this is a special case
    # for which the equation doesn't work and the points should lie on 
    # a straight line:

    if curvature == 0:
        A = [B[0] - (C[0]-B[0]), B[1] - (C[1]-B[1])]
        D = [C[0] + (C[0]-B[0]), C[1] + (C[1]-B[1])]
        # we return this result:
        return([A, B, C, D]),

    # If the curvature is not 0, we need to do some more work.

    # distance between B and C:
    dist = ((B[0] - C[0])**2 + (B[1] - C[1])**2)**0.5
    
    # the radius of the circle describing the curvature:
    R = 1 / np.abs(curvature)

    # The angle between two lines drawn through the origin
    # of the circle of curvature and the two points:
    ang_rad = 2 * ( (np.pi/2) - np.arccos( (dist/2) / R ) )

    # Get the angle in radians for all 4 points,
    # with B and C in the middle:
    point_angles = [ang_rad * x for x in [-1.5,-.5,.5,1.5]]
    
    # Now get the coordinates of the 4 points:
    # point_coords = [[np.cos(xa)*R, np.sin(xa)*R] for xa in point_angles]
    # in an array:
    point_coords = np.array([np.cos(point_angles)*R, np.sin(point_angles)*R]).T

    # Right now, the curvature is always toward fixation
    # but the relative placement is correct,
    # we just need to move things around a bit.

    # First we correct for our positive and negative curvature.
    # This does not really exist, we just define negative curvature
    # to mean 'away from fixation'.

    point_coords = point_coords - [R,0]
    if curvature < 0:
        point_coords[:,0] *= -1
    
    # Now we flip the points if the original B and C are to the left:
    if np.mean([B[0], C[0]]) < 0:
        point_coords[:,0] *= -1
    
    # Then we reposition the points such that the current B (2nd) point
    # is at [0,0]:
    point_coords -= point_coords[1,:]

    # We get the original and current angle of a line through the 2nd
    # and 3rd point:
    orig_ang = np.arctan2(C[1]-B[1], C[0]-B[0])
    curr_ang = np.arctan2(point_coords[2,1], point_coords[2,0])

    # Rotate the current points by the difference to match the input orientation:
    th = orig_ang - curr_ang
    Rm = np.array([[np.cos(th), -1*np.sin(th)],[np.sin(th),np.cos(th)]])
    point_coords = Rm @ point_coords.T

    # Translate such that the second and third point match the input locations:
    point_coords = point_coords.T + B

    # That should be all, so we return all 4 coordinates:
    return(point_coords)


