import time
from modules.request import Request
from modules.logger import CustomLogger
from typing import Callable, Optional


class Queue:
    """
    Class that implements a request queue.

    Attributes:
        timeout (int): Timeout in seconds for the queue's run method.
        logger (CustomLogger): Logger instance for logging.
        processing_function (Callable): Function to be called to process a request.
    """

    def __init__(
        self,
        timeout: int,
        logger: CustomLogger,
        processing_function: Optional[Callable] = None,
    ) -> None:
        """
        Create a new request queue.

        Args:
            timeout (int): Timeout in seconds for the queue's run method.
            logger (CustomLogger): Logger instance for logging.
            processing_function (Callable): Function to be called to process a request.
        """
        self.__queue: list[Request] = []
        self.__timeout = timeout
        self.__logger = logger
        self.__processing_function = processing_function

    def user_in_queue(self, user_id: int, request_type: str) -> bool:
        """
        Check if a user is already in the queue for a specific request type.

        Args:
            user_id (int): User's id.
            request_type (str): Request type.

        Returns:
            bool: If the user is in the queue for the specified request type.
        """
        for item in self.__queue:
            if item.user_id == user_id and item.request_type == request_type:
                return True
        return False

    def put(self, item: Request) -> None:
        """
        Add a request to the queue.

        Args:
            item (Request): Request to be added.
        """
        self.__queue.append(item)
        self.__logger.info(f"Request {item.request_type} added to queue.", "server")

    def get(self) -> Request:
        """
        Remove and return the oldest request from the queue.

        Returns:
            Request: The oldest request in the queue.
        """
        item = self.__queue.pop(0)
        self.__logger.info(f"Request {item.request_type} removed from queue.", "server")
        return item

    def __len__(self) -> int:
        """
        Return the length of the queue.

        Returns:
            int: Length of the queue.
        """
        length = len(self.__queue)
        return length

    def run(self) -> None:
        """
        Continuously process the requests in the queue.

        The function will sleep for the queue's timeout between iterations.
        """
        while True:
            if self.__queue:
                item = self.get()
                if self.__processing_function is not None:
                    self.__processing_function(item)
                self.__logger.info(f"Request {item.request_type} processed.", "server")
            time.sleep(self.__timeout)

    @property
    def processing_function(self) -> Optional[Callable]:
        """
        Get the processing function.

        Returns:
            Callable: The processing function.
        """
        return self.__processing_function

    @processing_function.setter
    def processing_function(self, processing_function: Callable) -> None:
        """
        Set the processing function.

        Args:
            processing_function (Callable): The new processing function.
        """
        self.__processing_function = processing_function

    @property
    def timeout(self) -> int:
        """
        Get the timeout.

        Returns:
            int: The timeout in seconds.
        """
        return self.__timeout
