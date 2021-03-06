# Copyright 2017 Open Source Robotics Foundation, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ros2srv.api import get_service_path
from ros2srv.api import service_type_completer
from ros2srv.verb import VerbExtension


class ShowVerb(VerbExtension):
    """Output the service definition."""

    def add_arguments(self, parser, cli_name):
        arg = parser.add_argument(
            'service_type',
            help="Type of the ROS service (e.g. 'std_srvs/Trigger')")
        arg.completer = service_type_completer

    def main(self, *, args):
        # TODO(dirk-thomas) this logic should come from a rosidl related
        # package
        try:
            package_name, service_name = args.service_type.split('/', 2)
            if not package_name or not service_name:
                raise ValueError()
        except ValueError:
            raise RuntimeError('The passed service type is invalid')
        try:
            path = get_service_path(package_name, service_name)
        except LookupError as e:
            return str(e)
        with open(path, 'r') as h:
            print(h.read(), end='')
