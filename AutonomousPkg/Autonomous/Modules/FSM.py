import time
from threading import *

class FSM(Thread):

    def __init__(self, states: list, looping: bool = True):

        super(FSM, self).__init__()

        self._states = states
        self._state_counter = 0

        self.__running = False
        self.__looping = looping
        self.__complete_states = []

    @property
    def running(self):
        return self.__running

    @property
    def completion_status(self):
        return self.__complete_states

    @property
    def current_state_id(self):
        return self._state_counter

    def stop_thread(self):
        self.__running = False

    def start(self) -> None:
        self.__running = True
        self.__complete_states.clear()
        self._state_counter = 0

    def __do_loop(self):
        while self.__running:
            self._state_counter = 0
            self.__complete_states.clear()

            for state in self._states:
                state.do_state()
                self.__complete_states.append(state.done)
                self._state_counter += 1

    def __do_once(self):
        self._state_counter = 0
        self.__complete_states.clear()

        for state in self._states:
            state.do_state()
            self.__complete_states.append(state.done)
            self._state_counter += 1

        self.__running = False

    def run(self) -> None:
        if self.__looping:
            self.__do_loop()
        else:
            self.__do_once()


class State:

    def __init__(self, state_func, timeout: int = 0):
        self.__running = False
        self.__complete = False
        self._start_time = 0.0
        self._dur = 0.0
        self.__timeout = timeout

        self._state_func = state_func

    def do_state(self):
        self.__running = False
        self.__complete = False

        self._start_timer()

        self._state_func()

        self._stop_timer()

    def kill_state(self):
        self.__running = False

    def _start_timer(self):
        self._start_time = time.perf_counter()

    def _stop_timer(self) -> float:
        self._dur = time.perf_counter() - self._start_time
        return self._dur

    @property
    def timeout(self):
        return self.__timeout

    @property
    def done(self):
        return self.__complete

    @property
    def running(self):
        return self.__running

    @property
    def duration(self):
        return self._dur






