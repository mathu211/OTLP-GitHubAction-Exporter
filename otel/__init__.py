import logging

from opentelemetry import metrics, trace
from opentelemetry.sdk.resources import SERVICE_NAME
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.http._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader

def create_otel_attributes(atts, GITHUB_SERVICE_NAME):
    attributes={SERVICE_NAME: GITHUB_SERVICE_NAME}
    for att in atts:
            attributes[att]=atts[att]
    return attributes

def otel_logger(endpoint, headers, resource, name):
    exporter = OTLPLogExporter(endpoint=f"{endpoint}v1/logs",headers=headers)
    logger = logging.getLogger(str(name))
    logger.handlers.clear()
    logger_provider = LoggerProvider(resource=resource)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(exporter))
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    logger.addHandler(handler)
    return logger


def otel_tracer(endpoint, headers, resource, tracer):
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=f"{endpoint}v1/traces",headers=headers))
    tracer = TracerProvider(resource=resource)
    tracer.add_span_processor(processor)
    tracer = trace.get_tracer(__name__, tracer_provider=tracer)

    return tracer

def otel_meter(endpoint, headers, resource, meter):
    reader = PeriodicExportingMetricReader(OTLPMetricExporter(endpoint=f"{endpoint}v1/metrics",headers=headers))
    provider = MeterProvider(resource=resource, metric_readers=[reader])
    meter = metrics.get_meter(__name__,meter_provider=provider)
    return meter