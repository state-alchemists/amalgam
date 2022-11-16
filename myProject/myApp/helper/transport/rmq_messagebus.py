from typing import Any, Callable
from pika.adapters.blocking_connection import BlockingConnection, BlockingChannel
from helper.transport.messagebus import MessageBus
from helper.transport.rmq_connection import RMQConnection
from helper.transport.rmq_config import RMQEventMap

import time
import pika
import threading
import traceback
import sys

class RMQMessageBus(RMQConnection, MessageBus):

    def __init__(self, rmq_connection_parameters: pika.ConnectionParameters, rmq_event_map: RMQEventMap):
        RMQConnection.__init__(self, rmq_connection_parameters)
        self._event_map=rmq_event_map
        self._error_count = 0


    def get_error_count(self) -> int:
        return self._error_count


    def handle(self, event_name: str) -> Callable[..., Any]:
        def register_event_handler(event_handler: Callable[[Any], Any]):
            exchange = self._event_map.get_exchange_name(event_name)
            queue = self._event_map.get_queue_name(event_name)
            dead_letter_exchange = self._event_map.get_dead_letter_exchange(event_name)
            dead_letter_queue = self._event_map.get_dead_letter_queue(event_name)
            auto_ack = self._event_map.get_auto_ack(event_name)
            arguments = self._event_map.get_queue_arguments(event_name)
            prefetch_count = self._event_map.get_prefetch_count(event_name)
            def consume():
                while not self._is_shutdown:
                    connection: BlockingConnection = None
                    try:
                        connection = self.create_connection()
                        ch = connection.channel()
                        if self._event_map.get_ttl(event_name) > 0:
                            ch.exchange_declare(exchange=dead_letter_exchange, exchange_type='fanout', durable=True)
                            ch.queue_declare(queue=dead_letter_queue, durable=True, exclusive=False)
                            ch.queue_bind(exchange=dead_letter_exchange, queue=dead_letter_queue)
                        ch.exchange_declare(exchange=exchange, exchange_type='fanout', durable=True)
                        ch.queue_declare(queue=queue, exclusive=False, durable=True, arguments=arguments)
                        ch.queue_bind(exchange=exchange, queue=queue)
                        ch.basic_qos(prefetch_count=prefetch_count)
                        # create handler and start consuming
                        on_event = self._create_event_handler(event_name, exchange, queue, auto_ack, event_handler)
                        ch.basic_consume(queue=queue, on_message_callback=on_event, auto_ack=auto_ack)
                        ch.start_consuming()
                    except:
                        print('Error while consuming queue {queue}'.format(queue=queue), file=sys.stderr)
                        self.remove_connection(connection)
                        self._error_count += 1
            thread = threading.Thread(target=consume)
            thread.start()
        return register_event_handler


    def _create_event_handler(self, event_name: str, exchange: str, queue: str, auto_ack: bool, event_handler: Callable[[Any], Any]):
        def on_event(ch, method, props, body):
            try:
                message = self._event_map.get_decoder(event_name)(body)
                print({'action': 'handle_rmq_event', 'event_name': event_name, 'message': message, 'exchange': exchange, 'routing_key': queue}, file=sys.stderr)
                event_handler(message)
            except Exception as exception:
                print('Error while handling event {event_name}'.format(event_name=event_name), file=sys.stderr)
                self._error_count += 1
                print(traceback.format_exc(), file=sys.stderr) 
            finally:
                if not auto_ack:
                    ch.basic_ack(delivery_tag=method.delivery_tag)
        return on_event


    def publish(self, event_name: str, message: Any) -> Any:
        try:
            connection = self.create_connection()
            exchange = self._event_map.get_exchange_name(event_name)
            routing_key = self._event_map.get_queue_name(event_name)
            body = self._event_map.get_encoder(event_name)(message)
            ch = connection.channel()
            ch.exchange_declare(exchange=exchange, exchange_type='fanout', durable=True)
            print({'action': 'publish_rmq_event', 'event_name': event_name, 'message': message, 'exchange': exchange, 'routing_key': routing_key, 'body': body}, file=sys.stderr)
            ch.basic_publish(
                exchange=exchange,
                routing_key=routing_key,
                body=body
            )
            self.remove_connection(connection)
        except Exception as exception:
            print('Error while publishing event {event_name} with messages: {message}'.format(event_name=event_name, message=message), file=sys.stderr)
            self._error_count += 1
            raise exception