import pytest
import math, cmath
from mypkg.geometry.vector import equals
from mypkg.geometry.positional_relation import ccw, intersect_p_complex, crosspoint_of_segments_complex, commonpoint_of_line_circle_complex, commonpoint_of_circles_complex, dist_between_point_line_complex, dist_between_point_segment_complex, dist_between_segments_complex


def test_ccw():
    # test for ccw
    assert (equals(ccw(0+0j, 1+1j, -1+1j), 2.0))
    assert (equals(ccw(0+0j, -1+1j, 1+1j), -2.0))
    assert (equals(ccw(1+1j, 2+2j, 3+3j), 0))
    # print("- test for ccw() passed.")    


def test_intersect_p_complex():
    # test for intersect_p_complex
    assert (intersect_p_complex(0+0j, 2+0j, 1+1j, 1-1j) == True)    # y = 0 と x = 1 は (1, 0) で交差する。交点はどちらの線分上でもある
    assert (intersect_p_complex(0+0j, 1+0j, 1+1j, 1-1j) == False)    # T 字型なので線分は交差していない
    assert (intersect_p_complex(1+0j, 2+0j, 1+1j, 1-1j) == False)    # T 字型
    assert (intersect_p_complex(0+1j, 2+1j, 1+1j, 1-1j) == False)    # T 字型   
    assert (intersect_p_complex(0-1j, 2-1j, 1+1j, 1+0j) == False)   # 直線の交点は線分上にない
    assert (intersect_p_complex(4+3j, 2+7j, 1+3j, 8+10j) == True)    # y = -2x + 11 と y = x + 2 は (3, 5) で交差する。交点はどちらの線分上でもある
    assert (intersect_p_complex(3+5j, 2+7j, 1+3j, 8+10j) == False)   # T 字型なので線分は交差していない
    assert (intersect_p_complex(4+3j, 2+7j, 1+3j, 2+4j) == False)   # 直線の交点は線分上にない
    assert (intersect_p_complex(1+2j, 3+4j, 1+3j, 3+5j) == False)    # y = x + 1 と y = x + 2 は平行。当然直線すら交わることはない 
    # print("- test for intersect_p_complex() passed.")    


def test_cross_point_of_segments_complex():
    # test for crosspoint_of_segments_complex
    assert (equals(crosspoint_of_segments_complex(-1-1j, 1+3j, -1+1j, 1-1j).real, -1/3))    # y = 2x + 1 と y = -x の交点 (-1/3, 1/3)
    assert (equals(crosspoint_of_segments_complex(-1-1j, 1+3j, -1+1j, 1-1j).imag, 1/3))
    # print("- test for crosspoint_of_segments_complex() passed.")


def test_commonpoint_of_line_circle_complex():
    # test for commonpoint_of_line_circle_complex
    c1, c2 = commonpoint_of_line_circle_complex(0+1j, 1+2j, 0+0j, 1)    # x^2+y^2=1 と y=x+1 の交点 (0,1), (-1,0)
    assert (equals(c1.real, 0))
    assert (equals(c1.imag, 1))
    assert (equals(c2.real, -1))
    assert (equals(c2.imag, 0))
    # print("- test for commonpoint_of_line_circle_complex() passed.")


def test_commonpoint_of_circles_complex():
    # test for commonpoint_of_circles_complex
    c1, c2 = commonpoint_of_circles_complex(0+1j, 5, 4+3j, math.sqrt(5))    # x^2 + (y-1)^2 = 25, (x-4)^2 + (y-3)^2 = 5 の交点 (3,5), (5,1)
    assert (equals(c1.real, 3))
    assert (equals(c1.imag, 5))
    assert (equals(c2.real, 5))
    assert (equals(c2.imag, 1))
    # print("- test for commonpoint_of_circles_complex() passed.")


def test_dist_between_point_line_complex():
    # test for dist_between_point_line_complex
    assert (equals(dist_between_point_line_complex(0+0j, complex(1, math.sqrt(3)), 2+0j), math.sqrt(3)))    # y = √3x と (2, 0) の距離 √3
    assert (equals(dist_between_point_line_complex(0+0j, 0+1j, 2+0j), 2))    # y 軸と (2, 0) の距離 2
    assert (equals(dist_between_point_line_complex(0+0j, 0+1j, 0+3j), 0))    # on line
    # print("- test for dist_between_point_line_complex() passed.")


def test_dist_between_point_segment_complex():
    # test for dist_between_point_segment_complex
    assert (equals(dist_between_point_segment_complex(0+0j, 10+20j, 3+1j), math.sqrt(5)))    # 直線 y=2x と (3,1) の距離は √5 だが
    assert (equals(dist_between_point_segment_complex(0+0j, -1-2j, 3+1j), math.sqrt(10)))    # このような線分になると (0, 0) との距離が最短となる
    assert (equals(dist_between_point_segment_complex(5+10j, 10+20j, 3+1j), math.sqrt(85)))    # このような線分になると (5, 10) との距離が最短となる
    assert (equals(dist_between_point_segment_complex(0+0j, 0+10j, 0+5j), 0))    # on segment
    # print("- test for dist_between_point_segment() passed.")


def test_dist_between_segments_complex():
    # test for dist_between_segments_complex
    assert (equals(dist_between_segments_complex(0+0j, 2+2j, 0+2j, 2+0j), 0))    # 線分が交わる
    assert (equals(dist_between_segments_complex(0+0j, 10+0j, 5+5j, 5+6j), 5))
    assert (equals(dist_between_segments_complex(0+0j, 0+10j, 5+5j, 5+6j), 5))
    # print("- test for dist_between_segments_complex() passed.")





if __name__ == "__main__":
    pytest.main(['-v', __file__])
