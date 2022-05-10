hosts = {
    's': ['10.0.1.4', 9000],
    'd1': ['10.0.2.3', 9001],
    'd2': ['10.0.4.4', 9002],
    'd3': ['10.0.5.4', 9003],
    'r1': ['10.0.1.1', 9004],
    'r2': ['10.0.2.1', 9005],
    'r3': ['10.0.3.1', 9006],
    'r4': ['10.0.4.1', 9007],
    'r5': ['10.0.5.1', 9008]
}

routes = {
    'r1': {
        'r2': {'path': 'r2', 'cost': 1},
        'r3': {'path': 'r3', 'cost': 1},
        'r4': {'path': 'r3', 'cost': 2},
        'r5': {'path': 'r3', 'cost': 2},
        's': {'path': 's', 'cost': 1},
        'd1': {'path': 'r2', 'cost': 2},
        'd2': {'path': 'r3', 'cost': 3},
        'd3': {'path': 'r3', 'cost': 3}
    },
    'r2': {
        'r1': {'path': 'r1', 'cost': 1},
        'r3': {'path': 'r1', 'cost': 2},
        'r4': {'path': 'r1', 'cost': 3},
        'r5': {'path': 'r1', 'cost': 3},
        's': {'path': 'r1', 'cost': 2},
        'd1': {'path': 'd1', 'cost': 1},
        'd2': {'path': 'r1', 'cost': 4},
        'd3': {'path': 'r1', 'cost': 4}
    },
    'r3': {
        'r1': {'path': 'r1', 'cost': 1},
        'r2': {'path': 'r1', 'cost': 2},
        'r4': {'path': 'r4', 'cost': 1},
        'r5': {'path': 'r5', 'cost': 1},
        's': {'path': 'r1', 'cost': 2},
        'd1': {'path': 'r1', 'cost': 3},
        'd2': {'path': 'r4', 'cost': 1},
        'd3': {'path': 'r5', 'cost': 2}
    },
    'r4': {
        'r1': {'path': 'r3', 'cost': 2},
        'r2': {'path': 'r3', 'cost': 3},
        'r3': {'path': 'r3', 'cost': 1},
        'r5': {'path': 'r5', 'cost': 1},
        's': {'path': 'r3', 'cost': 3},
        'd1': {'path': 'r3', 'cost': 4},
        'd2': {'path': 'd2', 'cost': 1},
        'd3': {'path': 'r5', 'cost': 2}
    },
    'r5': {
        'r1': {'path': 'r3', 'cost': 2},
        'r2': {'path': 'r3', 'cost': 3},
        'r3': {'path': 'r3', 'cost': 1},
        'r4': {'path': 'r4', 'cost': 1},
        's': {'path': 'r3', 'cost': 3},
        'd1': {'path': 'r3', 'cost': 4},
        'd2': {'path': 'r4', 'cost': 2},
        'd3': {'path': 'd3', 'cost': 1}
    },
    's': {
        'r1': {'path': 'r1', 'cost': 1},
        'r2': {'path': 'r1', 'cost': 2},
        'r3': {'path': 'r1', 'cost': 2},
        'r4': {'path': 'r1', 'cost': 3},
        'r5': {'path': 'r1', 'cost': 3},
        'd1': {'path': 'r1', 'cost': 3},
        'd2': {'path': 'r1', 'cost': 4},
        'd3': {'path': 'r1', 'cost': 4}
    },
    'd1': {
        'r1': {'path': 'r2', 'cost': 2},
        'r2': {'path': 'r2', 'cost': 1},
        'r3': {'path': 'r2', 'cost': 3},
        'r4': {'path': 'r2', 'cost': 4},
        'r5': {'path': 'r2', 'cost': 4},
        's': {'path': 'r2', 'cost': 3},
        'd2': {'path': 'r2', 'cost': 5},
        'd3': {'path': 'r2', 'cost': 5}
    },
    'd2': {
        'r1': {'path': 'r4', 'cost': 3},
        'r2': {'path': 'r4', 'cost': 4},
        'r3': {'path': 'r4', 'cost': 2},
        'r4': {'path': 'r4', 'cost': 1},
        'r5': {'path': 'r4', 'cost': 2},
        's': {'path': 'r4', 'cost': 4},
        'd1': {'path': 'r4', 'cost': 5},
        'd3': {'path': 'r4', 'cost': 3}
    },
    'd3': {
        'r1': {'path': 'r5', 'cost': 3},
        'r2': {'path': 'r5', 'cost': 4},
        'r3': {'path': 'r5', 'cost': 2},
        'r4': {'path': 'r5', 'cost': 2},
        'r5': {'path': 'r5', 'cost': 1},
        's': {'path': 'r5', 'cost': 4},
        'd1': {'path': 'r5', 'cost': 5},
        'd2': {'path': 'r5', 'cost': 3}
    }
}

src_resolve = {
    1: 'r1',
    2: 'r2',
    3: 'r3',
    4: 'r4',
    5: 'r5',
    6: 's',
    7: 'd1',
    8: 'd2',
    9: 'd3',
    'r1': 1,
    'r2': 2,
    'r3': 3,
    'r4': 4,
    'r5': 5,
    's': 6,
    'd1': 7,
    'd2': 8,
    'd3': 9,
}

nbrs = {
    'r1': ['r2', 'r3', 's'],
    'r2': ['r1', 'd1'],
    'r3': ['r1', 'r4', 'r5'],
    'r4': ['r3', 'r5', 'd2'],
    'r5': ['r3', 'r4', 'd3'],
    's': ['r1'],
    'd1': ['r2'],
    'd2': ['r4'],
    'd3': ['r5']
}