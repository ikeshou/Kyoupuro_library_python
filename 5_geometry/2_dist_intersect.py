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

Num = Union[int, float]
eps = 1e-10


# ==================================
# defined in 1_vec.py

def equals(x: Num, y: Num) -> bool:
    return abs(x - y) < eps

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
    """
    return abs(p1.real * p2.imag - p1.imag * p2.real)

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

# ==================================




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





if __name__ == "__main__":

    # test for ccw
    assert (equals(ccw(0+0j, 1+1j, -1+1j), 2.0))
    assert (equals(ccw(0+0j, -1+1j, 1+1j), -2.0))
    assert (equals(ccw(1+1j, 2+2j, 3+3j), 0))
    print("- test for ccw() passed.")

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
    print("- test for intersect_p_complex() passed.")

    # test for crosspoint_of_segments_complex
    assert (equals(crosspoint_of_segments_complex(-1-1j, 1+3j, -1+1j, 1-1j).real, -1/3))    # y = 2x + 1 と y = -x の交点 (-1/3, 1/3)
    assert (equals(crosspoint_of_segments_complex(-1-1j, 1+3j, -1+1j, 1-1j).imag, 1/3))
    print("- test for crosspoint_of_segments_complex() passed.")

    # test for commonpoint_of_line_circle_complex
    c1, c2 = commonpoint_of_line_circle_complex(0+1j, 1+2j, 0+0j, 1)    # x^2+y^2=1 と y=x+1 の交点 (0,1), (-1,0)
    assert (equals(c1.real, 0))
    assert (equals(c1.imag, 1))
    assert (equals(c2.real, -1))
    assert (equals(c2.imag, 0))
    print("- test for commonpoint_of_line_circle_complex() passed.")

    # test for commonpoint_of_circles_complex
    c1, c2 = commonpoint_of_circles_complex(0+1j, 5, 4+3j, math.sqrt(5))    # x^2 + (y-1)^2 = 25, (x-4)^2 + (y-3)^2 = 5 の交点 (3,5), (5,1)
    assert (equals(c1.real, 3))
    assert (equals(c1.imag, 5))
    assert (equals(c2.real, 5))
    assert (equals(c2.imag, 1))
    print("- test for commonpoint_of_circles_complex() passed.")

    # test for dist_between_point_line_complex
    assert (equals(dist_between_point_line_complex(0+0j, complex(1, math.sqrt(3)), 2+0j), math.sqrt(3)))    # y = √3x と (2, 0) の距離 √3
    assert (equals(dist_between_point_line_complex(0+0j, 0+1j, 2+0j), 2))    # y 軸と (2, 0) の距離 2
    assert (equals(dist_between_point_line_complex(0+0j, 0+1j, 0+3j), 0))    # on line
    print("- test for dist_between_point_line_complex() passed.")

    # test for dist_between_point_segment_complex
    assert (equals(dist_between_point_segment_complex(0+0j, 10+20j, 3+1j), math.sqrt(5)))    # 直線 y=2x と (3,1) の距離は √5 だが
    assert (equals(dist_between_point_segment_complex(0+0j, -1-2j, 3+1j), math.sqrt(10)))    # このような線分になると (0, 0) との距離が最短となる
    assert (equals(dist_between_point_segment_complex(5+10j, 10+20j, 3+1j), math.sqrt(85)))    # このような線分になると (5, 10) との距離が最短となる
    assert (equals(dist_between_point_segment_complex(0+0j, 0+10j, 0+5j), 0))    # on segment
    print("- test for dist_between_point_segment() passed.")

    # test for dist_between_segments_complex
    assert (equals(dist_between_segments_complex(0+0j, 2+2j, 0+2j, 2+0j), 0))    # 線分が交わる
    assert (equals(dist_between_segments_complex(0+0j, 10+0j, 5+5j, 5+6j), 5))
    assert (equals(dist_between_segments_complex(0+0j, 0+10j, 5+5j, 5+6j), 5))
    print("- test for dist_between_segments_complex() passed.")


    print(" * assertion test ok * ")
