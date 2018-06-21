from numpy import ones,vstack
from numpy.linalg import lstsq
import numpy as np

def draw_ground(img, lines, color=[0, 255, 255], thickness=3):

    # if this fails, go with some default line
    try:

        # finds the maximum y value for a ground marker
        # (since we cannot assume the horizon will always be at the same point.)

        ys = []
        for i in lines:
            for ii in i:
                ys += [ii[1],ii[3]]
        min_y = min(ys)
        max_y = 500
        new_lines = []
        line_dict = {}

        for idx,i in enumerate(lines):
            for xyxy in i:
                # These four lines:
                # modified from http://stackoverflow.com/questions/21565994/method-to-return-the-equation-of-a-straight-line-given-two-points
                # Used to calculate the definition of a line, given two sets of coords.
                x_coords = (xyxy[0],xyxy[2])
                y_coords = (xyxy[1],xyxy[3])
                A = vstack([x_coords,ones(len(x_coords))]).T
                m, b = lstsq(A, y_coords)[0]

                # Calculating our new, and improved, xs
                x1 = (min_y-b) / m
                x2 = (max_y-b) / m

                line_dict[idx] = [m,b,[int(x1), min_y, int(x2), max_y]]
                new_lines.append([int(x1), min_y, int(x2), max_y])

        final_ground = {}

        for idx in line_dict:
            final_ground_copy = final_ground.copy()
            m = line_dict[idx][0]
            b = line_dict[idx][1]
            line = line_dict[idx][2]

            if len(final_ground) == 0:
                final_ground[m] = [ [m,b,line] ]

            else:
                found_copy = False

                for other_ms in final_ground_copy:

                    if not found_copy:
                        if abs(other_ms*1.2) > abs(m) > abs(other_ms*0.8):
                            if abs(final_ground_copy[other_ms][0][1]*1.2) > abs(b) > abs(final_ground_copy[other_ms][0][1]*0.8):
                                final_ground[other_ms].append([m,b,line])
                                found_copy = True
                                break
                        else:
                            final_ground[m] = [ [m,b,line] ]

        line_counter = {}

        for ground in final_ground:
            line_counter[ground] = len(final_ground[ground])

        top_ground = sorted(line_counter.items(), key=lambda item: item[1])[::-1][:2]

        ground1_id = top_ground[0][0]
        ground2_id = top_ground[1][0]

        def average_ground(ground_data):
            x1s = []
            y1s = []
            x2s = []
            y2s = []
            for data in ground_data:
                x1s.append(data[2][0])
                y1s.append(data[2][1])
                x2s.append(data[2][2])
                y2s.append(data[2][3])
            return int(np.mean(x1s)), int(np.mean(y1s)), int(np.mean(x2s)), int(np.mean(y2s))

        l1_x1, l1_y1, l1_x2, l1_y2 = average_ground(final_ground[ground1_id])
        l2_x1, l2_y1, l2_x2, l2_y2 = average_ground(final_ground[ground2_id])

        return [l1_x1, l1_y1, l1_x2, l1_y2], [l2_x1, l2_y1, l2_x2, l2_y2], ground1_id, ground2_id
    except Exception as e:
        print(str(e))
