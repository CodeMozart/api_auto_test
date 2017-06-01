__author__ = 'widesky'

import pika
import os
import logging
import json

import libs.tools as tools


class RabbitAMQP:
    """
    RabbitAMQP method package
    """

    channel = None
    queue_name = None

    def __init__(self, conf_file_name='queue', vhost_name='wanplus'):
        """
        :param conf_file_name: config for the rabbitMQ
        :param vhost_name:
        :return:
        """

        vhost_conf_file = '%s/../../conf/%s.yaml' % (os.path.dirname(__file__), conf_file_name)
        vhost_conf = tools.get_conf_by_file_name(vhost_conf_file, 'vhost_' + vhost_name)
        if not vhost_conf:
            logging.error("not found conf")
            exit(1)

        if vhost_conf:
            credentials = pika.PlainCredentials(vhost_conf.get('login'), vhost_conf.get('password'))
            connection = pika.BlockingConnection(pika.ConnectionParameters(vhost_conf.get('host'),
                                                                           virtual_host=vhost_conf.get('vhost'),
                                                                           credentials=credentials))
            self.channel = connection.channel()

    def publish_message(self, queue_name=None, message_body=None):
        """
        Create file system path for this URL
        """

        if not queue_name or not message_body:
            return False

        if type(message_body) != unicode:
            message_body = json.dumps(message_body)

        try:

            return self.channel.basic_publish(exchange='', routing_key=queue_name, body=message_body)

        except Exception as e:
            logging.error('RabbitAMQP basic_publish error: %s' % str(e))
            return False



if __name__ == '__main__':
    mq = RabbitAMQP()
    message = 'message test!'
    mq.publish_message(queue_name='team_rank_stats', message_body=message)

    message = dict({"eid": 414, "scheduleid": 26179, "winner": 4459, "gametype": 6, "game": "kog"})
    mq.publish_message(queue_name='team_rank_stats', message_body=message)

    message = 121
    print mq.publish_message(queue_name='team_rank_stats', message_body=message)