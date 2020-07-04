from tinypy.generated.trees.generated_tree import GeneratedTree

from tinypy.geometry.point import Point


class TSPTree(GeneratedTree):

    def __init__(self, polytope):
        self.polytope = polytope
        self.hyperplanes = polytope.H

    def test(self, point: Point):
        if self.hyperplanes[1].in_halfspace(point):
            if self.hyperplanes[8].in_halfspace(point):
                if self.hyperplanes[3].in_halfspace(point):
                    if self.hyperplanes[4].in_halfspace(point):
                        if self.hyperplanes[2].in_halfspace(point):
                            if self.hyperplanes[23].in_halfspace(point):
                                return 12, 13, 6
                            else:
                                return 6, 12, 6
                        else:
                            if self.hyperplanes[16].in_halfspace(point):
                                if self.hyperplanes[15].in_halfspace(point):
                                    return 12, 17, 7
                                else:
                                    return 7, 16, 7
                            else:
                                if self.hyperplanes[25].in_halfspace(point):
                                    return 12, 19, 7
                                else:
                                    return 5, 18, 7
                    else:
                        if self.hyperplanes[5].in_halfspace(point):
                            if self.hyperplanes[23].in_halfspace(point):
                                return 12, 23, 6
                            else:
                                return 6, 22, 6
                        else:
                            if self.hyperplanes[18].in_halfspace(point):
                                if self.hyperplanes[13].in_halfspace(point):
                                    return 12, 27, 7
                                else:
                                    return 8, 26, 7
                            else:
                                if self.hyperplanes[27].in_halfspace(point):
                                    return 12, 29, 7
                                else:
                                    return 4, 28, 7
                else:
                    if self.hyperplanes[6].in_halfspace(point):
                        if self.hyperplanes[16].in_halfspace(point):
                            if self.hyperplanes[5].in_halfspace(point):
                                if self.hyperplanes[11].in_halfspace(point):
                                    return 12, 37, 7
                                else:
                                    return 9, 36, 7
                            else:
                                if self.hyperplanes[15].in_halfspace(point):
                                    return 12, 39, 7
                                else:
                                    return 7, 38, 7
                        else:
                            if self.hyperplanes[18].in_halfspace(point):
                                if self.hyperplanes[11].in_halfspace(point):
                                    return 12, 43, 7
                                else:
                                    return 9, 42, 7
                            else:
                                if self.hyperplanes[25].in_halfspace(point):
                                    return 12, 45, 7
                                else:
                                    return 5, 44, 7
                    else:
                        if self.hyperplanes[19].in_halfspace(point):
                            if self.hyperplanes[15].in_halfspace(point):
                                return 12, 49, 6
                            else:
                                return 7, 48, 6
                        else:
                            if self.hyperplanes[29].in_halfspace(point):
                                return 12, 51, 6
                            else:
                                return 3, 50, 6
            else:
                if self.hyperplanes[10].in_halfspace(point):
                    if self.hyperplanes[4].in_halfspace(point):
                        if self.hyperplanes[2].in_halfspace(point):
                            if self.hyperplanes[19].in_halfspace(point):
                                if self.hyperplanes[9].in_halfspace(point):
                                    return 12, 61, 7
                                else:
                                    return 10, 60, 7
                            else:
                                if self.hyperplanes[23].in_halfspace(point):
                                    return 12, 63, 7
                                else:
                                    return 6, 62, 7
                        else:
                            if self.hyperplanes[16].in_halfspace(point):
                                if self.hyperplanes[15].in_halfspace(point):
                                    return 12, 67, 7
                                else:
                                    return 7, 66, 7
                            else:
                                if self.hyperplanes[25].in_halfspace(point):
                                    return 12, 69, 7
                                else:
                                    return 5, 68, 7
                    else:
                        if self.hyperplanes[5].in_halfspace(point):
                            if self.hyperplanes[19].in_halfspace(point):
                                if self.hyperplanes[9].in_halfspace(point):
                                    return 12, 75, 7
                                else:
                                    return 10, 74, 7
                            else:
                                if self.hyperplanes[23].in_halfspace(point):
                                    return 12, 77, 7
                                else:
                                    return 6, 76, 7
                        else:
                            if self.hyperplanes[18].in_halfspace(point):
                                if self.hyperplanes[6].in_halfspace(point):
                                    if self.hyperplanes[9].in_halfspace(point):
                                        return 12, 83, 8
                                    else:
                                        return 10, 82, 8
                                else:
                                    if self.hyperplanes[13].in_halfspace(point):
                                        return 12, 85, 8
                                    else:
                                        return 8, 84, 8
                            else:
                                if self.hyperplanes[21].in_halfspace(point):
                                    if self.hyperplanes[9].in_halfspace(point):
                                        return 12, 89, 8
                                    else:
                                        return 10, 88, 8
                                else:
                                    if self.hyperplanes[27].in_halfspace(point):
                                        return 12, 91, 8
                                    else:
                                        return 4, 90, 8
                else:
                    if self.hyperplanes[12].in_halfspace(point):
                        if self.hyperplanes[2].in_halfspace(point):
                            if self.hyperplanes[19].in_halfspace(point):
                                return 10, 97, 6
                            else:
                                return 6, 96, 6
                        else:
                            if self.hyperplanes[16].in_halfspace(point):
                                if self.hyperplanes[5].in_halfspace(point):
                                    if self.hyperplanes[3].in_halfspace(point):
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 12, 105, 9
                                        else:
                                            return 10, 104, 9
                                    else:
                                        if self.hyperplanes[11].in_halfspace(point):
                                            return 12, 107, 9
                                        else:
                                            return 9, 106, 9
                                else:
                                    if self.hyperplanes[15].in_halfspace(point):
                                        return 12, 109, 8
                                    else:
                                        return 7, 108, 8
                            else:
                                if self.hyperplanes[18].in_halfspace(point):
                                    if self.hyperplanes[3].in_halfspace(point):
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 12, 115, 9
                                        else:
                                            return 10, 114, 9
                                    else:
                                        if self.hyperplanes[11].in_halfspace(point):
                                            return 12, 117, 9
                                        else:
                                            return 9, 116, 9
                                else:
                                    if self.hyperplanes[20].in_halfspace(point):
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 12, 121, 9
                                        else:
                                            return 10, 120, 9
                                    else:
                                        if self.hyperplanes[25].in_halfspace(point):
                                            return 12, 123, 9
                                        else:
                                            return 5, 122, 9
                    else:
                        if self.hyperplanes[14].in_halfspace(point):
                            if self.hyperplanes[16].in_halfspace(point):
                                if self.hyperplanes[4].in_halfspace(point):
                                    if self.hyperplanes[3].in_halfspace(point):
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 12, 133, 9
                                        else:
                                            return 10, 132, 9
                                    else:
                                        return 9, 130, 8
                                else:
                                    if self.hyperplanes[6].in_halfspace(point):
                                        return 10, 135, 8
                                    else:
                                        return 8, 134, 8
                            else:
                                if self.hyperplanes[17].in_halfspace(point):
                                    if self.hyperplanes[3].in_halfspace(point):
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 12, 141, 9
                                        else:
                                            return 10, 140, 9
                                    else:
                                        return 9, 138, 8
                                else:
                                    if self.hyperplanes[19].in_halfspace(point):
                                        return 10, 143, 8
                                    else:
                                        return 6, 142, 8
                        else:
                            if self.hyperplanes[22].in_halfspace(point):
                                if self.hyperplanes[7].in_halfspace(point):
                                    return 10, 147, 7
                                else:
                                    return 7, 146, 7
                            else:
                                if self.hyperplanes[28].in_halfspace(point):
                                    return 10, 149, 7
                                else:
                                    return 2, 148, 7
        else:
            if self.hyperplanes[9].in_halfspace(point):
                if self.hyperplanes[3].in_halfspace(point):
                    if self.hyperplanes[5].in_halfspace(point):
                        if self.hyperplanes[22].in_halfspace(point):
                            return 11, 157, 5
                        else:
                            return 6, 156, 5
                    else:
                        if self.hyperplanes[18].in_halfspace(point):
                            if self.hyperplanes[12].in_halfspace(point):
                                return 11, 161, 6
                            else:
                                return 8, 160, 6
                        else:
                            if self.hyperplanes[26].in_halfspace(point):
                                return 11, 163, 6
                            else:
                                return 4, 162, 6
                else:
                    if self.hyperplanes[6].in_halfspace(point):
                        if self.hyperplanes[2].in_halfspace(point):
                            if self.hyperplanes[22].in_halfspace(point):
                                return 11, 169, 6
                            else:
                                return 6, 168, 6
                        else:
                            if self.hyperplanes[18].in_halfspace(point):
                                if self.hyperplanes[10].in_halfspace(point):
                                    return 11, 173, 7
                                else:
                                    return 9, 172, 7
                            else:
                                if self.hyperplanes[24].in_halfspace(point):
                                    return 11, 175, 7
                                else:
                                    return 5, 174, 7
                    else:
                        if self.hyperplanes[7].in_halfspace(point):
                            if self.hyperplanes[16].in_halfspace(point):
                                if self.hyperplanes[4].in_halfspace(point):
                                    if self.hyperplanes[10].in_halfspace(point):
                                        return 11, 183, 8
                                    else:
                                        return 9, 182, 8
                                else:
                                    if self.hyperplanes[12].in_halfspace(point):
                                        return 11, 185, 8
                                    else:
                                        return 8, 184, 8
                            else:
                                if self.hyperplanes[17].in_halfspace(point):
                                    if self.hyperplanes[10].in_halfspace(point):
                                        return 11, 189, 8
                                    else:
                                        return 9, 188, 8
                                else:
                                    if self.hyperplanes[22].in_halfspace(point):
                                        return 11, 191, 8
                                    else:
                                        return 6, 190, 8
                        else:
                            if self.hyperplanes[19].in_halfspace(point):
                                if self.hyperplanes[14].in_halfspace(point):
                                    return 11, 195, 7
                                else:
                                    return 7, 194, 7
                            else:
                                if self.hyperplanes[28].in_halfspace(point):
                                    return 11, 197, 7
                                else:
                                    return 3, 196, 7
            else:
                if self.hyperplanes[11].in_halfspace(point):
                    if self.hyperplanes[4].in_halfspace(point):
                        if self.hyperplanes[2].in_halfspace(point):
                            if self.hyperplanes[19].in_halfspace(point):
                                if self.hyperplanes[8].in_halfspace(point):
                                    return 11, 207, 7
                                else:
                                    return 10, 206, 7
                            else:
                                if self.hyperplanes[22].in_halfspace(point):
                                    return 11, 209, 7
                                else:
                                    return 6, 208, 7
                        else:
                            if self.hyperplanes[16].in_halfspace(point):
                                return 7, 211, 6
                            else:
                                return 5, 210, 6
                    else:
                        if self.hyperplanes[5].in_halfspace(point):
                            if self.hyperplanes[16].in_halfspace(point):
                                if self.hyperplanes[6].in_halfspace(point):
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 11, 219, 8
                                    else:
                                        return 10, 218, 8
                                else:
                                    if self.hyperplanes[12].in_halfspace(point):
                                        return 11, 221, 8
                                    else:
                                        return 8, 220, 8
                            else:
                                if self.hyperplanes[19].in_halfspace(point):
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 11, 225, 8
                                    else:
                                        return 10, 224, 8
                                else:
                                    if self.hyperplanes[22].in_halfspace(point):
                                        return 11, 227, 8
                                    else:
                                        return 6, 226, 8
                        else:
                            if self.hyperplanes[18].in_halfspace(point):
                                return 8, 229, 6
                            else:
                                return 4, 228, 6
                else:
                    if self.hyperplanes[15].in_halfspace(point):
                        if self.hyperplanes[16].in_halfspace(point):
                            if self.hyperplanes[4].in_halfspace(point):
                                if self.hyperplanes[3].in_halfspace(point):
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 11, 239, 8
                                    else:
                                        return 10, 238, 8
                                else:
                                    if self.hyperplanes[10].in_halfspace(point):
                                        return 11, 241, 8
                                    else:
                                        return 9, 240, 8
                            else:
                                if self.hyperplanes[6].in_halfspace(point):
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 11, 245, 8
                                    else:
                                        return 10, 244, 8
                                else:
                                    if self.hyperplanes[12].in_halfspace(point):
                                        return 11, 247, 8
                                    else:
                                        return 8, 246, 8
                        else:
                            if self.hyperplanes[17].in_halfspace(point):
                                if self.hyperplanes[3].in_halfspace(point):
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 11, 253, 8
                                    else:
                                        return 10, 252, 8
                                else:
                                    if self.hyperplanes[10].in_halfspace(point):
                                        return 11, 255, 8
                                    else:
                                        return 9, 254, 8
                            else:
                                if self.hyperplanes[19].in_halfspace(point):
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 11, 259, 8
                                    else:
                                        return 10, 258, 8
                                else:
                                    if self.hyperplanes[22].in_halfspace(point):
                                        return 11, 261, 8
                                    else:
                                        return 6, 260, 8
                    else:
                        if self.hyperplanes[25].in_halfspace(point):
                            if self.hyperplanes[4].in_halfspace(point):
                                if self.hyperplanes[3].in_halfspace(point):
                                    return 10, 267, 7
                                else:
                                    if self.hyperplanes[10].in_halfspace(point):
                                        return 11, 269, 8
                                    else:
                                        return 9, 268, 8
                            else:
                                if self.hyperplanes[6].in_halfspace(point):
                                    return 10, 271, 7
                                else:
                                    if self.hyperplanes[12].in_halfspace(point):
                                        return 11, 273, 8
                                    else:
                                        return 8, 272, 8
                        else:
                            if self.hyperplanes[27].in_halfspace(point):
                                if self.hyperplanes[3].in_halfspace(point):
                                    return 10, 277, 7
                                else:
                                    if self.hyperplanes[10].in_halfspace(point):
                                        return 11, 279, 8
                                    else:
                                        return 9, 278, 8
                            else:
                                if self.hyperplanes[29].in_halfspace(point):
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 11, 283, 8
                                    else:
                                        return 10, 282, 8
                                else:
                                    return 1, 280, 7
