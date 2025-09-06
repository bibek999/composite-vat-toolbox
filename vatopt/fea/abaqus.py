def write_abaqus_coupon(path, width, height, ply_angles):
    tply = 0.0005
    with open(path, 'w') as f:
        f.write('*Heading\nComposite coupon auto-generated\n')
        f.write('*Part, name=COUPON\n')
        f.write('*Node\n1, 0., 0., 0.\n2, {}, 0., 0.\n3, {}, {}, 0.\n4, 0., {}, 0.\n'.format(width, width, height, height))
        f.write('*Element, type=S4\n1, 1,2,3,4\n')
        f.write('*Elset, elset=ALLE\n1\n')
        f.write('*End Part\n')
        f.write('*Assembly, name=ASM\n*Instance, name=I1, part=COUPON\n*End Instance\n*End Assembly\n')
        f.write('*Material, name=UD\n*Elastic, type=ENGINEERING CONSTANTS\n130000., 10000., 5000., 0.3,0.3,0.3, 5000.,5000.,5000.\n')
        f.write('*Shell Section, composite, elset=ASM.I1.ALLE\n')
        for ang in ply_angles:
            f.write(f'{tply}, UD, {ang}, 1.\n')
