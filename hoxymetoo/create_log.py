import json


def create_log_content(request):
    meta_data_of_request = request.META
    request_info_string = str()
    # request_info_string = '|| USER-IP : ' + meta_data_of_request.get('HTTP_X_FORWARDED_FOR')
    request_info_string += '|| PATH_INFO : ' + meta_data_of_request.get('PATH_INFO')
    request_info_string += '|| REQUEST_METHOD : ' + meta_data_of_request.get('REQUEST_METHOD')
    request_info_string += '|| HTTP_USER_AGENT : ' + meta_data_of_request.get('HTTP_USER_AGENT').split(' ')[0]
    request_info_string += '|| REQUEST_BODY : ' + json.dumps(dict(request.data))

    return request_info_string + '\n\n'
