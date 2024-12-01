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

from app.extensions import socketio


class Fuzzy:
    def __init__(self, current_height: float):
        # Fuzzification
        self.error: Antecedent | None = None
        self.delta_error: Antecedent | None = None
        self.power: Consequent | None = None

        # Base rules
        self.rules: List = list()

        # Control System
        self.control: ControlSystemSimulation | None = None

        # Defuzzification
        self.fa: float = 0.98621
        self.p_mode: float = 3
        self.set_point: float = 0
        self.height_history: List = list()
        self.current_height: float = current_height
        self.tolerance: float = 0.5
        self.max_iterations = 10000
        self.time: float = 0
        self.time_history: List = list()

        self.fuzzification()
        self.rule_base()
        self.control_system()

    def fuzzification(self):
        universe = np.arange(0, 1000.01, 0.01)
        self.error = Antecedent(universe=universe, label="error")

        universe = np.arange(-1000, 1000.01, 0.01)
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

    def control_system(self):
        self.control = ControlSystemSimulation(ControlSystem(self.rules))

    def reset_system(self):
        self.height_history = list()
        self.time_history = list()
        self.time = 0

    def defuzzification(self, set_point: float):
        self.set_point = set_point
        previous_error = self.set_point - self.current_height

        self.reset_system()

        while self.time < self.max_iterations:
            # Calculate and input the current error
            current_error = self.set_point - self.current_height
            self.control.input[self.error.label] = abs(current_error)

            # Calculate and input the current delta error
            current_delta_error = previous_error - current_error
            self.control.input[self.delta_error.label] = current_delta_error

            # Calculate equivalent output
            self.control.compute()

            # Fa adjustment
            if abs(current_error) <= self.tolerance:
                self.fa = self.fa_adjustment(
                    self.current_height,
                    self.control.output[self.power.label],
                    self.p_mode,
                    1.01398
                )

            # Update current height value based on the Transfer Function
            new_height = self.fa * self.current_height * 1.01398 + 0.5 * (
                self.p_mode * self.control.output[self.power.label]
                + self.p_mode * self.control.output[self.power.label]
            )

            if new_height < self.set_point:
                self.current_height = new_height
            else:
                self.current_height = self.current_height - (new_height - self.current_height)

            # Append current height and time to histories
            self.height_history = np.append(self.height_history, self.current_height)
            self.time_history = np.append(self.time_history, self.time)

            if self.time % 10 == 0:
                socketio.emit('result', {
                    "labels": self.time_history.astype(float).tolist(),
                    "memberships": [{
                        "name": "Altura/Tempo",
                        "values": self.height_history.astype(float).round(3).tolist(),
                        "color": "green",
                    }],
                    "set_point": float(self.set_point),
                    "current_height": float(round(self.current_height, 3)),
                    "fa": float(self.fa),
                    "p_mode": float(self.p_mode),
                    "error": abs(float(round(previous_error, 3))),
                    "min": self.height_history.min() * 0.8 if self.height_history.min() >= 0 else self.height_history.min() * 1.2,
                    "max": self.height_history.max() * 1.2 if self.height_history.max() >= 0 else self.height_history.max() * 0.8,
                })

            # Check if height has stabilized
            if abs(current_error) <= self.tolerance and len(self.height_history) > 10:
                if np.std(self.height_history[-50:]) < 0.01:
                    break

            # Update error and increment time
            previous_error = current_error
            self.time += 1

        return {
            "labels": self.time_history.astype(float).tolist(),
            "memberships": [{
                "name": "Altura/Tempo",
                "values": self.height_history.astype(float).round(3).tolist(),
                "color": "green",
            }],
            "set_point": float(self.set_point),
            "current_height": float(round(self.current_height, 3)),
            "fa": float(self.fa),
            "p_mode": float(self.p_mode),
            "error": abs(float(round(previous_error, 3))),
            "min": self.height_history.min() * 0.8 if self.height_history.min() >= 0 else self.height_history.min() * 1.2,
            "max": self.height_history.max() * 1.2 if self.height_history.max() >= 0 else self.height_history.max() * 0.8,
        }

    @staticmethod
    def calculate_fa(current_error: float) -> float:
        return 0.965605 + 0.020605 * (current_error / 100)

    @staticmethod
    def fa_adjustment(current_height: float, power: float, umax: float, h_coefs: float) -> float:
        return (current_height - (power * umax)) / (h_coefs * current_height)
