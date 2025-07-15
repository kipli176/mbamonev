# Gunakan image Python versi stabil
FROM python:3.11-slim

# Set direktori kerja di dalam container
WORKDIR /app

# Salin semua file ke dalam container
COPY . /app

# Install dependensi Python (gunakan requirements.txt jika tersedia)
RUN pip install -r requirements.txt

# Expose port Flask (default 5000)
EXPOSE 5005

# Jalankan aplikasi Flask
CMD ["python", "app.py"]
