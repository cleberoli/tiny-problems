from tinypy.generated.trees.generated_tree import GeneratedTree

from tinypy.geometry.point import Point


class TSPTree(GeneratedTree):

    def __init__(self, polytope):
        GeneratedTree.__init__(self, polytope)

    def test(self, point: Point):
        if self.hyperplanes[5].in_halfspace(point):
            if self.hyperplanes[6].in_halfspace(point):
                if self.hyperplanes[3].in_halfspace(point):
                    if self.hyperplanes[1].in_halfspace(point):
                        if self.hyperplanes[19].in_halfspace(point):
                            if self.hyperplanes[28].in_halfspace(point):
                                if self.hyperplanes[9].in_halfspace(point):
                                    if self.hyperplanes[25].in_halfspace(point):
                                        return 1, 263, 8, [5, 6, 3, 1, 19, 28, 9, 25]
                                    else:
                                        return 8, 262, 8, [5, 6, 3, 1, 19, 28, 9, -25]
                                else:
                                    if self.hyperplanes[20].in_halfspace(point):
                                        return 3, 261, 8, [5, 6, 3, 1, 19, 28, -9, 20]
                                    else:
                                        return 8, 260, 8, [5, 6, 3, 1, 19, 28, -9, -20]
                            else:
                                if self.hyperplanes[12].in_halfspace(point):
                                    return 8, 205, 7, [5, 6, 3, 1, 19, -28, 12]
                                else:
                                    return 11, 204, 7, [5, 6, 3, 1, 19, -28, -12]
                        else:
                            if self.hyperplanes[28].in_halfspace(point):
                                if self.hyperplanes[2].in_halfspace(point):
                                    if self.hyperplanes[23].in_halfspace(point):
                                        return 1, 259, 8, [5, 6, 3, 1, -19, 28, 2, 23]
                                    else:
                                        return 7, 258, 8, [5, 6, 3, 1, -19, 28, 2, -23]
                                else:
                                    if self.hyperplanes[25].in_halfspace(point):
                                        return 1, 257, 8, [5, 6, 3, 1, -19, 28, -2, 25]
                                    else:
                                        return 8, 256, 8, [5, 6, 3, 1, -19, 28, -2, -25]
                            else:
                                if self.hyperplanes[2].in_halfspace(point):
                                    if self.hyperplanes[14].in_halfspace(point):
                                        return 7, 255, 8, [5, 6, 3, 1, -19, -28, 2, 14]
                                    else:
                                        return 11, 254, 8, [5, 6, 3, 1, -19, -28, 2, -14]
                                else:
                                    if self.hyperplanes[12].in_halfspace(point):
                                        return 8, 253, 8, [5, 6, 3, 1, -19, -28, -2, 12]
                                    else:
                                        return 11, 252, 8, [5, 6, 3, 1, -19, -28, -2, -12]
                    else:
                        if self.hyperplanes[25].in_halfspace(point):
                            if self.hyperplanes[19].in_halfspace(point):
                                if self.hyperplanes[8].in_halfspace(point):
                                    return 2, 199, 7, [5, 6, 3, -1, 25, 19, 8]
                                else:
                                    return 3, 198, 7, [5, 6, 3, -1, 25, 19, -8]
                            else:
                                if self.hyperplanes[22].in_halfspace(point):
                                    return 2, 197, 7, [5, 6, 3, -1, 25, -19, 22]
                                else:
                                    return 7, 196, 7, [5, 6, 3, -1, 25, -19, -22]
                        else:
                            if self.hyperplanes[15].in_halfspace(point):
                                if self.hyperplanes[19].in_halfspace(point):
                                    return 3, 195, 7, [5, 6, 3, -1, -25, 15, 19]
                                else:
                                    return 7, 194, 7, [5, 6, 3, -1, -25, 15, -19]
                            else:
                                if self.hyperplanes[29].in_halfspace(point):
                                    return 3, 193, 7, [5, 6, 3, -1, -25, -15, 29]
                                else:
                                    return 12, 192, 7, [5, 6, 3, -1, -25, -15, -29]
                else:
                    if self.hyperplanes[10].in_halfspace(point):
                        if self.hyperplanes[23].in_halfspace(point):
                            if self.hyperplanes[1].in_halfspace(point):
                                if self.hyperplanes[25].in_halfspace(point):
                                    return 1, 191, 7, [5, 6, -3, 10, 23, 1, 25]
                                else:
                                    return 8, 190, 7, [5, 6, -3, 10, 23, 1, -25]
                            else:
                                if self.hyperplanes[24].in_halfspace(point):
                                    return 2, 189, 7, [5, 6, -3, 10, 23, -1, 24]
                                else:
                                    return 8, 188, 7, [5, 6, -3, 10, 23, -1, -24]
                        else:
                            if self.hyperplanes[24].in_halfspace(point):
                                if self.hyperplanes[22].in_halfspace(point):
                                    return 2, 187, 7, [5, 6, -3, 10, -23, 24, 22]
                                else:
                                    return 7, 186, 7, [5, 6, -3, 10, -23, 24, -22]
                            else:
                                if self.hyperplanes[2].in_halfspace(point):
                                    return 7, 185, 7, [5, 6, -3, 10, -23, -24, 2]
                                else:
                                    return 8, 184, 7, [5, 6, -3, 10, -23, -24, -2]
                    else:
                        if self.hyperplanes[1].in_halfspace(point):
                            if self.hyperplanes[18].in_halfspace(point):
                                if self.hyperplanes[9].in_halfspace(point):
                                    if self.hyperplanes[11].in_halfspace(point):
                                        return 1, 251, 8, [5, 6, -3, -10, 1, 18, 9, 11]
                                    else:
                                        return 4, 250, 8, [5, 6, -3, -10, 1, 18, 9, -11]
                                else:
                                    if self.hyperplanes[26].in_halfspace(point):
                                        return 4, 249, 8, [5, 6, -3, -10, 1, 18, -9, 26]
                                    else:
                                        return 11, 248, 8, [5, 6, -3, -10, 1, 18, -9, -26]
                            else:
                                if self.hyperplanes[9].in_halfspace(point):
                                    if self.hyperplanes[25].in_halfspace(point):
                                        return 1, 247, 8, [5, 6, -3, -10, 1, -18, 9, 25]
                                    else:
                                        return 8, 246, 8, [5, 6, -3, -10, 1, -18, 9, -25]
                                else:
                                    if self.hyperplanes[12].in_halfspace(point):
                                        return 8, 245, 8, [5, 6, -3, -10, 1, -18, -9, 12]
                                    else:
                                        return 11, 244, 8, [5, 6, -3, -10, 1, -18, -9, -12]
                        else:
                            if self.hyperplanes[18].in_halfspace(point):
                                if self.hyperplanes[27].in_halfspace(point):
                                    if self.hyperplanes[17].in_halfspace(point):
                                        return 4, 243, 8, [5, 6, -3, -10, -1, 18, 27, 17]
                                    else:
                                        return 7, 242, 8, [5, 6, -3, -10, -1, 18, 27, -17]
                                else:
                                    if self.hyperplanes[15].in_halfspace(point):
                                        return 7, 241, 8, [5, 6, -3, -10, -1, 18, -27, 15]
                                    else:
                                        return 12, 240, 8, [5, 6, -3, -10, -1, 18, -27, -15]
                            else:
                                if self.hyperplanes[2].in_halfspace(point):
                                    if self.hyperplanes[15].in_halfspace(point):
                                        return 7, 239, 8, [5, 6, -3, -10, -1, -18, 2, 15]
                                    else:
                                        return 12, 238, 8, [5, 6, -3, -10, -1, -18, 2, -15]
                                else:
                                    if self.hyperplanes[13].in_halfspace(point):
                                        return 8, 237, 8, [5, 6, -3, -10, -1, -18, -2, 13]
                                    else:
                                        return 12, 236, 8, [5, 6, -3, -10, -1, -18, -2, -13]
            else:
                if self.hyperplanes[15].in_halfspace(point):
                    if self.hyperplanes[9].in_halfspace(point):
                        if self.hyperplanes[7].in_halfspace(point):
                            if self.hyperplanes[22].in_halfspace(point):
                                return 2, 111, 6, [5, -6, 15, 9, 7, 22]
                            else:
                                return 7, 110, 6, [5, -6, 15, 9, 7, -22]
                        else:
                            if self.hyperplanes[28].in_halfspace(point):
                                return 2, 109, 6, [5, -6, 15, 9, -7, 28]
                            else:
                                return 10, 108, 6, [5, -6, 15, 9, -7, -28]
                    else:
                        if self.hyperplanes[12].in_halfspace(point):
                            if self.hyperplanes[22].in_halfspace(point):
                                return 2, 107, 6, [5, -6, 15, -9, 12, 22]
                            else:
                                return 7, 106, 6, [5, -6, 15, -9, 12, -22]
                        else:
                            if self.hyperplanes[16].in_halfspace(point):
                                return 5, 105, 6, [5, -6, 15, -9, -12, 16]
                            else:
                                return 7, 104, 6, [5, -6, 15, -9, -12, -16]
                else:
                    if self.hyperplanes[9].in_halfspace(point):
                        if self.hyperplanes[10].in_halfspace(point):
                            if self.hyperplanes[28].in_halfspace(point):
                                return 2, 103, 6, [5, -6, -15, 9, 10, 28]
                            else:
                                return 10, 102, 6, [5, -6, -15, 9, 10, -28]
                        else:
                            if self.hyperplanes[21].in_halfspace(point):
                                return 4, 101, 6, [5, -6, -15, 9, -10, 21]
                            else:
                                return 10, 100, 6, [5, -6, -15, 9, -10, -21]
                    else:
                        if self.hyperplanes[25].in_halfspace(point):
                            if self.hyperplanes[10].in_halfspace(point):
                                if self.hyperplanes[12].in_halfspace(point):
                                    return 2, 175, 7, [5, -6, -15, -9, 25, 10, 12]
                                else:
                                    return 5, 174, 7, [5, -6, -15, -9, 25, 10, -12]
                            else:
                                if self.hyperplanes[4].in_halfspace(point):
                                    return 4, 173, 7, [5, -6, -15, -9, 25, -10, 4]
                                else:
                                    return 5, 172, 7, [5, -6, -15, -9, 25, -10, -4]
                        else:
                            if self.hyperplanes[10].in_halfspace(point):
                                if self.hyperplanes[30].in_halfspace(point):
                                    return 2, 171, 7, [5, -6, -15, -9, -25, 10, 30]
                                else:
                                    return 12, 170, 7, [5, -6, -15, -9, -25, 10, -30]
                            else:
                                if self.hyperplanes[27].in_halfspace(point):
                                    return 4, 169, 7, [5, -6, -15, -9, -25, -10, 27]
                                else:
                                    return 12, 168, 7, [5, -6, -15, -9, -25, -10, -27]
        else:
            if self.hyperplanes[6].in_halfspace(point):
                if self.hyperplanes[15].in_halfspace(point):
                    if self.hyperplanes[9].in_halfspace(point):
                        if self.hyperplanes[25].in_halfspace(point):
                            if self.hyperplanes[10].in_halfspace(point):
                                if self.hyperplanes[27].in_halfspace(point):
                                    return 1, 167, 7, [-5, 6, 15, 9, 25, 10, 27]
                                else:
                                    return 9, 166, 7, [-5, 6, 15, 9, 25, 10, -27]
                            else:
                                if self.hyperplanes[30].in_halfspace(point):
                                    return 1, 165, 7, [-5, 6, 15, 9, 25, -10, 30]
                                else:
                                    return 11, 164, 7, [-5, 6, 15, 9, 25, -10, -30]
                        else:
                            if self.hyperplanes[10].in_halfspace(point):
                                if self.hyperplanes[4].in_halfspace(point):
                                    return 8, 163, 7, [-5, 6, 15, 9, -25, 10, 4]
                                else:
                                    return 9, 162, 7, [-5, 6, 15, 9, -25, 10, -4]
                            else:
                                if self.hyperplanes[12].in_halfspace(point):
                                    return 8, 161, 7, [-5, 6, 15, 9, -25, -10, 12]
                                else:
                                    return 11, 160, 7, [-5, 6, 15, 9, -25, -10, -12]
                    else:
                        if self.hyperplanes[10].in_halfspace(point):
                            if self.hyperplanes[21].in_halfspace(point):
                                return 3, 91, 6, [-5, 6, 15, -9, 10, 21]
                            else:
                                return 9, 90, 6, [-5, 6, 15, -9, 10, -21]
                        else:
                            if self.hyperplanes[28].in_halfspace(point):
                                return 3, 89, 6, [-5, 6, 15, -9, -10, 28]
                            else:
                                return 11, 88, 6, [-5, 6, 15, -9, -10, -28]
                else:
                    if self.hyperplanes[9].in_halfspace(point):
                        if self.hyperplanes[12].in_halfspace(point):
                            if self.hyperplanes[16].in_halfspace(point):
                                return 6, 87, 6, [-5, 6, -15, 9, 12, 16]
                            else:
                                return 8, 86, 6, [-5, 6, -15, 9, 12, -16]
                        else:
                            if self.hyperplanes[22].in_halfspace(point):
                                return 6, 85, 6, [-5, 6, -15, 9, -12, 22]
                            else:
                                return 11, 84, 6, [-5, 6, -15, 9, -12, -22]
                    else:
                        if self.hyperplanes[7].in_halfspace(point):
                            if self.hyperplanes[28].in_halfspace(point):
                                return 3, 83, 6, [-5, 6, -15, -9, 7, 28]
                            else:
                                return 11, 82, 6, [-5, 6, -15, -9, 7, -28]
                        else:
                            if self.hyperplanes[22].in_halfspace(point):
                                return 6, 81, 6, [-5, 6, -15, -9, -7, 22]
                            else:
                                return 11, 80, 6, [-5, 6, -15, -9, -7, -22]
            else:
                if self.hyperplanes[3].in_halfspace(point):
                    if self.hyperplanes[10].in_halfspace(point):
                        if self.hyperplanes[1].in_halfspace(point):
                            if self.hyperplanes[18].in_halfspace(point):
                                if self.hyperplanes[2].in_halfspace(point):
                                    if self.hyperplanes[13].in_halfspace(point):
                                        return 1, 235, 8, [-5, -6, 3, 10, 1, 18, 2, 13]
                                    else:
                                        return 5, 234, 8, [-5, -6, 3, 10, 1, 18, 2, -13]
                                else:
                                    if self.hyperplanes[15].in_halfspace(point):
                                        return 1, 233, 8, [-5, -6, 3, 10, 1, 18, -2, 15]
                                    else:
                                        return 6, 232, 8, [-5, -6, 3, 10, 1, 18, -2, -15]
                            else:
                                if self.hyperplanes[27].in_halfspace(point):
                                    if self.hyperplanes[15].in_halfspace(point):
                                        return 1, 231, 8, [-5, -6, 3, 10, 1, -18, 27, 15]
                                    else:
                                        return 6, 230, 8, [-5, -6, 3, 10, 1, -18, 27, -15]
                                else:
                                    if self.hyperplanes[17].in_halfspace(point):
                                        return 6, 229, 8, [-5, -6, 3, 10, 1, -18, -27, 17]
                                    else:
                                        return 9, 228, 8, [-5, -6, 3, 10, 1, -18, -27, -17]
                        else:
                            if self.hyperplanes[18].in_halfspace(point):
                                if self.hyperplanes[9].in_halfspace(point):
                                    if self.hyperplanes[12].in_halfspace(point):
                                        return 2, 227, 8, [-5, -6, 3, 10, -1, 18, 9, 12]
                                    else:
                                        return 5, 226, 8, [-5, -6, 3, 10, -1, 18, 9, -12]
                                else:
                                    if self.hyperplanes[25].in_halfspace(point):
                                        return 5, 225, 8, [-5, -6, 3, 10, -1, 18, -9, 25]
                                    else:
                                        return 12, 224, 8, [-5, -6, 3, 10, -1, 18, -9, -25]
                            else:
                                if self.hyperplanes[9].in_halfspace(point):
                                    if self.hyperplanes[26].in_halfspace(point):
                                        return 2, 223, 8, [-5, -6, 3, 10, -1, -18, 9, 26]
                                    else:
                                        return 9, 222, 8, [-5, -6, 3, 10, -1, -18, 9, -26]
                                else:
                                    if self.hyperplanes[11].in_halfspace(point):
                                        return 9, 221, 8, [-5, -6, 3, 10, -1, -18, -9, 11]
                                    else:
                                        return 12, 220, 8, [-5, -6, 3, 10, -1, -18, -9, -11]
                    else:
                        if self.hyperplanes[23].in_halfspace(point):
                            if self.hyperplanes[24].in_halfspace(point):
                                if self.hyperplanes[2].in_halfspace(point):
                                    return 5, 151, 7, [-5, -6, 3, -10, 23, 24, 2]
                                else:
                                    return 6, 150, 7, [-5, -6, 3, -10, 23, 24, -2]
                            else:
                                if self.hyperplanes[22].in_halfspace(point):
                                    return 6, 149, 7, [-5, -6, 3, -10, 23, -24, 22]
                                else:
                                    return 11, 148, 7, [-5, -6, 3, -10, 23, -24, -22]
                        else:
                            if self.hyperplanes[1].in_halfspace(point):
                                if self.hyperplanes[24].in_halfspace(point):
                                    return 5, 147, 7, [-5, -6, 3, -10, -23, 1, 24]
                                else:
                                    return 11, 146, 7, [-5, -6, 3, -10, -23, 1, -24]
                            else:
                                if self.hyperplanes[25].in_halfspace(point):
                                    return 5, 145, 7, [-5, -6, 3, -10, -23, -1, 25]
                                else:
                                    return 12, 144, 7, [-5, -6, 3, -10, -23, -1, -25]
                else:
                    if self.hyperplanes[1].in_halfspace(point):
                        if self.hyperplanes[25].in_halfspace(point):
                            if self.hyperplanes[15].in_halfspace(point):
                                if self.hyperplanes[29].in_halfspace(point):
                                    return 1, 143, 7, [-5, -6, -3, 1, 25, 15, 29]
                                else:
                                    return 10, 142, 7, [-5, -6, -3, 1, 25, 15, -29]
                            else:
                                if self.hyperplanes[19].in_halfspace(point):
                                    return 6, 141, 7, [-5, -6, -3, 1, 25, -15, 19]
                                else:
                                    return 10, 140, 7, [-5, -6, -3, 1, 25, -15, -19]
                        else:
                            if self.hyperplanes[19].in_halfspace(point):
                                if self.hyperplanes[22].in_halfspace(point):
                                    return 6, 139, 7, [-5, -6, -3, 1, -25, 19, 22]
                                else:
                                    return 11, 138, 7, [-5, -6, -3, 1, -25, 19, -22]
                            else:
                                if self.hyperplanes[8].in_halfspace(point):
                                    return 10, 137, 7, [-5, -6, -3, 1, -25, -19, 8]
                                else:
                                    return 11, 136, 7, [-5, -6, -3, 1, -25, -19, -8]
                    else:
                        if self.hyperplanes[19].in_halfspace(point):
                            if self.hyperplanes[28].in_halfspace(point):
                                if self.hyperplanes[2].in_halfspace(point):
                                    if self.hyperplanes[12].in_halfspace(point):
                                        return 2, 219, 8, [-5, -6, -3, -1, 19, 28, 2, 12]
                                    else:
                                        return 5, 218, 8, [-5, -6, -3, -1, 19, 28, 2, -12]
                                else:
                                    if self.hyperplanes[14].in_halfspace(point):
                                        return 2, 217, 8, [-5, -6, -3, -1, 19, 28, -2, 14]
                                    else:
                                        return 6, 216, 8, [-5, -6, -3, -1, 19, 28, -2, -14]
                            else:
                                if self.hyperplanes[2].in_halfspace(point):
                                    if self.hyperplanes[25].in_halfspace(point):
                                        return 5, 215, 8, [-5, -6, -3, -1, 19, -28, 2, 25]
                                    else:
                                        return 12, 214, 8, [-5, -6, -3, -1, 19, -28, 2, -25]
                                else:
                                    if self.hyperplanes[23].in_halfspace(point):
                                        return 6, 213, 8, [-5, -6, -3, -1, 19, -28, -2, 23]
                                    else:
                                        return 12, 212, 8, [-5, -6, -3, -1, 19, -28, -2, -23]
                        else:
                            if self.hyperplanes[28].in_halfspace(point):
                                if self.hyperplanes[12].in_halfspace(point):
                                    return 2, 131, 7, [-5, -6, -3, -1, -19, 28, 12]
                                else:
                                    return 5, 130, 7, [-5, -6, -3, -1, -19, 28, -12]
                            else:
                                if self.hyperplanes[9].in_halfspace(point):
                                    if self.hyperplanes[20].in_halfspace(point):
                                        return 5, 211, 8, [-5, -6, -3, -1, -19, -28, 9, 20]
                                    else:
                                        return 10, 210, 8, [-5, -6, -3, -1, -19, -28, 9, -20]
                                else:
                                    if self.hyperplanes[25].in_halfspace(point):
                                        return 5, 209, 8, [-5, -6, -3, -1, -19, -28, -9, 25]
                                    else:
                                        return 12, 208, 8, [-5, -6, -3, -1, -19, -28, -9, -25]
