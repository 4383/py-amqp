"""AMQP Messages."""
# Copyright (C) 2007-2008 Barry Pederson <bp@barryp.org>
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301

# Intended to fix #85: ImportError: cannot import name spec
# Encountered on python 2.7.3
# "The submodules often need to refer to each other. For example, the
#  surround [sic] module might use the echo module. In fact, such
#  references are so common that the import statement first looks in
#  the containing package before looking in the standard module search
#  path."
# Source:
#   http://stackoverflow.com/a/14216937/4982251
from typing import Any, MutableMapping
from typing import Mapping  # noqa
from .types import ChannelT
from .spec import Basic
from .serialization import GenericContent
from .types import MessageT

__all__ = ['Message']


class Message(GenericContent, MessageT):
    """A Message for use with the Channnel.basic_* methods.

    Expected arg types

        body: string
        children: (not supported)

    Keyword properties may include:

        content_type: shortstr
            MIME content type

        content_encoding: shortstr
            MIME content encoding

        application_headers: table
            Message header field table, a dict with string keys,
            and string | int | Decimal | datetime | dict values.

        delivery_mode: octet
            Non-persistent (1) or persistent (2)

        priority: octet
            The message priority, 0 to 9

        correlation_id: shortstr
            The application correlation identifier

        reply_to: shortstr
            The destination to reply to

        expiration: shortstr
            Message expiration specification

        message_id: shortstr
            The application message identifier

        timestamp: datetime.datetime
            The message timestamp

        type: shortstr
            The message type name

        user_id: shortstr
            The creating user id

        app_id: shortstr
            The creating application id

        cluster_id: shortstr
            Intra-cluster routing identifier

        Unicode bodies are encoded according to the 'content_encoding'
        argument. If that's None, it's set to 'UTF-8' automatically.

        Example::

            msg = Message('hello world',
                            content_type='text/plain',
                            application_headers={'foo': 7})
    """

    CLASS_ID: int = Basic.CLASS_ID

    #: Instances of this class have these attributes, which
    #: are passed back and forth as message properties between
    #: client and server
    PROPERTIES = [
        ('content_type', 's'),
        ('content_encoding', 's'),
        ('application_headers', 'F'),
        ('delivery_mode', 'o'),
        ('priority', 'o'),
        ('correlation_id', 's'),
        ('reply_to', 's'),
        ('expiration', 's'),
        ('message_id', 's'),
        ('timestamp', 'L'),
        ('type', 's'),
        ('user_id', 's'),
        ('app_id', 's'),
        ('cluster_id', 's')
    ]

    def __init__(self,
                 body: bytes = b'',
                 children: Any = None,
                 channel: ChannelT = None,
                 **properties) -> None:
        super().__init__(**properties)
        self.body = body
        self.channel = channel
        self.children = children  # unsupported
        self.delivery_info = {}  # set by basic_consume/_get

    @property
    def headers(self) -> MutableMapping:
        return self.properties.get('application_headers')

    @property
    def delivery_tag(self) -> str:
        return self.delivery_info.get('delivery_tag')
