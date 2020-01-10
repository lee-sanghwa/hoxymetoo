import json, os, logging
from datetime import datetime


class HttpHandler(logging.Handler):
    today_date = datetime.now().strftime("%Y-%m-%d")

    def emit(self, record):
        try:
            request = record.request
            record.ip = request.META.get('HTTP_X_FORWARDED_FOR')
            record.test = 'test'
            f = open(
                f'{os.fspath(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))}/{self.today_date}_debug.log',
                'a')
            f.write(f'[ {record.ip} ] ')
        except Exception:
            pass


def create_log_content(request):
    meta_data_of_request = request.META
    request_info_string = '  ||  USER-IP: ' + meta_data_of_request.get('HTTP_X_FORWARDED_FOR')
    request_info_string += '  ||  PATH_INFO: ' + meta_data_of_request.get('PATH_INFO')
    request_info_string += '  ||  QUERY_STRING: ' + meta_data_of_request.get('QUERY_STRING')
    request_info_string += '  ||  REQUEST_METHOD: ' + meta_data_of_request.get('REQUEST_METHOD')
    request_info_string += '  ||  HTTP_USER_AGENT:  ' + meta_data_of_request.get('HTTP_USER_AGENT').split(' ')[0]
    request_info_string += '  ||  REQUEST_BODY: ' + json.dumps(dict(request.data))

    return request_info_string + '\n\n'
