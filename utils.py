def generate_success_response(status_code=200, msg='success'):
    return {
        'status': status_code,
        'message': msg
    }


def generate_error_response(status_code=500, error='Bad Request', msg="Server Error"):
    return {
        'status': status_code,
        'error': error,
        'message': msg
    }
