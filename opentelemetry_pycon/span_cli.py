from opentelemetry import context, trace
from opentelemetry.propagate import extract, inject
from opentelemetry.trace import span
from opentelemetry.trace.status import Status, StatusCode


def client_task(message: str):
    current_span: span.Span
    with trace.get_tracer_provider().get_tracer(__name__).start_as_current_span('send', kind=trace.SpanKind.CLIENT) as current_span:
        headers: dict = {}
        inject(headers)
        current_span.set_attribute('text', message)
        server_task(message, headers)
        current_span.set_status(Status(StatusCode.OK))


def server_task(message: str, headers: dict):
    context.attach(extract(headers))
    current_span: span.Span
    with trace.get_tracer_provider().get_tracer(__name__).start_as_current_span('receive', kind=trace.SpanKind.SERVER) as current_span:
        current_span.set_attribute('text', message)
        print(f'Message received: {message}')
        current_span.set_status(Status(StatusCode.OK))


if __name__ == '__main__':
    while True:
        message: str = input('Input message:')
        client_task(message)
