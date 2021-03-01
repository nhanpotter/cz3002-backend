from rest_framework import renderers
import json
class ErrorRenderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            if 'error' in data:
                response = json.dumps({'errors': data['error']})
            else:
                response = json.dumps({'errors': data})
        else:
            response = json.dumps(data)
        return response