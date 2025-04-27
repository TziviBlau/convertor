FROM python:3.10-slim AS builder

WORKDIR /app

COPY requirements.txt .

# Install dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc && \
    pip install --no-cache-dir --user -r requirements.txt

FROM python:3.10-slim

WORKDIR /app

# Copy only necessary files from builder
COPY --from=builder /root/.local /root/.local
COPY convert_image_to_pdf.py .

# Make sure the script is executable
RUN chmod +x convert_image_to_pdf.py

# Add Python user packages to path
ENV PATH=/root/.local/bin:$PATH

# Create directories for volumes
RUN mkdir -p images output

# Set default for PDF_NAME environment variable
ENV PDF_NAME=output.pdf

# Default command
ENTRYPOINT ["python", "convert_image_to_pdf.py"]
CMD ["images"]
