"""
ベクトルの基本演算たち詰め合わせ

rotate_complex(p, deg):
    点の回転

norm_complex(p):
    ベクトルの大きさの二乗

phase_diff_complex(p1, p2):
    偏角の差

dot_product_complex(p1, p2):
    ベクトルの内積

area_of_parallelogram_complex(p1, p2):
    ベクトルの張る平行四辺形の面積、外積ベクトルの大きさ

orthogonal_p_complex(p1, p2):
    ベクトルの直交判定

parallel_p_complex(p1, p2):
    ベクトルの平行判定

projection_complex(p1, p2, target):
    点の直線への射影（垂線の足）

reflection_complex(p1, p2, target):
    点の直線への反射（対称位置）
"""


from typing import Union
import math
import cmath

Num = Union[int, float]
eps = 1e-10



def equals(x: Num, y: Num) -> bool:
    return abs(x - y) < eps


def rotate_complex(p: complex, deg: Num) -> complex:
    """
    点 P を deg だけ原点中心に反時計回りに回転させる (複素平面 ver.)
    """
    rad = math.radians(deg)
    return p * complex(math.cos(rad), math.sin(rad))


def norm_complex(p: complex) -> Num:
    """
    p ベクトルの大きさの二乗を求める (複素平面 ver.)
    """
    return p.real ** 2 + p.imag ** 2


def phase_diff_complex(p1: complex, p2: complex) -> Num:
    """
    p1 ベクトルと p2 ベクトルの偏角の差を計算する（p2 ベクトルを何度反時計回りに回転すると p1 ベクトルと方向が一致するか） (複素平面 ver.)
    戻り値は degree (0 <= degree <= 360)
    """
    return math.degrees(cmath.phase(p1) - cmath.phase(p2)) % 360



def dot_product_complex(p1: complex, p2: complex) -> Num:
    """
    p1 ベクトルと p2 ベクトルの内積を計算する (複素平面 ver.)
    Note:
        a・b = (a1i + a2j)・(b1i + b2j)
             = a1b1 + a2b2
    """
    return p1.real * p2.real + p1.imag * p2.imag
    


def area_of_parallelogram_complex(p1: complex, p2: complex) -> Num:
    """
    p1 ベクトルと p2 ベクトルで張られる平行四辺形の面積を計算する (複素平面 ver.)
    三角形の面積の場合は 2 で割る
    Note:
        S = |a| * |b| * sinθ
          = √(|a|^2|b|^2 - (a・b)^2)
          = √(a1^2 + a2^2) (b1^2 + b2^2) - (a1b1 + a2b2)^2)
          = √((a1b2 - a2b1)^2)
          = |a1b2 - a2b1|
          (3 次元空間での外積ベクトルを考えると z = (0, 0, a1b2 - a2b1) となり a, b, z は右手系をなす。
           外積の大きさは a, b で張られる平行四辺形の符号付き面積であり、a, b が反時計回りの関係にあるとき正となる)
    """
    return abs(p1.real * p2.imag - p1.imag * p2.real)



def orthogonal_p_complex(p1: complex, p2: complex) -> bool:
    """
    p1 ベクトルと p2 ベクトルが直交しているか判定する (複素平面 ver.)
    Note:
        内積が誤差を考慮した上で 0
    """
    return equals(dot_product_complex(p1, p2), 0.0)


def parallel_p_complex(p1: complex, p2: complex) -> bool:
    """
    p1 ベクトルと p2 ベクトルが平行であるか判定する (複素平面 ver.)
    Note:
        外積のベクトルの大きさが誤差を考慮した上で 0
    """
    return equals(area_of_parallelogram_complex(p1, p2), 0.0)



def projection_complex(p1: complex, p2: complex, target: complex) -> complex:
    """
    直線 P1P2 に対する 点 target の射影（垂線の足）を計算する (複素平面 ver.)
    Note:
        target を点 Q, Q の p1p2 への射影を X とする
        vec<P1P2> / |vec<P1P2>| (単位方向ベクトル) を u とする
        vec<OX> = vec<OP1> + vec<P1X>
                = vec<OP1> + |vec<P1X>| * u
                = vec<OP1> + (vec<P1Q>・u) * u
    """
    return p1 + (dot_product_complex(target - p1, p2 - p1) / norm_complex(p2 - p1)) * (p2 - p1)


def reflection_complex(p1: complex, p2: complex, target: complex) -> complex:
    """
    直線 P1P2 に対する 点 target の反射（対称位置）を計算する (複素平面 ver.)
    Note:
        target を点 Q, Q の p1p2 に対する反射を X とする
        Q から P1P2 に下ろした垂線の足を H とする
        vec<OX> = vec<OQ> + 2 * vec<QH>
                = vec<OQ> + 2 * (vec<OH> - vec<OQ>)
                = 2 * vec<OH> - vec<OQ>
    """
    return 2 * projection_complex(p1, p2, target) - target

