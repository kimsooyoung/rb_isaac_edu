"""
PID Controller
==============
"""

# Global imports
import numpy as np

class PIDController:
    """
    Controller acts on a predefined trajectory and adds PID control gains.
    """
    def __init__(self, Kp, Ki, Kd, data_dict=None, use_feed_forward=True):
        """
        Controller acts on a predefined trajectory and adds PID control gains.

        Parameters
        ----------
        data_dict : dictionary
            a dictionary containing the trajectory to follow
            should have the entries:
            data_dict["des_time"] : desired timesteps
            data_dict["des_pos"] : desired positions
            data_dict["des_vel"] : desired velocities
            data_dict["des_tau"] : desired torques
        Kp : float
            proportional term,
            gain proportial to the position error
        Ki : float
            integral term,
            gain proportional to the integral
            of the position error
        Kd : float
            derivative term,
            gain proportional to the derivative of the position error
        use_feed_forward : bool
            whether to use the torque that is provided in the csv file
        """

        if data_dict is not None:
            self.traj_len = len(data_dict["des_time"])
            self.traj_time = data_dict["des_time"]
            self.traj_pos = data_dict["des_pos"]
            self.traj_vel = data_dict["des_vel"]
            self.dt = self.traj_time[1] - self.traj_time[0]
            if use_feed_forward:
                self.traj_tau = data_dict["des_tau"]
        else:
            self.traj_len = 0
            self.traj_time = None
            self.traj_pos = None
            self.traj_vel = None
            self.traj_tau = None
            self.dt = 0.005

        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.use_feed_forward = use_feed_forward

        self.counter = 0
        self.errors = []
        self.last_pos = 0.0
        self.last_vel = 0.0

    def init(self, x0):
        self.counter = 0
        self.errors = []
        self.last_pos = 0.0
        self.last_vel = 0.0

    def reset(self):
        self.counter = 0
        self.errors = []
        self.last_pos = 0.0
        self.last_vel = 0.0

    def set_goal(self, x):
        self.goal = x

    def get_control_output(
            self, counter,
            meas_pos=None, meas_vel=None, 
            meas_tau=None, meas_time=None
        ):
        """
        The function to read and send the entries of the loaded trajectory
        as control input to the simulator/real pendulum.

        Parameters
        ----------
        meas_pos : float, deault=None
            the position of the pendulum [rad]
        meas_vel : float, deault=None
            the velocity of the pendulum [rad/s]
        meas_tau : float, deault=None
            the meastured torque of the pendulum [Nm]
        meas_time : float, deault=None
            the collapsed time [s]

        Returns
        -------
        des_pos : float
            the desired position of the pendulum [rad]
        des_vel : float
            the desired velocity of the pendulum [rad/s]
        des_tau : float
            the torque supposed to be applied by the actuator [Nm]
        """

        des_pos = self.last_pos
        des_vel = self.last_vel
        des_tau = 0.0

        # if self.counter < len(self.traj_time):
        if self.counter < self.traj_len:
            self.counter = counter
        else:
            self.counter = self.traj_len - 1
        print(f"self.counter: {self.counter} / self.traj_len: {self.traj_len}")

        if self.traj_pos is not None:
            des_pos = self.traj_pos[self.counter]
            des_vel = self.traj_vel[self.counter]
            if self.use_feed_forward:
                des_tau = self.traj_tau[self.counter]
        else:
            des_pos = self.goal[0]
            des_vel = self.goal[1]
            des_tau = 0.0

        self.last_pos = des_pos
        self.last_vel = des_vel

        e = des_pos - meas_pos

        if self.traj_pos is not None:
            e = (e + np.pi) % (2*np.pi) - np.pi
        else:
            e = e

        print(f"e: {e} / des_pos: {des_pos} / des_vel: {des_vel} / des_tau: {des_tau}")
        self.errors.append(e)

        P = self.Kp*e
        I = self.Ki*np.sum(self.errors)*self.dt
        if len(self.errors) > 2:
            D = self.Kd*(self.errors[-1]-self.errors[-2])/self.dt
        else:
            D = 0.0

        des_tau = des_tau + P + I + D

        self.counter += 1

        return des_pos, des_vel, des_tau


# def controller(obs, params):
    
#     theta, omega = obs[0]
#     kp, kd, theta_des, min_torque, max_torque = params.kp, params.kd, params.theta_des, params.min_torque, params.max_torque

#     # Ensure tensors are on CPU before converting to numpy
#     torque_value = -kp * (theta.cpu().numpy() - theta_des) - kd * omega.cpu().numpy()

#     # Clip torque value to specified limits
#     torque_value = np.clip(torque_value, min_torque, max_torque)

#     # Wrap in 2D NumPy array to get shape [1, 1]
#     torque = torch.from_numpy(np.array([[torque_value]], dtype=np.float32)).to(theta.device)

#     return torque