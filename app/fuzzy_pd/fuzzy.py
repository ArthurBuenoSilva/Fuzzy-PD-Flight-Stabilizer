import itertools
from typing import List

import numpy as np
import skfuzzy as fuzzy
from skfuzzy.control import (
    Antecedent,
    Consequent,
    ControlSystem,
    ControlSystemSimulation,
    Rule,
)


class Fuzzy:
    def __init__(self, fa: float, p_mode: float):
        # Fuzzification
        self.error: Antecedent | None = None
        self.delta_error: Antecedent | None = None
        self.power: Consequent | None = None

        # Base rules
        self.rules: List = list()

        # Defuzzification
        self.fa: float = fa
        self.p_mode: float = p_mode
        self.set_point: float = 0
        self.height_history: List = list()
        self.current_height: float = 0

    def fuzzification(self):
        universe = np.arange(-100, 100.01, 0.01)
        self.error = Antecedent(universe=universe, label="error")

        universe = np.arange(-6, 6.01, 0.01)
        self.delta_error = Antecedent(universe=universe, label="delta_error")

        universe = np.arange(0, 1.01, 0.01)
        self.power = Consequent(universe=universe, label="power")

        # Error membership functions
        self.error["MN"] = fuzzy.trapmf(self.error.universe, [0, 0, 0.5, 3.0])
        self.error["N"] = fuzzy.trimf(self.error.universe, [0.5, 3.0, 15.0])
        self.error["ZE"] = fuzzy.trimf(self.error.universe, [3.0, 15.0, 100.0])
        self.error["P"] = fuzzy.trimf(self.error.universe, [15.0, 100.0, 300.0])
        self.error["MP"] = fuzzy.trapmf(self.error.universe, [100.0, 300.0, 1000.0, 1000.0])

        # Delta error membership functions
        self.delta_error["MN"] = fuzzy.trapmf(self.delta_error.universe, [-1000.0, -100.0, -5, -0.5])
        self.delta_error["N"] = fuzzy.trimf(self.delta_error.universe, [-5, -0.5, 0])
        self.delta_error["ZE"] = fuzzy.trimf(self.delta_error.universe, [-0.5, 0, 0.5])
        self.delta_error["P"] = fuzzy.trimf(self.delta_error.universe, [0, 0.5, 5.0])
        self.delta_error["MP"] = fuzzy.trapmf(self.delta_error.universe, [0.5, 5, 1000.0, 1000.0])

        # Power membership functions
        self.power["MP"] = fuzzy.trimf(self.power.universe, [0, 0, 0.2])
        self.power["P"] = fuzzy.trimf(self.power.universe, [0, 0.2, 0.5])
        self.power["M"] = fuzzy.trimf(self.power.universe, [0.2, 0.5, 0.8])
        self.power["A"] = fuzzy.trimf(self.power.universe, [0.5, 0.8, 1])
        self.power["MA"] = fuzzy.trimf(self.power.universe, [0.8, 1, 1])

    def rule_base(self):
        power_result = [
            'MP', 'P', 'M', 'A', 'A',
            'P', 'M', 'A', 'A', 'MA',
            'M', 'A', 'A', 'MA', 'MA',
            'P', 'M', 'A', 'A', 'MA',
            'MP', 'P', 'M', 'A', 'A'
        ]

        # Apply the rules above
        self.rules = [
            Rule(self.error[error] & self.delta_error[delta_error], self.power[power])
            for (delta_error, error), power in zip(
                itertools.product(self.delta_error.terms.keys(), self.error.terms.keys()), power_result
            )
        ]

    def defuzzification(self):
        control_system = ControlSystemSimulation(ControlSystem(self.rules))
        previous_error = self.set_point - self.current_height

        time = np.arange(0, 400, 1)
        self.fa = 0.98621
        self.p_mode = -3.0 if self.current_height > self.set_point else 5.0

        for _ in range(1, np.max(time) + 1):
            # Calculate and input the current error
            current_error = self.set_point - self.current_height
            control_system.input[self.error.label] = abs(current_error)

            # Calculate and input the current delta error
            current_delta_error = previous_error - current_error
            control_system.input[self.delta_error.label] = current_delta_error

            # Calculate equivalent output
            control_system.compute()

            # Stop adjustment
            if (abs(current_error) <= 0.5):
                self.fa = self.stop_adjustment(self.current_height, control_system.output[self.power.label], self.p_mode, 1.01398)

            # Update current height value based on the Transfer Function
            new_height = self.fa * self.current_height * 1.01398 + 0.5 * (
                self.p_mode * control_system.output[self.power.label]
                + self.p_mode * control_system.output[self.power.label]
            )

            if new_height < self.set_point:
                self.current_height = new_height
            else:
                self.current_height = self.current_height - (new_height - self.current_height)

            self.height_history = np.append(self.height_history, self.current_height)


            # Update error
            previous_error = current_error

    def calculate_FA(self, current_error: float) -> float:
        return 0.965605 + 0.020605 * ((current_error) / (100))

    def stop_adjustment(self, current_height: float, power: float, umax: float, h_coefs: float) -> float:
        return (current_height - (power * umax)) / (h_coefs * current_height)
