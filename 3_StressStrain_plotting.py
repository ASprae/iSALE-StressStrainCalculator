import pySALEPlot as psp
import numpy as np
import matplotlib.pyplot as plt

sim = 'modelname'
psp.mkdir_p(sim)
folder = 'plotting'
psp.mkdir_p(sim + '/' + folder)

m = psp.opendatfile('../{}/output/jdata.dat'.format(sim))
m.setScale('cm')

tracerlist = np.load('TRACERS.npy')

fig=plt.figure(figsize = (10,12))
ax=fig.add_subplot(111,aspect='equal')

for i in np.arange(0,m.nsteps,1):

    ax.set_xlabel('r [cm]')
    ax.set_ylabel('z [cm]')

    ax.set_xlim([-np.amax(m.xhires), np.amax(m.xhires)])
    ax.set_ylim(m.yhires)

    s=m.readStep('Pre',i)

    p=ax.pcolormesh(m.x, m.y, s.Pre*1.e-9, cmap='viridis', vmin=0, vmax=5)
    p=ax.pcolormesh(-m.x, m.y, s.Pre*1.e-9, cmap='viridis', vmin=0, vmax=5)

    [ax.contour(m.xc, m.yc, s.cmc[mat], 1, colors='0.5', linewidths=1) for mat in [0,1,2,3]]
    [ax.contour(-m.xc, m.yc, s.cmc[mat], 1, colors='0.5', linewidths=1) for mat in [0,1,2,3]]

    if i == 0:
        cb=fig.colorbar(p, orientation = 'horizontal')
        cb.set_label('Pressure [GPa]')

    ax.set_title(r'{: 3.2f} $\mu s$'.format(s.time*1.e6))

    for tr in tracerlist:
        data = np.genfromtxt('{}/StressStrain_{}/output.txt'.format(sim, tr))

        time = data[:,1] * 1.E-6


        x_loc = s.xmark[tr]
        y_loc = s.ymark[tr]

        S1 = data[:,35] * 1.E-6
        S1_x = data[:,36]
        S1_y = data[:,37]
        S1_z = data[:,38]
        S2 = data[:,39] * 1.E-6
        S2_x = data[:,40]
        S2_y = data[:,41]
        S2_z = data[:,42]
        S3 = data[:,43] * 1.E-6
        S3_x = data[:,44]
        S3_y = data[:,45]
        S3_z = data[:,46]
        P = data[:,47] * 1.E-6
        T = data[:,48]

        Lowcutoff = 1
        LowLim = 500

        if P[i] <= Lowcutoff:
            width = 0
            scale = np.inf
        elif P[i] < LowLim:
            # 0 -> 1/30
            scale = (1/((P[i] - Lowcutoff) / (LowLim - Lowcutoff) * (1/30)))
        else:
            width = 0.004
            scale = 30

        ax.scatter(x_loc, y_loc, c = 'w', s = 0.5)
        ax.quiver(-x_loc, y_loc, -S1_x[i], S1_y[i], color = 'w', scale = scale, width = 0.004, headlength=0, headaxislength=0, pivot = 'middle')
        ax.quiver(x_loc, y_loc, S1_x[i], S1_y[i], color = 'w', scale = scale, width = 0.004, headlength=0, headaxislength=0, pivot = 'middle')

    fig.savefig('{}/{}/Pre_{:03d}.png'.format(sim,folder,i))

    ax.cla()
