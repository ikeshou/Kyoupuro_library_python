import pytest
import math, cmath
from mypkg.geometry.vector import equals, rotate_complex, norm_complex, phase_diff_complex, dot_product_complex, area_of_parallelogram_complex, orthogonal_p_complex, parallel_p_complex, projection_complex, reflection_complex


def test_equals():
    # test for equals
    assert (equals(0.1, 0.1))
    assert (equals(1.0, 1.0-1e-15))
    assert (equals(1.0, 1.0-1e-5) is False)
    assert (equals(-2.0, -2.0+1e-15))
    assert (equals(-2.0, -2.0+1e-5) is False)
    # print("- test for equals() passed.")


def test_rotate_complex():
    # test for rotate_complex
    assert (equals(math.degrees(cmath.phase(rotate_complex(1.0+1.0j, 45))), 90))
    assert (equals(math.degrees(cmath.phase(rotate_complex(1.0+1.0j, -45))), 0))
    assert (equals(rotate_complex(3.0+4.0j, 180).real, -3.0))
    assert (equals(rotate_complex(3.0+4.0j, 180).real, -3.0))
    assert (equals(rotate_complex(1.0+0.0j, 90).real, 0.0))
    assert (equals(rotate_complex(1.0+0.0j, 90).imag, 1.0))
    assert (equals(rotate_complex(3.0+5.0j, 360).real, 3.0))
    assert (equals(rotate_complex(3.0+5.0j, 360).imag, 5.0))
    assert (rotate_complex(3.0+5.0j, 0) == 3.0+5.0j)
    assert (rotate_complex(3.0+5.0j, 0) == 3.0+5.0j)
    assert (equals(abs(rotate_complex(cmath.rect(1.3, math.radians(35)), 52)), 1.3))
    assert (equals(math.degrees(cmath.phase(rotate_complex(cmath.rect(1.3, math.radians(35)), 52))), 87))
    # print("- test for rotate_complex() passed.")


def test_norm_complex():
    # test for norm_complex
    assert (equals(norm_complex(3.0+4.0j), 25.0))
    assert (equals(norm_complex(3.0-4.0j), 25.0))
    assert (equals(norm_complex(1.0+2.0j), 5.0))
    assert (equals(norm_complex(-1.0+2.0j), 5.0))
    assert (equals(norm_complex(-2.0-2.0j), 8.0))
    # print("- test for norm_complex() passed.")


def test_phase_diff_complex():
    # test for phase_diff_complex
    assert (equals(phase_diff_complex(1.0+1.0j, 1.0+0.0j), 45.0))
    assert (equals(phase_diff_complex(1.0+0.0j, 1.0+1.0j), 315.0))
    assert (equals(phase_diff_complex(1.0+1.0j, -2.0+2.0j), 270.0))
    assert (equals(phase_diff_complex(1.0+1.0j, 2.0-2.0j), 90.0))
    assert (equals(phase_diff_complex(3.0+4.0j, 3.0+4.0j), 0.0))
    # print("- test for phase_diff_complex() passed.")


def test_dot_product_complex():
    # test for dot_product_complex
    assert (equals(dot_product_complex(2.0+3.0j, 4.0+5.0j), 23.0))
    assert (equals(dot_product_complex(0+0j, 100+100j), 0))
    assert (equals(dot_product_complex(1.0+1.0j, 2.0+2.0j), 4.0))    # 平行
    assert (equals(dot_product_complex(1000+0j, 0+100j), 0))    # 直交
    # print("- test for dot_product_complex() passed.")


def test_area_of_parallelogram_complex():
    # test for area_of_parallelogram_complex
    assert (equals(area_of_parallelogram_complex(3.0+4.0j, 5.0+6.0j), 2.0))
    assert (equals(area_of_parallelogram_complex(1.0+3.0j, 5.0+7.0j), 8.0))
    assert (equals(area_of_parallelogram_complex(-1.0-2.0j, -2.0-4.0j), 0))    # 直線
    assert (equals(area_of_parallelogram_complex(2.0+3.0j, -3.0+2.0j), 13.0))    # 長方形
    # print("- test for area_of_parallelogram_complex() passed.")


def test_orthogonal_p_complex():
    # test for orthogonal_p_complex
    assert (orthogonal_p_complex(1.0+1.0j, 1.0-1.0j))
    assert (orthogonal_p_complex(1.0+1.0j, -1.0+1.0j))
    assert (orthogonal_p_complex(1.0+1.0j, -1.0-1.0j) is False)
    assert (orthogonal_p_complex(1.0+1.0j, 1.0+1.0j) is False)
    # print("- test for orthogonal_p_complex() passed.")


def test_parallel_p_complex():
    # test for parallel_p_complex
    assert (parallel_p_complex(1.0+1.0j, 5.0+5.0j))
    assert (parallel_p_complex(3.0+5.0j, 1.5+2.5j))
    assert (parallel_p_complex(1.0+1.0j, -1.0-1.0j))
    assert (parallel_p_complex(1.0+1.0j, 1.0+1.0j))
    assert (parallel_p_complex(1.0+1.0j, 1.0-1.0j) is False)
    # print("- test for parallel_p_complex() passed.")


def test_projection_complex():
    # test for projection_complex
    assert (equals(projection_complex(2.0-1.0j, 5.0-3.0j, 4.0+5.0j).real, 8/13))    # (4,5) から 2x+3y-1=0 への射影
    assert (equals(projection_complex(2.0-1.0j, 5.0-3.0j, 4.0+5.0j).imag, -1/13))
    assert (equals(projection_complex(1.0+1.0j, 3.0+3.0j, 2.0+2.0j).real, 2.0))    # そもそも直線上
    assert (equals(projection_complex(1.0+1.0j, 3.0+3.0j, 2.0+2.0j).imag, 2.0))
    # print("- test for projection_complex() passed.")


def test_reflection_complex():
    # test for reflection_complex
    assert (equals(reflection_complex(2.0+5.5j, 1.0+3.5j, -2.0+4.0j).real, 16/5))    # (-2, 4) からの 4x-2y+3=0 に対する反射
    assert (equals(reflection_complex(2.0+5.5j, 1.0+3.5j, -2.0+4.0j).imag, 7/5))
    assert (equals(reflection_complex(1.0+1.0j, 3.0+3.0j, 2.0+2.0j).real, 2.0))    # そもそも直線上
    assert (equals(reflection_complex(1.0+1.0j, 3.0+3.0j, 2.0+2.0j).imag, 2.0))
    # print("- test for reflection_complex() passed.")




if __name__ == "__main__":
    pytest.main(['-v', __file__])
