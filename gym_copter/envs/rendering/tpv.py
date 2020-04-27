from matplotlib import pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D

class TPV:

    def __init__(self, env):

        # Environment will be used to get position
        self.env = env

        # Helps us handle window close
        self.is_open = True

        # Set up figure & 3D axis for animation
        self.fig = plt.figure()
        ax = self.fig.add_axes([0, 0, 1, 1], projection='3d')

        # Set up axis labels
        ax.set_xlabel('X (m)')
        ax.set_ylabel('Y (m)')
        ax.set_zlabel('Z (m)')

        # Set title to name of environment
        ax.set_title(env.unwrapped.spec.id)

        # Set axis limits
        ax.set_xlim((-100, 100))
        ax.set_ylim((-100, 100))
        ax.set_zlim((0, 100))

        # Set up line and point
        self.line = ax.plot([], [], [], '-', c='b')[0]
        self.line.set_data([], [])
        self.line.set_3d_properties([])
        self.pt   = ax.plot([], [], [], 'o', c='b')[0]
        self.pt.set_data([], [])
        self.pt.set_3d_properties([])

        # Initialize arrays that we will accumulate to plot trajectory
        self.xs = []
        self.ys = []
        self.zs = []

    def start(self):

        # Instantiate the animator
        anim = animation.FuncAnimation(self.fig, self._animate, interval=int(1000*self.env.dt), blit=False)
        self.fig.canvas.mpl_connect('close_event', self._handle_close)

        # Show the display window
        plt.show()

    def _handle_close(self, event):

        self.is_open = False
        
    def _animate(self, i):

        # Get vehicle position
        x,y,z = self.env.state[0:6:2]

        # Negate Z to accomodate NED
        z = -z

        # Append position to arrays for plotting trajectory
        self.xs.append(x)
        self.ys.append(y)
        self.zs.append(z)

        # Plot trajectory
        self.line.set_data(self.xs, self.ys)
        self.line.set_3d_properties(self.zs)

        # Show vehicle as a dot
        self.pt.set_data(x, y)
        self.pt.set_3d_properties(z)

        # Draw everything
        self.fig.canvas.draw()
