from typing import Dict

from tinypy.geometry.hyperplane import Hyperplane
from tinypy.geometry.point import Point
from tinypy.polytopes.base_polytope import Polytope


class TSPTree:

    polytope: Polytope
    hyperplanes: Dict[int, Hyperplane]

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
                                return 12
                            else:
                                return 6
                        else:
                            if self.hyperplanes[16].in_halfspace(point):
                                if self.hyperplanes[15].in_halfspace(point):
                                    return 12
                                else:
                                    return 7
                            else:
                                if self.hyperplanes[25].in_halfspace(point):
                                    return 12
                                else:
                                    return 5
                    else:
                        if self.hyperplanes[5].in_halfspace(point):
                            if self.hyperplanes[23].in_halfspace(point):
                                return 12
                            else:
                                return 6
                        else:
                            if self.hyperplanes[18].in_halfspace(point):
                                if self.hyperplanes[13].in_halfspace(point):
                                    return 12
                                else:
                                    return 8
                            else:
                                if self.hyperplanes[27].in_halfspace(point):
                                    return 12
                                else:
                                    return 4
                else:
                    if self.hyperplanes[6].in_halfspace(point):
                        if self.hyperplanes[16].in_halfspace(point):
                            if self.hyperplanes[5].in_halfspace(point):
                                if self.hyperplanes[11].in_halfspace(point):
                                    return 12
                                else:
                                    return 9
                            else:
                                if self.hyperplanes[15].in_halfspace(point):
                                    return 12
                                else:
                                    return 7
                        else:
                            if self.hyperplanes[18].in_halfspace(point):
                                if self.hyperplanes[11].in_halfspace(point):
                                    return 12
                                else:
                                    return 9
                            else:
                                if self.hyperplanes[25].in_halfspace(point):
                                    return 12
                                else:
                                    return 5
                    else:
                        if self.hyperplanes[19].in_halfspace(point):
                            if self.hyperplanes[15].in_halfspace(point):
                                return 12
                            else:
                                return 7
                        else:
                            if self.hyperplanes[29].in_halfspace(point):
                                return 12
                            else:
                                return 3
            else:
                if self.hyperplanes[10].in_halfspace(point):
                    if self.hyperplanes[4].in_halfspace(point):
                        if self.hyperplanes[2].in_halfspace(point):
                            if self.hyperplanes[19].in_halfspace(point):
                                if self.hyperplanes[9].in_halfspace(point):
                                    return 12
                                else:
                                    return 10
                            else:
                                if self.hyperplanes[23].in_halfspace(point):
                                    return 12
                                else:
                                    return 6
                        else:
                            if self.hyperplanes[16].in_halfspace(point):
                                if self.hyperplanes[15].in_halfspace(point):
                                    return 12
                                else:
                                    return 7
                            else:
                                if self.hyperplanes[25].in_halfspace(point):
                                    return 12
                                else:
                                    return 5
                    else:
                        if self.hyperplanes[5].in_halfspace(point):
                            if self.hyperplanes[19].in_halfspace(point):
                                if self.hyperplanes[9].in_halfspace(point):
                                    return 12
                                else:
                                    return 10
                            else:
                                if self.hyperplanes[23].in_halfspace(point):
                                    return 12
                                else:
                                    return 6
                        else:
                            if self.hyperplanes[18].in_halfspace(point):
                                if self.hyperplanes[6].in_halfspace(point):
                                    if self.hyperplanes[9].in_halfspace(point):
                                        return 12
                                    else:
                                        return 10
                                else:
                                    if self.hyperplanes[13].in_halfspace(point):
                                        return 12
                                    else:
                                        return 8
                            else:
                                if self.hyperplanes[21].in_halfspace(point):
                                    if self.hyperplanes[9].in_halfspace(point):
                                        return 12
                                    else:
                                        return 10
                                else:
                                    if self.hyperplanes[27].in_halfspace(point):
                                        return 12
                                    else:
                                        return 4
                else:
                    if self.hyperplanes[12].in_halfspace(point):
                        if self.hyperplanes[2].in_halfspace(point):
                            if self.hyperplanes[19].in_halfspace(point):
                                return 10
                            else:
                                return 6
                        else:
                            if self.hyperplanes[16].in_halfspace(point):
                                if self.hyperplanes[5].in_halfspace(point):
                                    if self.hyperplanes[3].in_halfspace(point):
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 12
                                        else:
                                            return 10
                                    else:
                                        if self.hyperplanes[11].in_halfspace(point):
                                            return 12
                                        else:
                                            return 9
                                else:
                                    if self.hyperplanes[15].in_halfspace(point):
                                        return 12
                                    else:
                                        return 7
                            else:
                                if self.hyperplanes[18].in_halfspace(point):
                                    if self.hyperplanes[3].in_halfspace(point):
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 12
                                        else:
                                            return 10
                                    else:
                                        if self.hyperplanes[11].in_halfspace(point):
                                            return 12
                                        else:
                                            return 9
                                else:
                                    if self.hyperplanes[20].in_halfspace(point):
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 12
                                        else:
                                            return 10
                                    else:
                                        if self.hyperplanes[25].in_halfspace(point):
                                            return 12
                                        else:
                                            return 5
                    else:
                        if self.hyperplanes[14].in_halfspace(point):
                            if self.hyperplanes[16].in_halfspace(point):
                                if self.hyperplanes[4].in_halfspace(point):
                                    if self.hyperplanes[3].in_halfspace(point):
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 12
                                        else:
                                            return 10
                                    else:
                                        return 9
                                else:
                                    if self.hyperplanes[6].in_halfspace(point):
                                        return 10
                                    else:
                                        return 8
                            else:
                                if self.hyperplanes[17].in_halfspace(point):
                                    if self.hyperplanes[3].in_halfspace(point):
                                        if self.hyperplanes[9].in_halfspace(point):
                                            return 12
                                        else:
                                            return 10
                                    else:
                                        return 9
                                else:
                                    if self.hyperplanes[19].in_halfspace(point):
                                        return 10
                                    else:
                                        return 6
                        else:
                            if self.hyperplanes[22].in_halfspace(point):
                                if self.hyperplanes[7].in_halfspace(point):
                                    return 10
                                else:
                                    return 7
                            else:
                                if self.hyperplanes[28].in_halfspace(point):
                                    return 10
                                else:
                                    return 2
        else:
            if self.hyperplanes[9].in_halfspace(point):
                if self.hyperplanes[3].in_halfspace(point):
                    if self.hyperplanes[5].in_halfspace(point):
                        if self.hyperplanes[22].in_halfspace(point):
                            return 11
                        else:
                            return 6
                    else:
                        if self.hyperplanes[18].in_halfspace(point):
                            if self.hyperplanes[12].in_halfspace(point):
                                return 11
                            else:
                                return 8
                        else:
                            if self.hyperplanes[26].in_halfspace(point):
                                return 11
                            else:
                                return 4
                else:
                    if self.hyperplanes[6].in_halfspace(point):
                        if self.hyperplanes[2].in_halfspace(point):
                            if self.hyperplanes[22].in_halfspace(point):
                                return 11
                            else:
                                return 6
                        else:
                            if self.hyperplanes[18].in_halfspace(point):
                                if self.hyperplanes[10].in_halfspace(point):
                                    return 11
                                else:
                                    return 9
                            else:
                                if self.hyperplanes[24].in_halfspace(point):
                                    return 11
                                else:
                                    return 5
                    else:
                        if self.hyperplanes[7].in_halfspace(point):
                            if self.hyperplanes[16].in_halfspace(point):
                                if self.hyperplanes[4].in_halfspace(point):
                                    if self.hyperplanes[10].in_halfspace(point):
                                        return 11
                                    else:
                                        return 9
                                else:
                                    if self.hyperplanes[12].in_halfspace(point):
                                        return 11
                                    else:
                                        return 8
                            else:
                                if self.hyperplanes[17].in_halfspace(point):
                                    if self.hyperplanes[10].in_halfspace(point):
                                        return 11
                                    else:
                                        return 9
                                else:
                                    if self.hyperplanes[22].in_halfspace(point):
                                        return 11
                                    else:
                                        return 6
                        else:
                            if self.hyperplanes[19].in_halfspace(point):
                                if self.hyperplanes[14].in_halfspace(point):
                                    return 11
                                else:
                                    return 7
                            else:
                                if self.hyperplanes[28].in_halfspace(point):
                                    return 11
                                else:
                                    return 3
            else:
                if self.hyperplanes[11].in_halfspace(point):
                    if self.hyperplanes[4].in_halfspace(point):
                        if self.hyperplanes[2].in_halfspace(point):
                            if self.hyperplanes[19].in_halfspace(point):
                                if self.hyperplanes[8].in_halfspace(point):
                                    return 11
                                else:
                                    return 10
                            else:
                                if self.hyperplanes[22].in_halfspace(point):
                                    return 11
                                else:
                                    return 6
                        else:
                            if self.hyperplanes[16].in_halfspace(point):
                                return 7
                            else:
                                return 5
                    else:
                        if self.hyperplanes[5].in_halfspace(point):
                            if self.hyperplanes[16].in_halfspace(point):
                                if self.hyperplanes[6].in_halfspace(point):
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 11
                                    else:
                                        return 10
                                else:
                                    if self.hyperplanes[12].in_halfspace(point):
                                        return 11
                                    else:
                                        return 8
                            else:
                                if self.hyperplanes[19].in_halfspace(point):
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 11
                                    else:
                                        return 10
                                else:
                                    if self.hyperplanes[22].in_halfspace(point):
                                        return 11
                                    else:
                                        return 6
                        else:
                            if self.hyperplanes[18].in_halfspace(point):
                                return 8
                            else:
                                return 4
                else:
                    if self.hyperplanes[15].in_halfspace(point):
                        if self.hyperplanes[16].in_halfspace(point):
                            if self.hyperplanes[4].in_halfspace(point):
                                if self.hyperplanes[3].in_halfspace(point):
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 11
                                    else:
                                        return 10
                                else:
                                    if self.hyperplanes[10].in_halfspace(point):
                                        return 11
                                    else:
                                        return 9
                            else:
                                if self.hyperplanes[6].in_halfspace(point):
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 11
                                    else:
                                        return 10
                                else:
                                    if self.hyperplanes[12].in_halfspace(point):
                                        return 11
                                    else:
                                        return 8
                        else:
                            if self.hyperplanes[17].in_halfspace(point):
                                if self.hyperplanes[3].in_halfspace(point):
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 11
                                    else:
                                        return 10
                                else:
                                    if self.hyperplanes[10].in_halfspace(point):
                                        return 11
                                    else:
                                        return 9
                            else:
                                if self.hyperplanes[19].in_halfspace(point):
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 11
                                    else:
                                        return 10
                                else:
                                    if self.hyperplanes[22].in_halfspace(point):
                                        return 11
                                    else:
                                        return 6
                    else:
                        if self.hyperplanes[25].in_halfspace(point):
                            if self.hyperplanes[4].in_halfspace(point):
                                if self.hyperplanes[3].in_halfspace(point):
                                    return 10
                                else:
                                    if self.hyperplanes[10].in_halfspace(point):
                                        return 11
                                    else:
                                        return 9
                            else:
                                if self.hyperplanes[6].in_halfspace(point):
                                    return 10
                                else:
                                    if self.hyperplanes[12].in_halfspace(point):
                                        return 11
                                    else:
                                        return 8
                        else:
                            if self.hyperplanes[27].in_halfspace(point):
                                if self.hyperplanes[3].in_halfspace(point):
                                    return 10
                                else:
                                    if self.hyperplanes[10].in_halfspace(point):
                                        return 11
                                    else:
                                        return 9
                            else:
                                if self.hyperplanes[29].in_halfspace(point):
                                    if self.hyperplanes[8].in_halfspace(point):
                                        return 11
                                    else:
                                        return 10
                                else:
                                    return 1
