import fastapi
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.instrumentation.httpx import HTTPXClientInstrumentor
from opentelemetry.instrumentation.redis import RedisInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

from opentelemetry_pycon import tracing


EXPORTER: OTLPSpanExporter = OTLPSpanExporter(endpoint='opentelemetry-collector:4317', insecure=True)
TRACE_PROVIDER: TracerProvider = TracerProvider(
    resource=Resource.create(
        {
            SERVICE_NAME: 'opentelemetry-pycon',
        }
    )
)
TRACE_PROVIDER.add_span_processor(BatchSpanProcessor(EXPORTER))
trace.set_tracer_provider(TRACE_PROVIDER)
FASTAPI_APP: fastapi.FastAPI = fastapi.FastAPI()
FASTAPI_APP.include_router(tracing.FASTAPI_ROUTER)


@FASTAPI_APP.on_event('startup')
def on_startup():
    FastAPIInstrumentor().instrument_app(FASTAPI_APP)
    RedisInstrumentor().instrument()
    HTTPXClientInstrumentor().instrument()


@FASTAPI_APP.on_event('shutdown')
def on_shutdown():
    FastAPIInstrumentor().uninstrument_app(FASTAPI_APP)
    RedisInstrumentor().uninstrument()
    HTTPXClientInstrumentor().uninstrument()
