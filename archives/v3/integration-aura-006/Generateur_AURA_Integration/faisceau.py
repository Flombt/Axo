"""Courbes de service entre connecteurs, avec étude numérique de rayon et de collision."""

import math

import adsk.fusion as fusion


def add(a, b):
    return tuple(v + w for v, w in zip(a, b))


def sub(a, b):
    return tuple(v - w for v, w in zip(a, b))


def scale(a, x):
    return tuple(v * x for v in a)


def norm(a):
    return math.hypot(*a)


def unit(a):
    return scale(a, 1 / norm(a))


def cross(a, b):
    x, y, z = a
    u, v, w = b
    return y * w - z * v, z * u - x * w, x * v - y * u


def evaluate(p, q, r, s):
    path, radii = [], []
    a, b, c = sub(q, p), sub(r, q), sub(s, r)
    dd0, dd1 = sub(b, a), sub(c, b)
    for i in range(21):
        t = i / 20
        other = 1 - t
        point = add(add(scale(p, other**3), scale(q, 3 * other**2 * t)),
                    add(scale(r, 3 * other * t**2), scale(s, t**3)))
        velocity = scale(add(add(scale(a, other**2), scale(b, 2 * t * other)), scale(c, t**2)), 3)
        accel = scale(add(scale(dd0, other), scale(dd1, t)), 6)
        nums, denom = norm(velocity), norm(cross(velocity, accel))
        radii.append(nums**3 / denom if denom > .0001 else (1e6 if nums > .0001 else 0))
        path.append(point)
    length = sum(math.dist(x, y) for x, y in zip(path, path[1:]))
    return min(radii), length, path


def terminal(bench, component, p, outward, setback):
    frame = bench.parts[component].transform2
    direction = unit(outward)
    xyz = bench.base.point(add(p, scale(direction, setback)))
    xyz.transformBy(frame)
    n = bench.base.vector(direction)
    n.transformBy(frame)
    return tuple(v * 10 for v in xyz.asArray()), n.asArray()


def endpoints(bench, source, target):
    parent, _, points, radius = source
    child, _, next_points, next_radius = target
    p, a = terminal(bench, parent, points[-1], sub(points[-1], points[-2]), 7.1)
    s, b = terminal(bench, child, next_points[0], sub(next_points[0], next_points[1]), 7.1)
    return p, a, s, b, min(radius, next_radius)


def options(begin, outgoing, end, incoming):
    gap = math.dist(begin, end)
    handles = [gap * t for t in (.35, .60, .85, 1.10, 1.35)]
    designs = []
    for a in handles:
        for b in handles:
            v = evaluate(begin, add(begin, scale(outgoing, a)), add(end, scale(incoming, b)), end)
            designs.append(v)
    # Keep some spare length while favoring an even bend.
    usable = [v for v in designs if 1.05 * gap <= v[1] <= 1.55 * gap]
    return sorted(usable or designs, key=lambda v: -v[0])[:3]


def get_obstacles(bench, keys):
    items = []
    for key in sorted(keys):
        occurrence = bench.parts[key]
        body = next(x for x in occurrence.bRepBodies if x.name == key)
        box = body.boundingBox
        bounds = tuple(tuple(v * 10 for v in p.asArray()) for p in (box.minPoint, box.maxPoint))
        items.append((key, body, occurrence.transform2, bounds))
    return items


def overlaps(bench, curve, radius, obstacles):
    g = bench.g
    lo = [min(xs) - radius for xs in zip(*curve)]
    hi = [max(xs) + radius for xs in zip(*curve)]
    candidates = [(tag, body, frame) for tag, body, frame, (a, b) in obstacles
                  if all(x <= q and p <= y for x, p, y, q in zip(lo, a, hi, b))]
    if not candidates:
        return []
    # The tube is tessellated longitudinally in the CAD volume. Radius comes from the smooth curve.
    from_path = curve[::2]
    path = []
    for a, b in zip(from_path, from_path[1:]):
        direction = unit(sub(b, a))
        path.append(g.cyl(sub(a, scale(direction, .45)), add(b, scale(direction, .45)), radius))
    shape = g.union(path[0], *path[1:])
    hits = []
    for key, proxy, frame in candidates:
        actual = g.manager.copy(proxy.nativeObject or proxy)
        g.manager.transform(actual, frame)
        ok = g.manager.booleanOperation(actual, shape, fusion.BooleanTypes.IntersectionBooleanType)
        if ok and actual.volume * 1000 > .005:
            hits.append({"piece": key, "mm3": round(actual.volume * 1000, 3)})
    return hits


def study(bench, energy, keys):
    hand_points = ((12, -29, -13), (40, -29, -13))
    ports = energy.ROUTES + (("Paume", "Wrist", hand_points, 3.2),)
    obs = get_obstacles(bench, keys)
    recorded, homes = [], []
    for source, target in zip(ports, ports[1:]):
        name = f"{source[0]}_{target[0]}"
        start, a, finish, b, r = endpoints(bench, source, target)
        if math.dist(start, finish) < 2:
            recorded.append({"transition": name, "degagement_mm": round(math.dist(start, finish), 2),
                             "statut": "ancrages à éloigner"})
            continue
        candidates = options(start, a, finish, b)
        best = None
        for radius, length, coordinates in candidates:
            try:
                hits = overlaps(bench, coordinates, r, obs)
            except RuntimeError:
                # Fusion can fail to join very tight consecutive solids of the sampled curve.
                continue
            proposal = (hits, radius, length, coordinates)
            if best is None or sum(h["mm3"] for h in hits) < sum(h["mm3"] for h in best[0]):
                best = proposal
            if not hits:
                break
        if best is None:
            recorded.append({"transition": name, "statut": "enveloppe Fusion non calculée"})
            continue
        hits, radius, length, coordinates = best
        reserve = 10 * r
        recorded.append({"transition": name, "longueur_mm": round(length, 2),
                         "rayon_min_mm": round(radius, 2), "cible_hypothese_mm": round(reserve, 2),
                         "rayon_cible_atteint": radius >= reserve, "interferences": hits})
        homes.append((name, coordinates[::2], r))
    return recorded, homes
