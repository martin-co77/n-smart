from flask import jsonify


class Response:
    data = None
    status_code = None
    status_text = None
    status = None

    def set(
            self,
            status_text,
            status=False,
            status_code=200,
            data=None
    ):
        self.status = status
        self.status_text = status_text
        self.status_code = status_code
        self.data = data or dict({})
        return self

    def jsonify(self):
        return jsonify({
            'status': self.status,
            'status_text': self.status_text,
            'status_code': self.status_code,
            'data': self.data
        }), self.status_code
