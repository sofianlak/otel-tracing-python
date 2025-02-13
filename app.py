import time
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, SimpleSpanProcessor
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.semconv.resource import ResourceAttributes

# Set up OpenTelemetry trace provider with a service name
resource = Resource.create({ResourceAttributes.SERVICE_NAME: "my_python_app"})
trace.set_tracer_provider(TracerProvider(resource=resource))

# Export traces to console for debugging purposes
console_exporter = ConsoleSpanExporter()
trace.get_tracer_provider().add_span_processor(SimpleSpanProcessor(console_exporter))

# Export traces to OTLP collector
span_processor = SimpleSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4317"))
trace.get_tracer_provider().add_span_processor(span_processor)

# Create a tracer
tracer = trace.get_tracer(__name__)

# Simulate some work in your application
def do_work():
    with tracer.start_as_current_span("work_span") as work_span:
        print("Starting the epic quest of work...")
        time.sleep(1)  # Simulate work by sleeping for 1 second

        with tracer.start_as_current_span("subtask_1") as subtask_1_span:
            print("Embarking on subtask 1: Slaying the dragon...")
            time.sleep(3)  # Simulate subtask 1 by sleeping for 3 second
            print("Subtask 1 complete: Dragon defeated!")

        with tracer.start_as_current_span("subtask_2") as subtask_2_span:
            print("Embarking on subtask 2: Finding the treasure...")
            time.sleep(1)  # Simulate subtask 2 by sleeping for 1 second
            print("Subtask 2 complete: Treasure found!")

        print("Epic quest complete: Work done.")

if __name__ == "__main__":
    print("Starting work...")
    do_work()
    print("Work completed.")
