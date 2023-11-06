from __future__ import annotations
from src.helper.args import arg_shift


class QueuedCollectionPathManager:
    def __init__(self, root_request):
        self.root_request = root_request
        self.response = None
        self.request = None
        self.steps = [None]

        args = list(root_request.args_tmp)
        steps = arg_shift(args, 'command-request-step')
        if steps:
            self.steps = list(map(int, str(steps).split('.')))

    def set_current_response(self, response):
        self.response = response

    def set_current_request(self, request):
        self.request = request

    def has_child_queue(self):
        return self.response.step_position >= len(self.request.steps)
