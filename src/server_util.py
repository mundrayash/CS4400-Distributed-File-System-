def url_builder(ip, port, endpoints=''):
    return 'http://' + ip + ':' + str(port) + '/' + str(endpoints)

def file_missing_error(file_id):
    return {'message': '{} does not exist'.format(file_id)}, 404

def no_servers_error():
    return {'message': 'No server available'}, 503

def file_already_exists_error(file_id):
    return {'message': '{} already exists'.format(file_id)}, 400