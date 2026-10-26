"""Independent exact audit of PR5618's projector/rank bridge.

Written for MatShep with substantial OpenAI Codex assistance. Apache-2.0.
No executable from the audited package or its predecessors is imported.
"""
from collections import Counter, defaultdict
from fractions import Fraction as Q
from hashlib import sha256
import gzip
import json
from math import lcm
from pathlib import Path
import sys
from itertools import permutations

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
INPUT = ROOT / 'research/p2-full-history-deficit/inputs'


def require(ok, message):
    if not ok:
        raise ValueError(message)


def transpose(a):
    return [list(row) for row in zip(*a)]


def multiply(a, b):
    out = [[0] * len(b[0]) for _ in a]
    for i, row in enumerate(a):
        for k, value in enumerate(row):
            if value:
                for j, other in enumerate(b[k]):
                    if other:
                        out[i][j] += value * other
    return out


def identity(n):
    return [[int(i == j) for j in range(n)] for i in range(n)]


def subtract(a, b):
    return [[x-y for x, y in zip(r, s)] for r, s in zip(a, b)]


def row_basis(a):
    pivots, original = {}, []
    for source in a:
        row = list(map(Q, source))
        for j, basis in pivots.items():
            if row[j]:
                z = row[j]
                row = [x-z*y for x, y in zip(row, basis)]
        j = next((j for j, x in enumerate(row) if x), None)
        if j is not None:
            z = row[j]
            pivots[j] = [x/z for x in row]
            original.append(list(map(Q, source)))
    return original


def inverse(a):
    n = len(a)
    unit = identity(n)
    aug = [list(map(Q, row)) + unit[i] for i, row in enumerate(a)]
    for j in range(n):
        k = next((k for k in range(j, n) if aug[k][j]), None)
        require(k is not None, 'Singular Gram matrix')
        aug[k], aug[j] = aug[j], aug[k]
        z = aug[j][j]
        aug[j] = [x/z for x in aug[j]]
        for k in range(n):
            if k != j and aug[k][j]:
                z = aug[k][j]
                aug[k] = [x-z*y for x, y in zip(aug[k], aug[j])]
    return [row[n:] for row in aug]


def scaled_projection(rows):
    basis = row_basis(rows)
    b = transpose(basis)
    r = multiply(multiply(b, inverse(multiply(basis, b))), basis)
    scale = 1
    for row in r:
        for x in row:
            scale = lcm(scale, x.denominator)
    ints = [[int(x*scale) for x in row] for row in r]
    check_projection(ints, scale, len(basis))
    return ints, scale, len(basis)


def check_projection(r, scale, rank):
    require(scale > 0 and r == transpose(r), 'Orthogonal projection must be symmetric')
    require(multiply(r, r) == [[scale*x for x in row] for row in r], 'Projection idempotence')
    require(sum(r[i][i] for i in range(len(r))) == rank*scale, 'Projection rank trace')


def binary_compose(a, b):
    out = []
    for row in a:
        value = 0
        for j in range(len(b)):
            if row >> j & 1:
                value ^= b[j]
        out.append(value)
    return tuple(out)


def binary_inverse(a):
    n = len(a)
    aug = [row | (1 << (n+i)) for i, row in enumerate(a)]
    for j in range(n):
        k = next((k for k in range(j, n) if aug[k] >> j & 1), None)
        require(k is not None, 'Singular binary normalizer')
        aug[k], aug[j] = aug[j], aug[k]
        for k in range(n):
            if k != j and aug[k] >> j & 1:
                aug[k] ^= aug[j]
    result = tuple(row >> n for row in aug)
    require(binary_compose(a, result) == tuple(1 << i for i in range(n)), 'Binary inverse check')
    return result


def embed(a, axes, n=17):
    out = [1 << i for i in range(n)]
    for i, axis in enumerate(axes):
        out[axis] = sum(((a[i] >> j) & 1) << other for j, other in enumerate(axes))
    return tuple(out)


def pair_partition(ws):
    inverses = [binary_inverse(w) for w in ws]
    groups = defaultdict(list)
    for j, w in enumerate(ws):
        for k, wi in enumerate(inverses):
            groups[binary_compose(w, wi)].append((j, k))
    ident = tuple(1 << i for i in range(len(ws[0])))
    m = len(ws)
    require(groups[ident] == [(j, j) for j in range(m)], 'Identity class has exactly the diagonal pairs')
    require(len(groups) == 1 + m*(m-1), 'All ordered nonidentity ratios must be distinct')
    return groups


def grouped_moment(r, scale, groups):
    numerator = sum(r[i][j]*r[j][k]*r[k][l]*r[l][i]
                    for pairs in groups.values() for j, k in pairs for i, l in pairs)
    return Q(numerator, scale**4)


def source_check(code, normal):
    m = len(code)
    require(m == 112 and all(len(row) == m for row in code), 'Source dimensions')
    require(multiply(code, code) == identity(m), 'Literal transposed code involution')
    p = [[Q(int(i == j)-x, 2) for j, x in enumerate(row)] for i, row in enumerate(code)]
    require(multiply(p, p) == p and len(row_basis(p)) == 8, 'Rank-eight source idempotent')
    selected = [i for i in range(m) if code[i][i] == 12]
    require(len(selected) == 8 and sum(code[i][i] for i in range(m)) == 96, 'Source diagonal and trace')
    col, cs, cr = scaled_projection(transpose(p))
    weights = [Q(1, 11) if j in selected else Q(1) for j in range(m)]
    balanced = [[x*weights[j] for j, x in enumerate(row)] for row in p]
    row, rs, rr = scaled_projection(balanced)
    require(cr == rr == 8 and cs == rs == 28, 'Independently derived projector scales')
    require(all(Q(col[i][i], cs) == Q(row[i][i], rs) == Q(1, 14) for i in range(m)),
            'Both independent metrics have uniform leverage')
    require(col != row, 'Independent positive row scaling gives a distinct projector')
    require(multiply(col, p) == [[cs*x for x in v] for v in p], 'Full column-space inclusion')
    bt = transpose(balanced)
    require(multiply(row, bt) == [[rs*x for x in v] for v in bt], 'Full balanced row-space inclusion')
    ws = []
    for record in normal['ports']:
        word = record['K_word']
        require(len(word) == 2 and word[0][0] == 'P' and word[1][0] == 'D', 'Normalizer grammar')
        g, (quad, phase) = word[0][1], word[1][1:]
        require(len(g) == 9 and not any(quad) and len(phase) == 9 and
                all(z % 2 == 0 for z in phase), 'Signed permutation normalizer')
        require(all((a & b).bit_count() % 2 == (i == j)
                    for i, a in enumerate(g) for j, b in enumerate(g)), 'Orthogonal source map')
        k1, k3 = embed(g, range(9)), embed(g, [0]+list(range(9, 17)))
        ws.append(binary_compose(k1, binary_inverse(k3)))
    require(len(ws) == m, 'Complete source normalizer inventory')
    groups = pair_partition(ws)
    moments = [grouped_moment(r, s, groups) for r, s in ((col, cs), (row, rs))]
    require(moments == [Q(27, 343)]*2, 'Two literal grouped second moments')
    closed = 2*8*Q(1, 14)**2 - m*Q(1, 14)**4
    require(moments[0] == closed, 'Independent closed moment')
    rank_lower = 16-sum(moments)
    require(rank_lower == Q(5434, 343) and 224+rank_lower == Q(82266, 343) > 239,
            'Integer return lower bound')
    result = dict(source_dimension=m, source_rank=8, selected=selected,
                  binary_pair_classes=len(groups), pair_multiplicities={str(k):v for k,v in Counter(map(len, groups.values())).items()},
                  projector_scales=[cs, rs], projector_digests=[sha256(json.dumps(r,separators=(',',':')).encode()).hexdigest() for r in (col,row)],
                  first_moment='4/7', second_moments=list(map(str,moments)),
                  rank_lower_over_h=str(rank_lower), deficit_lower_over_h=str(224+rank_lower),
                  credited_oracle_optimum=240, minimum_width_from_credited_faithfulness=72)
    return result, p, ws


def shift_power(h, residue, exponent):
    """Realification of a unitary generator X with X**h = i**residue."""
    n = 2*h
    out = [[0]*n for _ in range(n)]
    rotations = ((0,1),(1,1),(0,-1),(1,-1))
    for j in range(h):
        wraps, target = divmod(j+exponent, h)
        power = wraps*residue % 4
        for c in range(2):
            tc, sign = rotations[(power+c) % 4]
            out[2*target+tc][2*j+c] = sign
    require(multiply(transpose(out),out) == identity(n), 'Unitary twisted shift')
    return out


def gauge(a, blocks):
    """diag(blocks)^* (a tensor I) diag(blocks)."""
    m, h = len(a), len(blocks[0])
    out = [[0]*(m*h) for _ in range(m*h)]
    for i in range(m):
        for j in range(m):
            if a[i][j]:
                z = multiply(transpose(blocks[i]), blocks[j])
                for k in range(h):
                    for l in range(h):
                        if z[k][l]:
                            out[i*h+k][j*h+l] = a[i][j]*z[k][l]
    return out


def synthetic_checks():
    fixtures = []
    for residue in range(4):
        h, positions = 7, (0,1,3)
        blocks = [shift_power(h,residue,a) for a in positions]
        one = [identity(2*h)]*3
        r = [[1]*3 for _ in range(3)]
        e, f = gauge(r,one), gauge(r,blocks)
        ef = multiply(e,f)
        tau = Q(sum(ef[i][j]*ef[j][i] for i in range(6*h) for j in range(6*h)), 2*h*3**4)
        require(tau == Q(5,27), 'Literal complex phase-cocycle second moment')
        metric = [Q(1),Q(2),Q(3)]
        p = [[Q(metric[j],3*metric[i]) for j in range(3)] for i in range(3)]
        p1, p3 = gauge(p,one), gauge(p,blocks)
        c1, c3 = [subtract(identity(6*h),[[2*x for x in row] for row in v]) for v in (p1,p3)]
        require(multiply(c1,c1) == multiply(c3,c3) == identity(6*h), 'Literal gauge involutions')
        leakage = subtract(identity(6*h),multiply(c3,c1))
        alternative = multiply([[2*x for x in row] for row in subtract(p3,p1)], c1)
        require(leakage == alternative, 'Complete alternative rank factorization')
        rank_l, rank_difference = len(row_basis(leakage)),len(row_basis(subtract(p1,p3)))
        require(rank_l == rank_difference, 'Right multiplication by the involution preserves rank')
        upper_factor = [a+b for a,b in zip(p1,p3)]
        lower_factor = p1+p3
        factor_dimension = len(row_basis(p1))+len(row_basis(p3))
        require(factor_dimension == 4*h, 'Two literal rank-one regular factors')
        bound = len(row_basis(upper_factor))+len(row_basis(lower_factor))-factor_dimension
        require(rank_l >= bound, 'Literal product rank inequality')
        fixtures.append(dict(phase_residue=residue,complex_group_order=h,real_matrix_dimension=6*h,
                             second_moment=str(tau),leakage_real_rank=rank_l,sylvester_real_lower=bound))
    h=5; blocks=[shift_power(h,0,a) for a in (0,1,2)]
    e,f=gauge([[1]*3 for _ in range(3)],[identity(2*h)]*3),gauge([[1]*3 for _ in range(3)],blocks)
    ef=multiply(e,f)
    bad_tau=Q(sum(ef[i][j]*ef[j][i] for i in range(6*h) for j in range(6*h)),2*h*3**4)
    require(bad_tau != Q(5,27), 'Repeated-ratio fixture must defeat the Sidon formula')
    return fixtures,str(bad_tau)


def noncommuting_regular_check():
    """Build left/right S3 group-ring actions literally from multiplication."""
    elements = list(permutations(range(3)))
    e = elements[0]
    def product(a,b):
        return tuple(a[b[j]] for j in range(3))
    inverses = {a:next(b for b in elements if product(a,b)==e==product(b,a)) for a in elements}
    k1=[e,(1,0,2),(1,2,0)]
    k3=[e,(0,2,1),(2,0,1)]
    weights=[Q(1),Q(2),Q(3)]
    p=[[Q(weights[j],3*weights[i]) for j in range(3)] for i in range(3)]
    def code(ks):
        out=[[defaultdict(Q) for _ in range(3)] for _ in range(3)]
        for i in range(3):
            for j in range(3):
                out[i][j][e]+=int(i==j)
                out[i][j][product(inverses[ks[i]],ks[j])]-=2*p[i][j]
        return out
    c1,c3=code(k1),code(k3)
    l=[[defaultdict(Q) for _ in range(3)] for _ in range(3)]
    for i in range(3):
        for j in range(3):
            l[i][j][e]+=int(i==j)
            for k in range(3):
                for a,x in c3[i][k].items():
                    for b,y in c1[k][j].items():
                        l[i][j][product(a,b)]-=x*y
    star=[[{inverses[g]:x for g,x in l[j][i].items()} for j in range(3)] for i in range(3)]
    h=len(elements); lookup={g:i for i,g in enumerate(elements)}
    def regular(matrix,right=False):
        out=[[Q(0)]*(3*h) for _ in range(3*h)]
        for i in range(3):
            for j in range(3):
                for g in elements:
                    for a,x in matrix[i][j].items():
                        if right:
                            out[j*h+lookup[product(g,a)]][i*h+lookup[g]]+=x
                        else:
                            out[i*h+lookup[product(a,g)]][j*h+lookup[g]]+=x
        return out
    left,right,adjoint=regular(l),regular(l,True),regular(star)
    conjugation=[[0]*(3*h) for _ in range(3*h)]
    for i in range(3):
        for g in elements:
            conjugation[i*h+lookup[inverses[g]]][i*h+lookup[g]]=1
    require(multiply(conjugation,multiply(right,conjugation))==adjoint,
            'Literal right action intertwines with left adjoint, including port transpose')
    require(adjoint==transpose(left), 'Regular group involution is the Hilbert adjoint')
    require(left!=right, 'The noncommutative left/right fixture must distinguish the operators')
    ranks=[len(row_basis(x)) for x in (left,right,adjoint)]
    require(len(set(ranks))==1, 'Literal noncommutative left/right rank equality')
    return dict(group='S3',group_order=h,matrix_dimension=3*h,ranks=ranks,
                left_and_right_matrices_differ=True,adjoint_intertwiner_exact=True)


def rejected(fn, name):
    try:
        fn()
    except ValueError:
        return name
    raise ValueError('Semantic control was accepted: '+name)


def main():
    for pin in json.loads((HERE/'SOURCES.json').read_bytes())['files']:
        if pin['usage'] == 'input':
            require(sha256((ROOT/pin['path']).read_bytes()).hexdigest() == pin['sha256'], 'Exact source bytes')
    raw=json.loads(gzip.decompress((INPUT/'INVOLUTIVE-WORD.json.gz').read_bytes()))['F']
    code=[[Q(raw[j][i]) for j in range(112)] for i in range(112)]
    normal=json.loads((INPUT/'NORMALIZERS.json').read_bytes())
    result,p,ws=source_check(code,normal)
    fixtures,bad_tau=synthetic_checks()
    regular_fixture=noncommuting_regular_check()
    bad_code=[row[:] for row in code];bad_code[0][0]-=1
    controls=[rejected(lambda:source_check(bad_code,normal),'damaged literal involution'),
              rejected(lambda:pair_partition([ws[0]]*112),'collapsed fresh-block gauges'),
              rejected(lambda:binary_inverse((0,2)),'singular binary map'),
              rejected(lambda:check_projection([[1,1],[0,0]],1,1),'nonsymmetric idempotent used as an orthogonal projector'),
              rejected(lambda:require(239>=Q(result['deficit_lower_over_h']),'false capacity'),'239-return claim'),
              rejected(lambda:require(2*Q(4,7)<1,'first moment insufficient'),'first-moment closure')]
    result.update(status='PASS_INDEPENDENT_P2_PROJECTOR_AUDIT',
                  synthetic_phase_and_rank_fixtures=fixtures,repeated_ratio_moment=bad_tau,
                  noncommutative_left_right_fixture=regular_fixture,
                  rejected_semantic_controls=controls,imports_from_audited_packages=0,
                  scope='Independent source projector, all pair ratios, phase trace and rank bridge; credited history/faithfulness/oracle upper bound not replayed')
    if '--write' in sys.argv:
        (HERE/'RESULT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    else:
        require(result==json.loads((HERE/'RESULT.json').read_bytes()),'Committed independent receipt')
    print(json.dumps(result,sort_keys=True))


if __name__ == '__main__':
    main()
