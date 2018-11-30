import datetime
import io
import os
import logging
import tarfile

import docker

from collections import namedtuple

logging.basicConfig()
logger = logging.getLogger(name=__file__)


class ContainerTests:

    def __init__(self, suite_name, dockerfile=None, image_tag=None):
        self.suite_name = suite_name
        self.start_time = None
        self.end_time = None

        self._client = docker.from_env()
        self._dockerfile = dockerfile if dockerfile is not None else os.path.join(os.path.dirname(__file__), 'Dockerfile')
        self._image_tag = image_tag if image_tag is not None else 'container-test'
        self._tests = []

        self.__TestContainer = namedtuple('TestContainer', ['name', 'container'])

    def start_test(self, test_name, cmd, **kwargs):
        """
        Start a test container
        :param test_name: The name of the test
        :param cmd: The command that starts the test
        :param kwargs: Any kwargs to pass to the container
        :return:
        """
        if not os.path.isdir('results'):
            os.mkdir('results')

        container = self._client.containers.run(self._image_tag, command=cmd, detach=True, **kwargs)

        self._tests.append(self.__TestContainer(test_name, container))

        with open('results/{}-{}-{}.log'.format(self.suite_name, test_name, self.start_time), mode='wb') as f:
            for line in container.logs(stream=True, timestamps=True):
                print(line.decode('utf-8'))
                f.write(line)

    def _cleanup(self):
        for test in self._tests:
            results = test.container.get_archive('/results')

            for item in results[0]:
                tar = tarfile.TarFile(fileobj=io.BytesIO(item))
                tar.extractall()

            test.container.remove(v=True, force=True)

    def __enter__(self):
        self.start_time = datetime.datetime.now().isoformat()
        self._client.images.build(path=os.path.dirname(self._dockerfile), tag=self._image_tag)

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end_time = datetime.datetime.now().isoformat()

        if exc_type is not None:
            logger.error(exc_type)
            logger.error(exc_val)
            logger.error(exc_tb)
            return False

        self._cleanup()

        return True
