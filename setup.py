from setuptools import setup, find_packages

setup(
    name="netsweep",
    version="1.0.0",
    author="Tu Nombre",
    description="Herramienta de escaneo de red avanzada (supera a nmap)",
    packages=find_packages(),
    install_requires=[
        "scapy>=2.5.0",
        "python-nmap>=0.7.1",
        "requests>=2.31.0",
        "colorama>=0.4.6",
        "netifaces>=0.11.0",
        "tabulate>=0.9.0",
        "pdfkit>=1.0.0",
        "jinja2>=3.1.2"
    ],
    entry_points={
        "console_scripts": [
            "netsweep=netsweep.cli:main"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)
