"""
BESC30-R3 (Blue Robotics Basic ESC) Driver.
"""

import threading
import time

# Don't forget to set these all to False when you're done!

# Skip instructions that involve the RPI
DEBUG_NO_PI: bool = False

# Enable `print_debug`
DEBUG_LOG_ENABLED: bool = False


def print_debug(*msg: object):
    if DEBUG_LOG_ENABLED == False:
        return

    print(msg)


try:
    import pigpio  # type: ignore
except ModuleNotFoundError:
    if DEBUG_NO_PI == False:
        print("[error] (client): pigpio not found, and DEBUG_NO_PI set to False. Are you on the right system?")
        exit()


# Forward declaration
class DriverInterface:
    pass


class SequenceNode:
    """
    Sequence node class, eventually submitted as requests.
    """

    def __init__(self, duration_s: float, value: int):
        """
        Paremeters:

                `duration`
                        The length of the sequence node

                `value`
                        The serial value of the node

        """
        self.duration: float = duration_s
        self.value: int = value


class ThrusterSequence:
    """
    Synchronizes and executes lists of `SequenceNode`s
    """

    def __init__(self, nodes: list[SequenceNode]):
        """
        Paremeters:
                `nodes`
                        List of sequence nodes (tickets) to be executed by this sequence
        """

        self.nodes: list[SequenceNode] = nodes

    def exec_seq(self, driver: DriverInterface, pin: int):
        """
        Eexcutes the sequence.

        NOTE: THIS WILL BLOCK YOUR THREAD.
        """

        for node in self.nodes:
            print_debug("[info] (ThrusterSequence) Performing: Value {}, Duration {}s".format(
                node.value, node.duration))

            # Asks nicely for a ticket
            driver.submit_request(pin, node.value)

            # Waits before proceeding with the next node
            time.sleep(node.duration)

        # Tells the ESC to terminate
        driver.submit_request(pin, 0)


class SerialRequest:
    """
    Data structure representing a request
    """

    def __init__(self, pin: int, value: int):
        """
        Parameters:

                `pin`
                        The physical serial out pin to write to

                `value`
                        The serial value to write out
        """

        self.value: int = value
        self.pin: int = pin


class DriverInterface:
    """
    Wrapper for various pigpio stuff, as well as the actual request handling
    """

    def __init__(self):
        self.request_buffer: list[SerialRequest] = []

        self.pi = None

    def init_pi(self):
        """
        Sets the 'pi' property to the local pi, using pigpio
        """
        if DEBUG_NO_PI:
            print(
                "[info] (Debug) DEBUG_NO_PI mode has been set to True, `init_pi` has been skipped.")
            return

        self.pi = pigpio.pi()

    def submit_request(self, pin: int, value: int):
        self.request_buffer.append(SerialRequest(pin, value))

    def __process_request(self, request: SerialRequest):
        """
        This assumes the pi is initialized!
        """

        self.pi.set_servo_pulsewidth(request.pin, request.value)

    def process_request_buffer(self):
        if self.pi == None:
            return

        # No point if there's no work
        if len(self.request_buffer) == 0:
            return

        index: int = 0
        for request in self.request_buffer:

            # Process and clear the request
            self.__process_request(request)
            self.request_buffer.pop(index)

            index += 1

        print_debug(
            "[info] (DriverInterface) Processed {} requests.".format(index))

# Default sequences


class SEQUENCES:

    # Initialize a BESC30-R3
    INIT = ThrusterSequence([
        SequenceNode(1.5, 1500),
    ])

    # Terminate a BESC30-R3
    END = ThrusterSequence([
        SequenceNode(1.0, 0)
    ])

    # Initialize the ESC, run the thruster, and then terminate the ESC.
    # Good for checking if a thruster is alive
    THRUSTER_TEST = ThrusterSequence([
        SequenceNode(1.5, 1500),
        SequenceNode(1.5, 1550),
        SequenceNode(1.0, 0)
    ])


# Generic testing pin looool
# TODO: Write a control system that manages every pin
TESTING_PIN = 4


def thruster_seq(driver: DriverInterface, seq: ThrusterSequence, pin: int):
    """
    Brief:
            Execute a thruster sequence using a thread.
    Parameters:
                    `driver`
                            Reference to the active driver interface

                    `seq`
                            The sequence to execute

                    `pin`
                            The pin to execute the sequence on (e.g. which thruster)


    Returns:
            Thread
    """

    thread = threading.Thread(target=seq.exec_seq, args=(driver, pin,))
    thread.start()

    return thread


def driver_processor(driver: DriverInterface):
    """
    Brief:
        This will indefinitely compute a driver's request buffer.
    Parameters:
        `driver`
                The driver to compute
    """

    # This is stupid.
    # FIXME: Add an explicit exit point, ideally managed by the robot client's core.
    while True:
        driver.process_request_buffer()


def main():
    # Bind the driver to a pi
    driver = DriverInterface()
    driver.init_pi()

    # Start the processor
    processor = threading.Thread(target=driver_processor, args=(driver,))
    processor.start()

    # Run the thruster sequence. These two lines *need* to be replaced with
    # something that can recieve control system information. For the purposes
    # of running test sequences, however, this is ideal.
    test_thread = thruster_seq(driver, SEQUENCES.THRUSTER_TEST, TESTING_PIN)
    test_thread.join()

    # NOTE: Processor will not explicitly exit.
    processor.join()


if __name__ == "__main__":
    main()
