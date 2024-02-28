import numpy as np


class PIDController:
    """
        Simulate a PID controller

        Attributes:
            p (float): Proportional Coefficient for Response Function
            i (float): Integral Coefficient for Response Function
            d (float): Derivative Coefficient for Response Function

        Methods:
            response(err, err_int, err_der) -> float:
                Calculates the response value of the controller and returns it
                based on the formula: u(t) = Kp*e(t) + Ki*∫e(t)dt + Kd*de(t)/dt

                err (float): Error Value from the function sp - y(t)
                err_int (float): Error summation from t=0 to t=t
                err_der (float): The current rate of change of e(t)

            standard_form(kp,tau_i,tau_d) -> PIDController:
                Provides another way of creating a PID Controller using the
                standard form of the response equation:
                u(t) = Kp*(e(t)+(1/tau_i)*∫e(t)dt+tau_d*de(t)/dt

                kp (float): Process Gain
                tau_i (float): Integration Time
                tau_d (float): Derivative Time
    """

    def __init__(self, p: float = 0, i: float = 0, d: float = 0):
        self.p = p
        self.i = i
        self.d = d

    def response(self, err, err_int, err_der):
        # u(t) = Kp*e(t) + Ki*∫e(t)dt + Kd*de(t)/dt
        return self.p * err + err_int * self.i + self.d * err_der

    @classmethod
    def standard_form(cls,kp: float = 0, tau_i: float = 0, tau_d: float = 0):
        # u(t) = Kp*(e(t)+(1/Tau_i)*∫e(t)dt+Tau_d*de(t)/dt
        ki = kp/tau_i
        kd = kp*tau_d
        return cls(kp, ki, kd)


class ControlLoop:
    """
        Simulates a Control Loop of a Closed Loop Process

        Attributes:
            dt (float): Simulation step size in seconds
            pid (PIDController): PID Controller for the Control Loop

        Methods:
            rt(t) -> float:
                Returns the process value, r(t), that the pid controller is
                designed to control at a certain time, t. Meant to be overwritten by children of
                the ControlLoop class such that the method of getting the process
                values can be updated as necessary.

                t (float): Time since start of the control loop in seconds

            sp(t) -> float:
                Returns the setpoint of the process at a specified time, t. Meant
                to be overwritten by children to allow for modifiable setpoints
                such as step change, ramp, etc.

                t (float): Time since start of the control loop in seconds

            simulate_loop(key,tend) -> tuple (tplot,rt):
                Runs a simulation based on the Control Loop using process values obtained
                from the rt method against setpoints obtained from the sp method and corrections
                made by using the PID Controller, pid. Returns a tuple containing all the time
                values in tplot as well as the process values in rt

                key (string): key of the variable that is modifying the process
                tend (float): endpoint of the simulation in seconds

    """


    dt = 0.1

    def __init__(self, pid: PIDController, **kwargs):
        self.pid = pid
        for key, val in kwargs.items():
            self.__dict__[key] = val

    def rt(self, t):
        # meant to be overwritten by children
        return 0

    def sp(self, t):
        # meant to be overwritten by children
        return 0

    def simulate_loop(self, key='q', tend=10):
        tplot = np.arange(0, tend + self.dt, self.dt)
        et = np.zeros(tplot.shape)
        et_int = 0
        et_der = 0

        qi = np.zeros(tplot.shape)
        rt = np.zeros(tplot.shape)

        for i in range(tplot.shape[0]):
            try:
                qi[i] = self.__dict__[key]
            except KeyError:
                qi[i] = eval(f'self.{key}')
            rt[i] = self.rt(tplot[i])
            et[i] = rt[i] - self.sp(tplot[i])
            # print(rt[i],et[i],sep=' -- ')
            et_int += et[i] * self.dt
            et_der = 0 if i == 0 else (et[i] - et[i - 1]) / 2
            self.__dict__[key] = qi[0] - self.pid.response(et[i], et_int, et_der)

        return tplot, rt
