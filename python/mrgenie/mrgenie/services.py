import abc


class Service:
    @abc.abstractmethod
    def get_rooms(self):
        """
        Get all the rooms in the system
        :return: list of (id, name) tuples
        """
        return []

    @abc.abstractmethod
    def get_reservations(self, room_id):
        """
        Get reservations for a room
        :param room_id: id of the room
        :return: list of {'start_date': ?, 'end_date': }
        """
        return []

    @abc.abstractmethod
    def make_reservation(self, room_id):
        """
        Make a reservation right now. The backend may reject the request
        :param room_id: id of the room
        :return: True if the request was accepted, or else False
        """
        return False

    @abc.abstractmethod
    def cancel_reservation(self, room_id):
        """
        Cancel the current reservation. The backend may reject the request
        :param room_id: id of the room
        :return: True if the request was accepted, or else False
        """
        return False
