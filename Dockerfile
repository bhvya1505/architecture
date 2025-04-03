# Use Miniconda as base image
FROM condaforge/miniforge3:latest

# Set environment variables
ENV PATH=/opt/conda/bin:$PATH

# Copy the environment.yml to the container
COPY environment.yml /tmp/environment.yml

# Create the conda environment
RUN conda env create -f /tmp/environment.yml

# Activate conda environment by default
ENV CONDA_DEFAULT_ENV=myenv
RUN echo "conda activate myenv" >> ~/.bashrc
SHELL ["/bin/bash", "--login", "-c"]

# Set the working directory
WORKDIR /app

# Copy the FastAPI app to the container
COPY . /app

# Expose the port FastAPI will run on
EXPOSE 8000

# Run the app using uvicorn
CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]