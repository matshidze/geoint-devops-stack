FROM python:3.12-slim

# Security: non-root user
RUN useradd -m geointuser

WORKDIR /app

COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app /app/app
COPY docker/entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh

ENV PYTHONPATH=/app

ENV PYTHONUNBUFFERED=1
ENV APP_HOST=0.0.0.0
EXPOSE 5000

USER geointuseruser

ENTRYPOINT ["/app/entrypoint.sh"]

CMD ["gunicorn", "-b", "0.0.0.0:5000", "app.app:create_app_for_gunicorn()", "--workers", "2", "--threads", "4"]

