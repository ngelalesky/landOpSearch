from setuptools import setup, find_packages

setup(
    name="land-agent-backend",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "pydantic>=2.6.0",
        "numpy>=1.24.0",
        "stable-baselines3>=2.2.1",
        "torch>=2.1.0",
        "gymnasium>=0.29.1",
    ],
) 