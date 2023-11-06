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

    def start_rendering(self, request, response):
        self.request = request
        self.response = response

        # Assign position
        if self.response.parent:
            self.response.step_position = self.response.find_parent_response_collection().step_position + 1

    def has_child_queue(self):
        return self.response.step_position >= len(self.request.steps)
