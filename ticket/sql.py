# coding: utf-8
from ticket.models import Ticket
from ticket.serializer import TicketSerializer


class TicketSql:
    @staticmethod
    def get_ticket(ticket):
        ticket = Ticket.objects.filter(ticket=ticket).first()
        return TicketSerializer(ticket).data

    @staticmethod
    def create_ticket(**kwargs):
        Ticket.objects.create(**kwargs)

    @staticmethod
    def delete_ticket(ticket):
        Ticket.objects.filter(ticket=ticket).delete()


ticket_sql = TicketSql()
