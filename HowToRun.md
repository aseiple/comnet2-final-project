1. `sudo python topo.py`
2. From Mininet CLI launch xterms
    1. `xterm s`
    2. `xterm d1`
    3. `xterm d2`
    4. `xterm d3`
    5. `xterm r1`
    6. `xterm r2`
    7. `xterm r3`
    8. `xterm r4`
    9. `xterm r5`
3. In each xterm run related python file specifing the which host it is
    1. s: `python node.py s`
    2. d1: `python node.py d1`
    3. d2: `python node.py d2`
    4. d3: `python node.py d3`
    5. r1: `python router.py r1`
    6. r2: `python router.py r2`
    7. r3: `python router.py r3`
    8. r4: `python router.py r4`
    9. r5: `python router.py r5`
4. Run requested operation from node xterms,
    - Multicast: `mul <n> <k> <dst 1> <dst 2> <dst 3> <data>`
    - Unicast: `uni <dst> <data>`
