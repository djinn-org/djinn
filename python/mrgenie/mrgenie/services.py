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
        :return: list of {'start_date': ?, 'end_date': }
        """
        return []
