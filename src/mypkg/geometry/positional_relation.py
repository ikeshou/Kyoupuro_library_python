"""
図形の位置関係詰め合わせ

ccw(p1, p2, target):
    点の位置が反時計回りか判定

intersect_p_complex(p1, p2, p3, p4):
    線分同士の交差判定

crosspoint_of_segments_complex(p1, p2, p3, p4):
    線分の交点

commonpoint_of_line_circle_complex(p1, p2, c, radius):
    円と直線の共有点

commonpoint_of_circles_complex(c1, r1, c2, r2):
    円と円の共有点

dist_between_point_line_complex(p1, p2, target):
    点と直線の距離

dist_between_point_segment_complex(p1, p2, target):
    点と線分の距離

dist_between_segments_complex(p1, p2, p3, p4):
    線分同士の距離
"""



from typing import Union, Tuple
import math
import cmath
from .vector import equals, norm_complex, phase_diff_complex, dot_product_complex, area_of_parallelogram_complex, projection_complex

Num = Union[int, float]
eps = 1e-10



def ccw(p1: complex, p2: complex, target: complex) -> Num:
    """
    (target の点を Q として) P1P2 に対し P1Q が counter-clockwise か判定する
    vec<P1P2> と vec<P1Q> が反時計回りの関係にあるとき正、時計回りの関係にあるとき負、方向ベクトル共通の場合 0 を返す

    Note:
        これは符号付き面積を用いて計算することができる
        S = a1b2 - a2b1
    """
    S = (p2-p1).real * (target-p1).imag - (p2-p1).imag * (target-p1).real
    return 0 if equals(S, 0.0) else S



# verified @ABC016D
def intersect_p_complex(p1: complex, p2: complex, p3: complex, p4: complex) -> bool:
    """
    線分 P1P2 と線分 P3P4 が交差するか判定する (複素平面 ver.)

    Note:
        u, v を通る直線は変数 x, y として (v.x - u.x) * (y - u.y) = (v.y - u.y) * (x - u.x) と表される
        target の座標をこの式に代入した時の不等号の向きで線分により分たれるどの領域にいるかが判定可能と考えても良い。
        符号付き面積をもとにした counter_clock_wise 関数をベースに考えても良い。
        どちらにせよ、
        「P1, P2 を通る直線に対し P3, P4 が違う側に存在」かつ「P3, P4 を通る直線に対し P1, P2 が違う側にいる」=> 線分は交差する
    """
    t1 = ccw(p1, p2, p3)
    t2 = ccw(p1, p2, p4)
    t3 = ccw(p3, p4, p1)
    t4 = ccw(p3, p4, p2)
    return t1 * t2 < 0 and t3 * t4 < 0



def crosspoint_of_segments_complex(p1: complex, p2: complex, p3: complex, p4: complex) -> complex:
    """
    線分 P1P2 と線分 P3P4 の交点を求める (複素平面 ver.)
    Raises:
        ValueError: P1P2 と P3P4 が交差しないとき
    Note:
        交点 X, P1 から P3P4 に下ろした垂線の足を H1, P2 から P3P4 に下ろした垂線の足を H2 とする
        X は P1P2 を |vec<P1H1>| : |vec<P2H2>| に内分する点である
        位置ベクトルの内分公式により
        vec<OX> = a * vec<OP1> + b * vec<OP2>
        ただし a = (|vec<P1H2>| / (|vec<P1H1>| + |vec<P2H2>|)), b = (|vec<P1H1>| / (|vec<P1H1>| + |vec<P2H2>|))
    """
    if not intersect_p_complex(p1, p2, p3, p4):
        raise ValueError(f"crosspoint_segments_complex(): segment and segment do not crossed. got L1: {p1}, {p2}. L2: {p3}, {p4}")
    d1 = area_of_parallelogram_complex(p1 - p3, p4 - p3) / abs(p4 - p3)
    d2 = area_of_parallelogram_complex(p2 - p3, p4 - p3) / abs(p4 - p3)
    return (d2 / (d1 + d2)) * p1 + (d1 / (d1 + d2)) * p2



def commonpoint_of_line_circle_complex(p1: complex, p2: complex, c: complex, radius: Num) -> Tuple[complex]:
    """
    直線 P1P2 と円 C の共有点を計算する (複素平面 ver.)
    Raise:
        ValueError: P1P2 と円 C が交差も接しもしないとき
    Note:
        交点の個数は縁の中心と直線に対し点と直線の距離の公式を適用し、半径と比較すれば自明
        交点 X, C から P1P2 へ下ろした垂線の足を H, vec<P1P2> の方向単位ベクトル u として
        vec<OX> = vec<OH> ± t * u
        ただし t = √(radius ^ 2 - |vec<CH>|^2) 
    """
    h = projection_complex(p1, p2, c)
    if radius ** 2 < norm_complex(h - c):
        raise ValueError(f"commonpoint_line_circle_complex(): line and circle do not crossed. got line: {p1}, {p2}. got circle: (center){c} (radius){radius}")
    coeff = math.sqrt(radius ** 2 - norm_complex(h - c))
    unit = (p2 - p1) / abs(p2 - p1)
    if equals(coeff, 0):
        return (h, )
    else:
        return (h + coeff * unit, h - coeff * unit)


def commonpoint_of_circles_complex(c1: complex, r1: Num, c2: complex, r2: Num) -> Tuple[complex]:
    """
    円 C1 と円 C2 の共有点を計算する (複素平面 ver.)
    Raise:
        ValueError: 円 C1 と円 C2 が交差も接しもしないとき
    Note:
        交点の個数は中心間の距離を半径と比較すれば自明
        共有点 X とする
        共有点が 2 個の場合、どのような位置関係でも三角形 C1C2X は三辺の長さが C1C2, C2X, XC1 である（鋭角三角形だったり鈍角三角形だったりする）
        いずれにせよ vec<OC1> がわかるため、vec<C1X> の偏角絶対値が分かれば良い。
        絶対値は r1。
        偏角は θ は arg(C1C2) = α, ∠XC1C2 = β として θ = α ± β. β は余弦定理を用いればわかる。
    """
    d = abs(c2 - c1)
    alpha = cmath.phase(c2 - c1)
    # 共有点 0 個
    if d > r1 + r2 or d < max(r1, r2) - min(r1, r2):
        raise ValueError(f"commonpoint_circles_complex(): circlues do not crossed. got C1: (center){c1}, (radius){r1}, C2: (center){c2} (radius){r2}")
    # 共有点 1 個
    elif equals(d, r1 + r2) or equals(d, max(r1, r2) - min(r1, r2)):
        return (c1 + cmath.rect(r1, alpha), )
    # 共有点 2 個
    else:
        beta = math.acos((r1 ** 2 + d ** 2 - r2 ** 2) / (2 * r1 * d))
        return (c1 + cmath.rect(r1, alpha + beta), c1 + cmath.rect(r1, alpha - beta))
    



def dist_between_point_line_complex(p1: complex, p2: complex, target: complex) -> Num:
    """
    直線 P1P2 と点 target の距離を計算する (複素平面 ver.)
    Note:
        target を点 Q, Q から P1P2 に下ろした垂線の足を H とする
        |vec<QH>| = (vec<P1Q>, vec<P1P2> で張られる平行四辺形の面積) / |vec<P1P2>|
    """
    return area_of_parallelogram_complex(target - p1, p2 - p1) / abs(p2 - p1)



def dist_between_point_segment_complex(p1: complex, p2: complex, target: complex) -> Num:
    """
    線分 P1P2 と点 target の距離を計算する (複素平面 ver.)
    Note:
            |            |
            |            |
        Q   |       Q    |   Q
            P1-----------P2
            |            |
            |            |
        x         y          z
        Q が領域 x に入っているときは P1Q, Q が領域 z に入っているときは P2Q, それ以外は点と直線の距離
    """
    if 90 <= phase_diff_complex(target - p1, p2 - p1) <= 270:
        return abs(target - p1) 
    elif 90 <= phase_diff_complex(target - p2, p1 - p2) <= 270:
        return abs(target - p2)
    else:
        return dist_between_point_line_complex(p1, p2, target)



def dist_between_segments_complex(p1: complex, p2: complex, p3: complex, p4: complex) -> Num:
    """
    線分 P1P2 と線分 P3P4 の最短距離を計算する (複素平面 ver.)
    Note:
        交差する場合は 0
        交差しない場合は
        1. 線分 P1P2 と P3 の距離
        2. 線分 P1P2 と P4 の距離
        3. 線分 P3P4 と P1 の距離
        4. 線分 P3P4 と P2 の距離
        の最小値である
    """
    if intersect_p_complex(p1, p2, p3, p4):
        return 0
    else:
        return min(dist_between_point_segment_complex(p1, p2, p3),
                   dist_between_point_segment_complex(p1, p2, p4),
                   dist_between_point_segment_complex(p3, p4, p1),
                   dist_between_point_segment_complex(p3, p4, p2))

