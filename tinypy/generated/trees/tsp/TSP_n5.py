from tinypy.generated.trees.generated_tree import GeneratedTree

from tinypy.geometry.point import Point


class TSPTree(GeneratedTree):

    def __init__(self, polytope):
        GeneratedTree.__init__(self, polytope)

    def test(self, point: Point):
        if self.hyperplanes[1].in_halfspace(point):
            if self.hyperplanes[9].in_halfspace(point):
                if self.hyperplanes[11].in_halfspace(point):
                    if self.hyperplanes[13].in_halfspace(point):
                        if self.hyperplanes[15].in_halfspace(point):
                            if self.hyperplanes[23].in_halfspace(point):
                                if self.hyperplanes[25].in_halfspace(point):
                                    if self.hyperplanes[27].in_halfspace(point):
                                        if self.hyperplanes[29].in_halfspace(point):
                                            if self.hyperplanes[30].in_halfspace(point):
                                                return 1, 21, 10, [1, 9, 11, 13, 15, 23, 25, 27, 29, 30]
                                            else:
                                                return 11, 20, 10, [1, 9, 11, 13, 15, 23, 25, 27, 29, -30]
                                        else:
                                            return 10, 18, 9, [1, 9, 11, 13, 15, 23, 25, 27, -29]
                                    else:
                                        if self.hyperplanes[3].in_halfspace(point):
                                            if self.hyperplanes[10].in_halfspace(point):
                                                return 9, 25, 10, [1, 9, 11, 13, 15, 23, 25, -27, 3, 10]
                                            else:
                                                return 11, 24, 10, [1, 9, 11, 13, 15, 23, 25, -27, 3, -10]
                                        else:
                                            return 10, 22, 9, [1, 9, 11, 13, 15, 23, 25, -27, -3]
                                else:
                                    if self.hyperplanes[4].in_halfspace(point):
                                        if self.hyperplanes[6].in_halfspace(point):
                                            if self.hyperplanes[12].in_halfspace(point):
                                                return 8, 31, 10, [1, 9, 11, 13, 15, 23, -25, 4, 6, 12]
                                            else:
                                                return 11, 30, 10, [1, 9, 11, 13, 15, 23, -25, 4, 6, -12]
                                        else:
                                            return 10, 28, 9, [1, 9, 11, 13, 15, 23, -25, 4, -6]
                                    else:
                                        if self.hyperplanes[3].in_halfspace(point):
                                            if self.hyperplanes[10].in_halfspace(point):
                                                return 9, 35, 10, [1, 9, 11, 13, 15, 23, -25, -4, 3, 10]
                                            else:
                                                return 11, 34, 10, [1, 9, 11, 13, 15, 23, -25, -4, 3, -10]
                                        else:
                                            return 10, 32, 9, [1, 9, 11, 13, 15, 23, -25, -4, -3]
                            else:
                                if self.hyperplanes[2].in_halfspace(point):
                                    if self.hyperplanes[5].in_halfspace(point):
                                        return 7, 39, 8, [1, 9, 11, 13, 15, -23, 2, 5]
                                    else:
                                        return 9, 38, 8, [1, 9, 11, 13, 15, -23, 2, -5]
                                else:
                                    if self.hyperplanes[4].in_halfspace(point):
                                        if self.hyperplanes[6].in_halfspace(point):
                                            if self.hyperplanes[12].in_halfspace(point):
                                                return 8, 45, 10, [1, 9, 11, 13, 15, -23, -2, 4, 6, 12]
                                            else:
                                                return 11, 44, 10, [1, 9, 11, 13, 15, -23, -2, 4, 6, -12]
                                        else:
                                            return 10, 42, 9, [1, 9, 11, 13, 15, -23, -2, 4, -6]
                                    else:
                                        if self.hyperplanes[3].in_halfspace(point):
                                            if self.hyperplanes[10].in_halfspace(point):
                                                return 9, 49, 10, [1, 9, 11, 13, 15, -23, -2, -4, 3, 10]
                                            else:
                                                return 11, 48, 10, [1, 9, 11, 13, 15, -23, -2, -4, 3, -10]
                                        else:
                                            return 10, 46, 9, [1, 9, 11, 13, 15, -23, -2, -4, -3]
                        else:
                            if self.hyperplanes[16].in_halfspace(point):
                                if self.hyperplanes[17].in_halfspace(point):
                                    if self.hyperplanes[19].in_halfspace(point):
                                        if self.hyperplanes[22].in_halfspace(point):
                                            return 6, 57, 9, [1, 9, 11, 13, -15, 16, 17, 19, 22]
                                        else:
                                            return 11, 56, 9, [1, 9, 11, 13, -15, 16, 17, 19, -22]
                                    else:
                                        if self.hyperplanes[8].in_halfspace(point):
                                            return 10, 59, 9, [1, 9, 11, 13, -15, 16, 17, -19, 8]
                                        else:
                                            return 11, 58, 9, [1, 9, 11, 13, -15, 16, 17, -19, -8]
                                else:
                                    if self.hyperplanes[3].in_halfspace(point):
                                        if self.hyperplanes[10].in_halfspace(point):
                                            return 9, 63, 9, [1, 9, 11, 13, -15, 16, -17, 3, 10]
                                        else:
                                            return 11, 62, 9, [1, 9, 11, 13, -15, 16, -17, 3, -10]
                                    else:
                                        if self.hyperplanes[8].in_halfspace(point):
                                            return 10, 65, 9, [1, 9, 11, 13, -15, 16, -17, -3, 8]
                                        else:
                                            return 11, 64, 9, [1, 9, 11, 13, -15, 16, -17, -3, -8]
                            else:
                                if self.hyperplanes[4].in_halfspace(point):
                                    if self.hyperplanes[6].in_halfspace(point):
                                        if self.hyperplanes[12].in_halfspace(point):
                                            return 8, 71, 9, [1, 9, 11, 13, -15, -16, 4, 6, 12]
                                        else:
                                            return 11, 70, 9, [1, 9, 11, 13, -15, -16, 4, 6, -12]
                                    else:
                                        if self.hyperplanes[8].in_halfspace(point):
                                            return 10, 73, 9, [1, 9, 11, 13, -15, -16, 4, -6, 8]
                                        else:
                                            return 11, 72, 9, [1, 9, 11, 13, -15, -16, 4, -6, -8]
                                else:
                                    if self.hyperplanes[3].in_halfspace(point):
                                        if self.hyperplanes[10].in_halfspace(point):
                                            return 9, 77, 9, [1, 9, 11, 13, -15, -16, -4, 3, 10]
                                        else:
                                            return 11, 76, 9, [1, 9, 11, 13, -15, -16, -4, 3, -10]
                                    else:
                                        if self.hyperplanes[8].in_halfspace(point):
                                            return 10, 79, 9, [1, 9, 11, 13, -15, -16, -4, -3, 8]
                                        else:
                                            return 11, 78, 9, [1, 9, 11, 13, -15, -16, -4, -3, -8]
                    else:
                        if self.hyperplanes[2].in_halfspace(point):
                            if self.hyperplanes[18].in_halfspace(point):
                                return 5, 83, 6, [1, 9, 11, -13, 2, 18]
                            else:
                                return 9, 82, 6, [1, 9, 11, -13, 2, -18]
                        else:
                            if self.hyperplanes[17].in_halfspace(point):
                                if self.hyperplanes[19].in_halfspace(point):
                                    if self.hyperplanes[22].in_halfspace(point):
                                        return 6, 89, 8, [1, 9, 11, -13, -2, 17, 19, 22]
                                    else:
                                        return 11, 88, 8, [1, 9, 11, -13, -2, 17, 19, -22]
                                else:
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 10, 91, 8, [1, 9, 11, -13, -2, 17, -19, 8]
                                    else:
                                        return 11, 90, 8, [1, 9, 11, -13, -2, 17, -19, -8]
                            else:
                                if self.hyperplanes[3].in_halfspace(point):
                                    if self.hyperplanes[10].in_halfspace(point):
                                        return 9, 95, 8, [1, 9, 11, -13, -2, -17, 3, 10]
                                    else:
                                        return 11, 94, 8, [1, 9, 11, -13, -2, -17, 3, -10]
                                else:
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 10, 97, 8, [1, 9, 11, -13, -2, -17, -3, 8]
                                    else:
                                        return 11, 96, 8, [1, 9, 11, -13, -2, -17, -3, -8]
                else:
                    if self.hyperplanes[5].in_halfspace(point):
                        if self.hyperplanes[18].in_halfspace(point):
                            return 4, 101, 5, [1, 9, -11, 5, 18]
                        else:
                            return 8, 100, 5, [1, 9, -11, 5, -18]
                    else:
                        if self.hyperplanes[16].in_halfspace(point):
                            if self.hyperplanes[19].in_halfspace(point):
                                if self.hyperplanes[22].in_halfspace(point):
                                    return 6, 107, 7, [1, 9, -11, -5, 16, 19, 22]
                                else:
                                    return 11, 106, 7, [1, 9, -11, -5, 16, 19, -22]
                            else:
                                if self.hyperplanes[8].in_halfspace(point):
                                    return 10, 109, 7, [1, 9, -11, -5, 16, -19, 8]
                                else:
                                    return 11, 108, 7, [1, 9, -11, -5, 16, -19, -8]
                        else:
                            if self.hyperplanes[6].in_halfspace(point):
                                if self.hyperplanes[12].in_halfspace(point):
                                    return 8, 113, 7, [1, 9, -11, -5, -16, 6, 12]
                                else:
                                    return 11, 112, 7, [1, 9, -11, -5, -16, 6, -12]
                            else:
                                if self.hyperplanes[8].in_halfspace(point):
                                    return 10, 115, 7, [1, 9, -11, -5, -16, -6, 8]
                                else:
                                    return 11, 114, 7, [1, 9, -11, -5, -16, -6, -8]
            else:
                if self.hyperplanes[3].in_halfspace(point):
                    if self.hyperplanes[6].in_halfspace(point):
                        if self.hyperplanes[7].in_halfspace(point):
                            if self.hyperplanes[19].in_halfspace(point):
                                if self.hyperplanes[20].in_halfspace(point):
                                    if self.hyperplanes[21].in_halfspace(point):
                                        if self.hyperplanes[28].in_halfspace(point):
                                            return 3, 129, 9, [1, -9, 3, 6, 7, 19, 20, 21, 28]
                                        else:
                                            return 11, 128, 9, [1, -9, 3, 6, 7, 19, 20, 21, -28]
                                    else:
                                        if self.hyperplanes[10].in_halfspace(point):
                                            return 9, 131, 9, [1, -9, 3, 6, 7, 19, 20, -21, 10]
                                        else:
                                            return 11, 130, 9, [1, -9, 3, 6, 7, 19, 20, -21, -10]
                                else:
                                    if self.hyperplanes[12].in_halfspace(point):
                                        return 8, 133, 8, [1, -9, 3, 6, 7, 19, -20, 12]
                                    else:
                                        return 11, 132, 8, [1, -9, 3, 6, 7, 19, -20, -12]
                            else:
                                if self.hyperplanes[2].in_halfspace(point):
                                    if self.hyperplanes[5].in_halfspace(point):
                                        if self.hyperplanes[14].in_halfspace(point):
                                            return 7, 139, 9, [1, -9, 3, 6, 7, -19, 2, 5, 14]
                                        else:
                                            return 11, 138, 9, [1, -9, 3, 6, 7, -19, 2, 5, -14]
                                    else:
                                        if self.hyperplanes[10].in_halfspace(point):
                                            return 9, 141, 9, [1, -9, 3, 6, 7, -19, 2, -5, 10]
                                        else:
                                            return 11, 140, 9, [1, -9, 3, 6, 7, -19, 2, -5, -10]
                                else:
                                    if self.hyperplanes[12].in_halfspace(point):
                                        return 8, 143, 8, [1, -9, 3, 6, 7, -19, -2, 12]
                                    else:
                                        return 11, 142, 8, [1, -9, 3, 6, 7, -19, -2, -12]
                        else:
                            if self.hyperplanes[22].in_halfspace(point):
                                return 6, 145, 6, [1, -9, 3, 6, -7, 22]
                            else:
                                return 11, 144, 6, [1, -9, 3, 6, -7, -22]
                    else:
                        if self.hyperplanes[2].in_halfspace(point):
                            if self.hyperplanes[18].in_halfspace(point):
                                if self.hyperplanes[24].in_halfspace(point):
                                    return 5, 151, 7, [1, -9, 3, -6, 2, 18, 24]
                                else:
                                    return 11, 150, 7, [1, -9, 3, -6, 2, 18, -24]
                            else:
                                if self.hyperplanes[10].in_halfspace(point):
                                    return 9, 153, 7, [1, -9, 3, -6, 2, -18, 10]
                                else:
                                    return 11, 152, 7, [1, -9, 3, -6, 2, -18, -10]
                        else:
                            if self.hyperplanes[22].in_halfspace(point):
                                return 6, 155, 6, [1, -9, 3, -6, -2, 22]
                            else:
                                return 11, 154, 6, [1, -9, 3, -6, -2, -22]
                else:
                    if self.hyperplanes[5].in_halfspace(point):
                        if self.hyperplanes[18].in_halfspace(point):
                            if self.hyperplanes[26].in_halfspace(point):
                                return 4, 161, 6, [1, -9, -3, 5, 18, 26]
                            else:
                                return 11, 160, 6, [1, -9, -3, 5, 18, -26]
                        else:
                            if self.hyperplanes[12].in_halfspace(point):
                                return 8, 163, 6, [1, -9, -3, 5, -18, 12]
                            else:
                                return 11, 162, 6, [1, -9, -3, 5, -18, -12]
                    else:
                        if self.hyperplanes[22].in_halfspace(point):
                            return 6, 165, 5, [1, -9, -3, -5, 22]
                        else:
                            return 11, 164, 5, [1, -9, -3, -5, -22]
        else:
            if self.hyperplanes[8].in_halfspace(point):
                if self.hyperplanes[10].in_halfspace(point):
                    if self.hyperplanes[12].in_halfspace(point):
                        if self.hyperplanes[14].in_halfspace(point):
                            if self.hyperplanes[22].in_halfspace(point):
                                if self.hyperplanes[24].in_halfspace(point):
                                    if self.hyperplanes[26].in_halfspace(point):
                                        if self.hyperplanes[28].in_halfspace(point):
                                            if self.hyperplanes[30].in_halfspace(point):
                                                return 2, 183, 10, [-1, 8, 10, 12, 14, 22, 24, 26, 28, 30]
                                            else:
                                                return 12, 182, 10, [-1, 8, 10, 12, 14, 22, 24, 26, 28, -30]
                                        else:
                                            if self.hyperplanes[9].in_halfspace(point):
                                                return 10, 185, 10, [-1, 8, 10, 12, 14, 22, 24, 26, -28, 9]
                                            else:
                                                return 12, 184, 10, [-1, 8, 10, 12, 14, 22, 24, 26, -28, -9]
                                    else:
                                        if self.hyperplanes[3].in_halfspace(point):
                                            return 9, 187, 9, [-1, 8, 10, 12, 14, 22, 24, -26, 3]
                                        else:
                                            return 10, 186, 9, [-1, 8, 10, 12, 14, 22, 24, -26, -3]
                                else:
                                    if self.hyperplanes[6].in_halfspace(point):
                                        return 8, 189, 8, [-1, 8, 10, 12, 14, 22, -24, 6]
                                    else:
                                        return 10, 188, 8, [-1, 8, 10, 12, 14, 22, -24, -6]
                            else:
                                if self.hyperplanes[2].in_halfspace(point):
                                    if self.hyperplanes[5].in_halfspace(point):
                                        if self.hyperplanes[7].in_halfspace(point):
                                            if self.hyperplanes[15].in_halfspace(point):
                                                return 7, 197, 10, [-1, 8, 10, 12, 14, -22, 2, 5, 7, 15]
                                            else:
                                                return 12, 196, 10, [-1, 8, 10, 12, 14, -22, 2, 5, 7, -15]
                                        else:
                                            if self.hyperplanes[9].in_halfspace(point):
                                                return 10, 199, 10, [-1, 8, 10, 12, 14, -22, 2, 5, -7, 9]
                                            else:
                                                return 12, 198, 10, [-1, 8, 10, 12, 14, -22, 2, 5, -7, -9]
                                    else:
                                        if self.hyperplanes[3].in_halfspace(point):
                                            return 9, 201, 9, [-1, 8, 10, 12, 14, -22, 2, -5, 3]
                                        else:
                                            return 10, 200, 9, [-1, 8, 10, 12, 14, -22, 2, -5, -3]
                                else:
                                    if self.hyperplanes[6].in_halfspace(point):
                                        return 8, 203, 8, [-1, 8, 10, 12, 14, -22, -2, 6]
                                    else:
                                        return 10, 202, 8, [-1, 8, 10, 12, 14, -22, -2, -6]
                        else:
                            if self.hyperplanes[19].in_halfspace(point):
                                return 6, 205, 6, [-1, 8, 10, 12, -14, 19]
                            else:
                                return 10, 204, 6, [-1, 8, 10, 12, -14, -19]
                    else:
                        if self.hyperplanes[2].in_halfspace(point):
                            if self.hyperplanes[16].in_halfspace(point):
                                if self.hyperplanes[18].in_halfspace(point):
                                    if self.hyperplanes[20].in_halfspace(point):
                                        if self.hyperplanes[25].in_halfspace(point):
                                            return 5, 215, 9, [-1, 8, 10, -12, 2, 16, 18, 20, 25]
                                        else:
                                            return 12, 214, 9, [-1, 8, 10, -12, 2, 16, 18, 20, -25]
                                    else:
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 10, 217, 9, [-1, 8, 10, -12, 2, 16, 18, -20, 9]
                                        else:
                                            return 12, 216, 9, [-1, 8, 10, -12, 2, 16, 18, -20, -9]
                                else:
                                    if self.hyperplanes[3].in_halfspace(point):
                                        if self.hyperplanes[11].in_halfspace(point):
                                            return 9, 221, 9, [-1, 8, 10, -12, 2, 16, -18, 3, 11]
                                        else:
                                            return 12, 220, 9, [-1, 8, 10, -12, 2, 16, -18, 3, -11]
                                    else:
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 10, 223, 9, [-1, 8, 10, -12, 2, 16, -18, -3, 9]
                                        else:
                                            return 12, 222, 9, [-1, 8, 10, -12, 2, 16, -18, -3, -9]
                            else:
                                if self.hyperplanes[5].in_halfspace(point):
                                    if self.hyperplanes[15].in_halfspace(point):
                                        return 7, 227, 8, [-1, 8, 10, -12, 2, -16, 5, 15]
                                    else:
                                        return 12, 226, 8, [-1, 8, 10, -12, 2, -16, 5, -15]
                                else:
                                    if self.hyperplanes[3].in_halfspace(point):
                                        if self.hyperplanes[11].in_halfspace(point):
                                            return 9, 231, 9, [-1, 8, 10, -12, 2, -16, -5, 3, 11]
                                        else:
                                            return 12, 230, 9, [-1, 8, 10, -12, 2, -16, -5, 3, -11]
                                    else:
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 10, 233, 9, [-1, 8, 10, -12, 2, -16, -5, -3, 9]
                                        else:
                                            return 12, 232, 9, [-1, 8, 10, -12, 2, -16, -5, -3, -9]
                        else:
                            if self.hyperplanes[19].in_halfspace(point):
                                return 6, 235, 6, [-1, 8, 10, -12, -2, 19]
                            else:
                                return 10, 234, 6, [-1, 8, 10, -12, -2, -19]
                else:
                    if self.hyperplanes[4].in_halfspace(point):
                        if self.hyperplanes[5].in_halfspace(point):
                            if self.hyperplanes[17].in_halfspace(point):
                                if self.hyperplanes[18].in_halfspace(point):
                                    if self.hyperplanes[21].in_halfspace(point):
                                        if self.hyperplanes[27].in_halfspace(point):
                                            return 4, 247, 9, [-1, 8, -10, 4, 5, 17, 18, 21, 27]
                                        else:
                                            return 12, 246, 9, [-1, 8, -10, 4, 5, 17, 18, 21, -27]
                                    else:
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 10, 249, 9, [-1, 8, -10, 4, 5, 17, 18, -21, 9]
                                        else:
                                            return 12, 248, 9, [-1, 8, -10, 4, 5, 17, 18, -21, -9]
                                else:
                                    if self.hyperplanes[6].in_halfspace(point):
                                        if self.hyperplanes[13].in_halfspace(point):
                                            return 8, 253, 9, [-1, 8, -10, 4, 5, 17, -18, 6, 13]
                                        else:
                                            return 12, 252, 9, [-1, 8, -10, 4, 5, 17, -18, 6, -13]
                                    else:
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 10, 255, 9, [-1, 8, -10, 4, 5, 17, -18, -6, 9]
                                        else:
                                            return 12, 254, 9, [-1, 8, -10, 4, 5, 17, -18, -6, -9]
                            else:
                                if self.hyperplanes[2].in_halfspace(point):
                                    if self.hyperplanes[15].in_halfspace(point):
                                        return 7, 259, 8, [-1, 8, -10, 4, 5, -17, 2, 15]
                                    else:
                                        return 12, 258, 8, [-1, 8, -10, 4, 5, -17, 2, -15]
                                else:
                                    if self.hyperplanes[6].in_halfspace(point):
                                        if self.hyperplanes[13].in_halfspace(point):
                                            return 8, 263, 9, [-1, 8, -10, 4, 5, -17, -2, 6, 13]
                                        else:
                                            return 12, 262, 9, [-1, 8, -10, 4, 5, -17, -2, 6, -13]
                                    else:
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 10, 265, 9, [-1, 8, -10, 4, 5, -17, -2, -6, 9]
                                        else:
                                            return 12, 264, 9, [-1, 8, -10, 4, 5, -17, -2, -6, -9]
                        else:
                            if self.hyperplanes[19].in_halfspace(point):
                                if self.hyperplanes[23].in_halfspace(point):
                                    return 6, 269, 7, [-1, 8, -10, 4, -5, 19, 23]
                                else:
                                    return 12, 268, 7, [-1, 8, -10, 4, -5, 19, -23]
                            else:
                                if self.hyperplanes[9].in_halfspace(point):
                                    return 10, 271, 7, [-1, 8, -10, 4, -5, -19, 9]
                                else:
                                    return 12, 270, 7, [-1, 8, -10, 4, -5, -19, -9]
                    else:
                        if self.hyperplanes[2].in_halfspace(point):
                            if self.hyperplanes[25].in_halfspace(point):
                                return 5, 275, 6, [-1, 8, -10, -4, 2, 25]
                            else:
                                return 12, 274, 6, [-1, 8, -10, -4, 2, -25]
                        else:
                            if self.hyperplanes[19].in_halfspace(point):
                                if self.hyperplanes[23].in_halfspace(point):
                                    return 6, 279, 7, [-1, 8, -10, -4, -2, 19, 23]
                                else:
                                    return 12, 278, 7, [-1, 8, -10, -4, -2, 19, -23]
                            else:
                                if self.hyperplanes[9].in_halfspace(point):
                                    return 10, 281, 7, [-1, 8, -10, -4, -2, -19, 9]
                                else:
                                    return 12, 280, 7, [-1, 8, -10, -4, -2, -19, -9]
            else:
                if self.hyperplanes[3].in_halfspace(point):
                    if self.hyperplanes[6].in_halfspace(point):
                        if self.hyperplanes[19].in_halfspace(point):
                            if self.hyperplanes[29].in_halfspace(point):
                                return 3, 289, 6, [-1, -8, 3, 6, 19, 29]
                            else:
                                return 12, 288, 6, [-1, -8, 3, 6, 19, -29]
                        else:
                            if self.hyperplanes[15].in_halfspace(point):
                                return 7, 291, 6, [-1, -8, 3, 6, -19, 15]
                            else:
                                return 12, 290, 6, [-1, -8, 3, 6, -19, -15]
                    else:
                        if self.hyperplanes[16].in_halfspace(point):
                            if self.hyperplanes[18].in_halfspace(point):
                                if self.hyperplanes[25].in_halfspace(point):
                                    return 5, 297, 7, [-1, -8, 3, -6, 16, 18, 25]
                                else:
                                    return 12, 296, 7, [-1, -8, 3, -6, 16, 18, -25]
                            else:
                                if self.hyperplanes[11].in_halfspace(point):
                                    return 9, 299, 7, [-1, -8, 3, -6, 16, -18, 11]
                                else:
                                    return 12, 298, 7, [-1, -8, 3, -6, 16, -18, -11]
                        else:
                            if self.hyperplanes[5].in_halfspace(point):
                                if self.hyperplanes[15].in_halfspace(point):
                                    return 7, 303, 7, [-1, -8, 3, -6, -16, 5, 15]
                                else:
                                    return 12, 302, 7, [-1, -8, 3, -6, -16, 5, -15]
                            else:
                                if self.hyperplanes[11].in_halfspace(point):
                                    return 9, 305, 7, [-1, -8, 3, -6, -16, -5, 11]
                                else:
                                    return 12, 304, 7, [-1, -8, 3, -6, -16, -5, -11]
                else:
                    if self.hyperplanes[4].in_halfspace(point):
                        if self.hyperplanes[5].in_halfspace(point):
                            if self.hyperplanes[17].in_halfspace(point):
                                if self.hyperplanes[18].in_halfspace(point):
                                    if self.hyperplanes[27].in_halfspace(point):
                                        return 4, 315, 8, [-1, -8, -3, 4, 5, 17, 18, 27]
                                    else:
                                        return 12, 314, 8, [-1, -8, -3, 4, 5, 17, 18, -27]
                                else:
                                    if self.hyperplanes[13].in_halfspace(point):
                                        return 8, 317, 8, [-1, -8, -3, 4, 5, 17, -18, 13]
                                    else:
                                        return 12, 316, 8, [-1, -8, -3, 4, 5, 17, -18, -13]
                            else:
                                if self.hyperplanes[2].in_halfspace(point):
                                    if self.hyperplanes[15].in_halfspace(point):
                                        return 7, 321, 8, [-1, -8, -3, 4, 5, -17, 2, 15]
                                    else:
                                        return 12, 320, 8, [-1, -8, -3, 4, 5, -17, 2, -15]
                                else:
                                    if self.hyperplanes[13].in_halfspace(point):
                                        return 8, 323, 8, [-1, -8, -3, 4, 5, -17, -2, 13]
                                    else:
                                        return 12, 322, 8, [-1, -8, -3, 4, 5, -17, -2, -13]
                        else:
                            if self.hyperplanes[23].in_halfspace(point):
                                return 6, 325, 6, [-1, -8, -3, 4, -5, 23]
                            else:
                                return 12, 324, 6, [-1, -8, -3, 4, -5, -23]
                    else:
                        if self.hyperplanes[2].in_halfspace(point):
                            if self.hyperplanes[25].in_halfspace(point):
                                return 5, 329, 6, [-1, -8, -3, -4, 2, 25]
                            else:
                                return 12, 328, 6, [-1, -8, -3, -4, 2, -25]
                        else:
                            if self.hyperplanes[23].in_halfspace(point):
                                return 6, 331, 6, [-1, -8, -3, -4, -2, 23]
                            else:
                                return 12, 330, 6, [-1, -8, -3, -4, -2, -23]
