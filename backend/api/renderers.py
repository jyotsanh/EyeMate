from rest_framework.renderers import JSONRenderer
from rest_framework.utils.serializer_helpers import ReturnList, ReturnDict

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # If the response data is a dict and contains the "errors" key, it's an error response
        if isinstance(data, (dict, ReturnDict)) and data.get('errors', None):
            response = {
                'status': 'error',
                'errors': data['errors']
            }
        # If the response data is a list, treat it as a successful list response
        elif isinstance(data, (list, ReturnList)):
            response = {
                'status': 'success',
                'data': data
            }
        # Otherwise, treat it as a general successful response
        else:
            response = {
                'status': 'success',
                'data': data
            }

        # Render the final response using the parent class's render method
        return super(CustomJSONRenderer, self).render(response, accepted_media_type, renderer_context)
