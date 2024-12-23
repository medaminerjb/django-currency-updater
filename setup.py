from setuptools import setup, find_packages

setup(
    name="django-currency-updater",
    version="0.1.0",
    description="A reusable Django library for updating currency rates",
    author="medaminerjb",
    author_email="meda30449@gmail.com",
    url="https://github.com/medaminerjb/django-currency-update",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=3.2",
        "requests",
    ],
    extras_require={
        "automation": ["apscheduler"],  # Optional APScheduler dependency
    },
    classifiers=[
        "Framework :: Django",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
