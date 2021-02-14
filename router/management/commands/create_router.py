from django.core.management.base import BaseCommand
from django.utils.crypto import get_random_string
import random
from router.models import Device
import socket
import struct
import ipaddress


class Command(BaseCommand):
    help = 'Create random router'

    def add_arguments(self, parser):
        parser.add_argument('total', type=int, help='Indicates the number of router to be created')

    def random_MAC(self):
        mac = [0x00, 0x16, 0x3e,
               random.randint(0x00, 0x7f),
               random.randint(0x00, 0xff),
               random.randint(0x00, 0xff)]
        return ':'.join(map(lambda x: "%02x" % x, mac))

    def ip_addr(self):
        result = socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
        return result

    def handle(self, *args, **kwargs):
        total = kwargs['total']
        for i in range(total):
            Device.objects.create(hostname=get_random_string(8),
                                  sapid = random.randint(10,999),
                                  mac_address = self.random_MAC(),
                                  loopback = ipaddress.ip_address(self.ip_addr()),
                                  ip_address= socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))
                                  )